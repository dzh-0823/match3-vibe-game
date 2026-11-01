"""Persistent top-score storage and completed-game policy."""

from __future__ import annotations

from dataclasses import dataclass
import json
import os
from pathlib import Path


LEADERBOARD_LIMIT = 5
SCHEMA_VERSION = 1
APP_DATA_DIRECTORY = "Match3VibeGame"
HIGH_SCORE_FILENAME = "high_scores.json"


class HighScoreError(RuntimeError):
    """Base class for recoverable high-score persistence failures."""


class HighScoreFormatError(HighScoreError):
    """Raised when an existing high-score file has an unsupported format."""


class HighScoreStorageError(HighScoreError):
    """Raised when high-score data cannot be read or written."""


def default_high_score_path() -> Path:
    """Return the per-user score path without creating files or directories."""
    local_app_data = os.environ.get("LOCALAPPDATA")
    if local_app_data:
        return Path(local_app_data) / APP_DATA_DIRECTORY / HIGH_SCORE_FILENAME
    return Path.home() / ".match3-vibe-game" / HIGH_SCORE_FILENAME


@dataclass(frozen=True)
class GameCompletion:
    scores: tuple[int, ...]
    saved: bool


class HighScoreStore:
    """Store a bounded, descending leaderboard in a versioned JSON file."""

    def __init__(self, path: str | Path, *, limit: int = LEADERBOARD_LIMIT) -> None:
        if type(limit) is not int or limit <= 0:
            raise ValueError("Leaderboard limit must be a positive integer.")
        self.path = Path(path)
        self.limit = limit

    def load(self) -> tuple[int, ...]:
        try:
            text = self.path.read_text(encoding="utf-8")
        except FileNotFoundError:
            return ()
        except UnicodeDecodeError as exc:
            raise HighScoreFormatError("The high-score file is not valid UTF-8.") from exc
        except OSError as exc:
            raise HighScoreStorageError("High scores could not be read.") from exc

        try:
            payload = json.loads(text)
        except json.JSONDecodeError as exc:
            raise HighScoreFormatError("The high-score file is not valid JSON.") from exc

        if (
            not isinstance(payload, dict)
            or type(payload.get("version")) is not int
            or payload.get("version") != SCHEMA_VERSION
        ):
            raise HighScoreFormatError("The high-score file uses an unsupported schema.")
        scores = payload.get("scores")
        if not isinstance(scores, list) or any(type(score) is not int or score < 0 for score in scores):
            raise HighScoreFormatError("The high-score file contains invalid scores.")
        return tuple(sorted(scores, reverse=True)[: self.limit])

    def record(self, score: int) -> tuple[int, ...]:
        if type(score) is not int or score < 0:
            raise ValueError("A completed-game score must be a non-negative integer.")

        try:
            scores = list(self.load())
        except HighScoreFormatError:
            # Malformed local data must not permanently block future scores.
            scores = []
        scores.append(score)
        scores = sorted(scores, reverse=True)[: self.limit]
        self._write(scores)
        return tuple(scores)

    def _write(self, scores: list[int]) -> None:
        temporary_path = self.path.with_name(f".{self.path.name}.{os.getpid()}.tmp")
        try:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            with temporary_path.open("w", encoding="utf-8", newline="\n") as stream:
                json.dump(
                    {"version": SCHEMA_VERSION, "scores": scores},
                    stream,
                    indent=2,
                )
                stream.write("\n")
                stream.flush()
                os.fsync(stream.fileno())
            os.replace(temporary_path, self.path)
        except OSError as exc:
            try:
                temporary_path.unlink(missing_ok=True)
            except OSError:
                pass
            raise HighScoreStorageError("High scores could not be saved.") from exc


class HighScoreService:
    """Own leaderboard state and decide which completed games are persisted."""

    def __init__(self, store: HighScoreStore) -> None:
        self.store = store
        self._scores: tuple[int, ...] = ()

    @property
    def scores(self) -> tuple[int, ...]:
        return self._scores

    def load(self) -> tuple[int, ...]:
        self._scores = self.store.load()
        return self._scores

    def complete_game(self, score: int) -> GameCompletion:
        if type(score) is not int or score < 0:
            raise ValueError("A completed-game score must be a non-negative integer.")
        if score == 0:
            return GameCompletion(self._scores, False)
        self._scores = self.store.record(score)
        return GameCompletion(self._scores, True)
