from __future__ import annotations

import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from high_scores import (
    APP_DATA_DIRECTORY,
    HIGH_SCORE_FILENAME,
    SCHEMA_VERSION,
    HighScoreFormatError,
    HighScoreService,
    HighScoreStorageError,
    HighScoreStore,
    default_high_score_path,
)
from main import format_leaderboard


class DefaultPathTests(unittest.TestCase):
    def test_default_path_uses_local_app_data(self) -> None:
        base = Path("C:/Users/Test/AppData/Local")
        with patch.dict(os.environ, {"LOCALAPPDATA": str(base)}):
            self.assertEqual(
                default_high_score_path(),
                base / APP_DATA_DIRECTORY / HIGH_SCORE_FILENAME,
            )


class HighScoreStoreTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory(dir=Path(__file__).resolve().parent)
        self.addCleanup(self.temporary_directory.cleanup)
        self.path = Path(self.temporary_directory.name) / "scores" / "high_scores.json"
        self.store = HighScoreStore(self.path)

    def test_missing_file_loads_as_empty_without_creating_data(self) -> None:
        self.assertEqual(self.store.load(), ())
        self.assertFalse(self.path.exists())

    def test_scores_persist_sort_descending_keep_duplicates_and_limit_to_five(self) -> None:
        for score in (40, 120, 80, 120, 5, 200):
            self.store.record(score)

        expected = (200, 120, 120, 80, 40)
        self.assertEqual(HighScoreStore(self.path).load(), expected)
        payload = json.loads(self.path.read_text(encoding="utf-8"))
        self.assertEqual(payload, {"version": SCHEMA_VERSION, "scores": list(expected)})

    def test_malformed_file_is_reported_and_next_score_recovers_it(self) -> None:
        self.path.parent.mkdir(parents=True)
        self.path.write_text("not-json", encoding="utf-8")

        with self.assertRaises(HighScoreFormatError):
            self.store.load()

        self.assertEqual(self.store.record(70), (70,))
        self.assertEqual(HighScoreStore(self.path).load(), (70,))

    def test_unsupported_schema_and_invalid_scores_are_rejected(self) -> None:
        invalid_payloads = (
            {"version": 2, "scores": [10]},
            {"version": True, "scores": [10]},
            {"version": 1, "scores": "10"},
            {"version": 1, "scores": [True]},
            {"version": 1, "scores": [-1]},
        )
        self.path.parent.mkdir(parents=True)
        for payload in invalid_payloads:
            with self.subTest(payload=payload):
                self.path.write_text(json.dumps(payload), encoding="utf-8")
                with self.assertRaises(HighScoreFormatError):
                    self.store.load()

    def test_invalid_score_and_limit_values_are_rejected(self) -> None:
        for score in (-1, True, 1.5, "10"):
            with self.subTest(score=score), self.assertRaises(ValueError):
                self.store.record(score)  # type: ignore[arg-type]
        for limit in (0, -1, True, 1.5):
            with self.subTest(limit=limit), self.assertRaises(ValueError):
                HighScoreStore(self.path, limit=limit)  # type: ignore[arg-type]

    def test_read_failure_is_reported_as_storage_error(self) -> None:
        with patch.object(Path, "read_text", side_effect=OSError("denied")):
            with self.assertRaises(HighScoreStorageError):
                self.store.load()

    def test_failed_atomic_replace_removes_temporary_file(self) -> None:
        temporary_path = self.path.with_name(f".{self.path.name}.{os.getpid()}.tmp")
        with patch("high_scores.os.replace", side_effect=OSError("denied")):
            with self.assertRaises(HighScoreStorageError):
                self.store.record(50)
        self.assertFalse(self.path.exists())
        self.assertFalse(temporary_path.exists())


class HighScoreServiceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory(dir=Path(__file__).resolve().parent)
        self.addCleanup(self.temporary_directory.cleanup)
        self.path = Path(self.temporary_directory.name) / "high_scores.json"
        self.store = HighScoreStore(self.path)
        self.service = HighScoreService(self.store)

    def test_zero_point_game_is_not_added_to_existing_leaderboard(self) -> None:
        self.store.record(90)
        self.assertEqual(self.service.load(), (90,))
        before = self.path.read_bytes()

        result = self.service.complete_game(0)

        self.assertFalse(result.saved)
        self.assertEqual(result.scores, (90,))
        self.assertEqual(self.path.read_bytes(), before)

    def test_positive_completed_game_updates_cached_and_persistent_scores(self) -> None:
        self.store.record(50)
        self.service.load()

        result = self.service.complete_game(110)

        self.assertTrue(result.saved)
        self.assertEqual(result.scores, (110, 50))
        self.assertEqual(self.service.scores, (110, 50))
        self.assertEqual(HighScoreStore(self.path).load(), (110, 50))

    def test_positive_game_recovers_after_malformed_startup_data(self) -> None:
        self.path.write_text("broken", encoding="utf-8")
        with self.assertRaises(HighScoreFormatError):
            self.service.load()

        result = self.service.complete_game(60)

        self.assertTrue(result.saved)
        self.assertEqual(result.scores, (60,))
        self.assertEqual(HighScoreStore(self.path).load(), (60,))


class LeaderboardPresentationTests(unittest.TestCase):
    def test_leaderboard_text_handles_empty_and_ranked_scores(self) -> None:
        self.assertEqual(format_leaderboard(()), "Top scores: No completed games yet.")
        self.assertEqual(
            format_leaderboard((200, 120, 80)),
            "Top scores: 1. 200  |  2. 120  |  3. 80",
        )


if __name__ == "__main__":
    unittest.main()
