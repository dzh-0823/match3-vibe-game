"""Testable match-3 board, move, resolution, and scoring logic."""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
import random
from typing import Callable


BOARD_ROWS = 8
BOARD_COLUMNS = 8
TILE_TYPES = 6
POINTS_PER_TILE = 10

Coordinate = tuple[int, int]
Tile = int | None
Board = list[list[Tile]]
ResolutionObserver = Callable[[int, int], None]


@dataclass(frozen=True)
class MoveResult:
    accepted: bool
    reason: str
    cleared_tiles: int = 0
    cascades: int = 0
    reshuffled: bool = False


def copy_board(board: Board) -> Board:
    return [row[:] for row in board]


def in_bounds(board: Board, coordinate: Coordinate) -> bool:
    row, column = coordinate
    return bool(board) and 0 <= row < len(board) and 0 <= column < len(board[0])


def are_adjacent(first: Coordinate, second: Coordinate) -> bool:
    return abs(first[0] - second[0]) + abs(first[1] - second[1]) == 1


def find_matches(board: Board) -> set[Coordinate]:
    """Return the union of every horizontal and vertical run of length 3+."""
    if not board or not board[0]:
        return set()
    rows = len(board)
    columns = len(board[0])
    matched: set[Coordinate] = set()

    for row in range(rows):
        start = 0
        while start < columns:
            tile = board[row][start]
            end = start + 1
            while end < columns and tile is not None and board[row][end] == tile:
                end += 1
            if tile is not None and end - start >= 3:
                matched.update((row, column) for column in range(start, end))
            start = end

    for column in range(columns):
        start = 0
        while start < rows:
            tile = board[start][column]
            end = start + 1
            while end < rows and tile is not None and board[end][column] == tile:
                end += 1
            if tile is not None and end - start >= 3:
                matched.update((row, column) for row in range(start, end))
            start = end
    return matched


def _swap(board: Board, first: Coordinate, second: Coordinate) -> None:
    first_row, first_column = first
    second_row, second_column = second
    board[first_row][first_column], board[second_row][second_column] = (
        board[second_row][second_column],
        board[first_row][first_column],
    )


def swap_creates_match(board: Board, first: Coordinate, second: Coordinate) -> bool:
    if not in_bounds(board, first) or not in_bounds(board, second) or not are_adjacent(first, second):
        return False
    _swap(board, first, second)
    matches = find_matches(board)
    _swap(board, first, second)
    return bool(matches and (first in matches or second in matches))


def has_legal_move(board: Board) -> bool:
    if not board or not board[0] or any(tile is None for row in board for tile in row):
        return False
    rows = len(board)
    columns = len(board[0])
    for row in range(rows):
        for column in range(columns):
            here = (row, column)
            if column + 1 < columns and swap_creates_match(board, here, (row, column + 1)):
                return True
            if row + 1 < rows and swap_creates_match(board, here, (row + 1, column)):
                return True
    return False


def is_playable_board(board: Board) -> bool:
    return (
        len(board) == BOARD_ROWS
        and all(len(row) == BOARD_COLUMNS for row in board)
        and all(isinstance(tile, int) and 0 <= tile < TILE_TYPES for row in board for tile in row)
        and not find_matches(board)
        and has_legal_move(board)
    )


def _known_playable_board() -> Board:
    board: Board = [[(row + column) % TILE_TYPES for column in range(BOARD_COLUMNS)] for row in range(BOARD_ROWS)]
    board[0][2] = 0
    board[1][1] = 0
    return board


def generate_playable_board(rng: random.Random) -> Board:
    """Generate a full, match-free board with all tile types and a legal move."""
    for _ in range(1_000):
        board: Board = []
        for row in range(BOARD_ROWS):
            board.append([])
            for column in range(BOARD_COLUMNS):
                candidates = list(range(TILE_TYPES))
                rng.shuffle(candidates)
                for tile in candidates:
                    horizontal_match = column >= 2 and board[row][column - 1] == board[row][column - 2] == tile
                    vertical_match = row >= 2 and board[row - 1][column] == board[row - 2][column] == tile
                    if not horizontal_match and not vertical_match:
                        board[row].append(tile)
                        break
        if set(tile for row in board for tile in row) == set(range(TILE_TYPES)) and has_legal_move(board):
            return board

    fallback = _known_playable_board()
    if not is_playable_board(fallback):
        raise RuntimeError("Internal playable-board fallback is invalid.")
    return fallback


class Game:
    """Stateful game rules with no dependency on tkinter."""

    def __init__(
        self,
        *,
        rng: random.Random | None = None,
        board: Board | None = None,
        refill_tiles: Iterable[int] | None = None,
    ) -> None:
        self.rng = rng if rng is not None else random.Random()
        self._refill_iterator = iter(refill_tiles) if refill_tiles is not None else None
        self.score = 0
        if board is None:
            self.board = generate_playable_board(self.rng)
        else:
            self._validate_board(board)
            self.board = copy_board(board)

    @staticmethod
    def _validate_board(board: Board) -> None:
        if len(board) != BOARD_ROWS or any(len(row) != BOARD_COLUMNS for row in board):
            raise ValueError(f"Board must be {BOARD_ROWS} x {BOARD_COLUMNS}.")
        for row in board:
            for tile in row:
                if tile is not None and (not isinstance(tile, int) or not 0 <= tile < TILE_TYPES):
                    raise ValueError(f"Tile values must be integers from 0 to {TILE_TYPES - 1}, or None.")

    def _next_tile(self) -> int:
        if self._refill_iterator is not None:
            try:
                tile = next(self._refill_iterator)
            except StopIteration:
                self._refill_iterator = None
            else:
                if not isinstance(tile, int) or not 0 <= tile < TILE_TYPES:
                    raise ValueError(f"Refill tiles must be integers from 0 to {TILE_TYPES - 1}.")
                return tile
        return self.rng.randrange(TILE_TYPES)

    def restart(self) -> None:
        self.score = 0
        self.board = generate_playable_board(self.rng)

    def attempt_swap(
        self,
        first: Coordinate,
        second: Coordinate,
        on_resolution_step: ResolutionObserver | None = None,
    ) -> MoveResult:
        if not in_bounds(self.board, first) or not in_bounds(self.board, second):
            return MoveResult(False, "invalid_selection")
        if not are_adjacent(first, second):
            return MoveResult(False, "not_adjacent")

        _swap(self.board, first, second)
        matches = find_matches(self.board)
        if not matches or (first not in matches and second not in matches):
            _swap(self.board, first, second)
            return MoveResult(False, "no_match")

        cleared, cascades = self._resolve_cascades(matches, on_resolution_step)
        regenerated = self.ensure_playable()
        return MoveResult(True, "accepted", cleared, cascades, regenerated)

    def _resolve_cascades(
        self,
        matches: set[Coordinate] | None = None,
        on_resolution_step: ResolutionObserver | None = None,
    ) -> tuple[int, int]:
        total_cleared = 0
        cascade_steps = 0
        current_matches = find_matches(self.board) if matches is None else matches
        while current_matches:
            cascade_steps += 1
            total_cleared += len(current_matches)
            self.score += len(current_matches) * POINTS_PER_TILE
            for row, column in current_matches:
                self.board[row][column] = None
            self._apply_gravity_and_refill()
            if on_resolution_step is not None:
                on_resolution_step(cascade_steps, len(current_matches))
            current_matches = find_matches(self.board)
        return total_cleared, cascade_steps

    def _apply_gravity_and_refill(self) -> None:
        for column in range(BOARD_COLUMNS):
            remaining = [self.board[row][column] for row in range(BOARD_ROWS) if self.board[row][column] is not None]
            empty_count = BOARD_ROWS - len(remaining)
            new_column = [self._next_tile() for _ in range(empty_count)] + remaining
            for row, tile in enumerate(new_column):
                self.board[row][column] = tile

    def ensure_playable(self) -> bool:
        """Regenerate a stable dead board, preserving score. Return whether recovery occurred."""
        if is_playable_board(self.board):
            return False
        if find_matches(self.board) or any(tile is None for row in self.board for tile in row):
            raise ValueError("Dead-board recovery requires a full, stable board.")
        self.board = generate_playable_board(self.rng)
        return True
