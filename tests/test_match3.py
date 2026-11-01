from __future__ import annotations

import random
import time
import unittest

from match3 import (
    BOARD_COLUMNS,
    BOARD_ROWS,
    POINTS_PER_TILE,
    TILE_TYPES,
    Game,
    copy_board,
    find_matches,
    generate_playable_board,
    has_legal_move,
    is_playable_board,
    swap_creates_match,
)


def controlled_board() -> list[list[int]]:
    board = [[(row + column) % TILE_TYPES for column in range(BOARD_COLUMNS)] for row in range(BOARD_ROWS)]
    board[0][2] = 0
    board[1][1] = 0
    return board


def dead_board() -> list[list[int]]:
    return [[(row + column) % TILE_TYPES for column in range(BOARD_COLUMNS)] for row in range(BOARD_ROWS)]


class MatchDetectionTests(unittest.TestCase):
    def test_run_of_four_is_included_in_full(self) -> None:
        board = dead_board()
        for column in range(1, 5):
            board[2][column] = 5
        self.assertEqual(find_matches(board), {(2, column) for column in range(1, 5)})

    def test_simultaneous_disjoint_horizontal_and_vertical_matches(self) -> None:
        board = dead_board()
        for column in range(3):
            board[1][column] = 5
        for row in range(4, 7):
            board[row][6] = 2
        expected = {(1, column) for column in range(3)} | {(row, 6) for row in range(4, 7)}
        self.assertEqual(find_matches(board), expected)

    def test_horizontal_vertical_long_and_intersecting_matches_are_unioned(self) -> None:
        board = [[(row + column) % TILE_TYPES for column in range(BOARD_COLUMNS)] for row in range(BOARD_ROWS)]
        for column in range(1, 6):
            board[3][column] = 5
        for row in range(1, 6):
            board[row][3] = 5

        expected = {(3, column) for column in range(1, 6)} | {(row, 3) for row in range(1, 6)}
        self.assertEqual(find_matches(board), expected)
        self.assertEqual(len(find_matches(board)), 9)

    def test_none_cells_do_not_form_matches(self) -> None:
        board = controlled_board()
        board[0][0:3] = [None, None, None]
        self.assertEqual(find_matches(board), set())


class BoardGenerationTests(unittest.TestCase):
    def test_seeded_generation_is_reproducible_and_playable(self) -> None:
        first = generate_playable_board(random.Random(12345))
        second = generate_playable_board(random.Random(12345))
        self.assertEqual(first, second)
        self.assertTrue(is_playable_board(first))
        self.assertEqual({tile for row in first for tile in row}, set(range(TILE_TYPES)))

    def test_one_hundred_initial_boards_are_valid_within_two_seconds(self) -> None:
        started = time.perf_counter()
        for seed in range(100):
            board = generate_playable_board(random.Random(seed))
            self.assertTrue(is_playable_board(board), f"invalid board for seed {seed}")
        self.assertLess(time.perf_counter() - started, 2.0)

    def test_is_playable_board_classifies_valid_incomplete_matched_and_dead_boards(self) -> None:
        valid_board = controlled_board()
        incomplete_board = copy_board(valid_board)
        incomplete_board[7][7] = None
        matched_board = dead_board()
        matched_board[0][0:3] = [5, 5, 5]

        cases = (
            ("valid", valid_board, True, 0, set(), True),
            ("incomplete", incomplete_board, False, 1, set(), False),
            ("matched", matched_board, False, 0, {(0, 0), (0, 1), (0, 2)}, None),
            ("dead", dead_board(), False, 0, set(), False),
        )

        for name, board, expected, empty_count, expected_matches, expected_legal_move in cases:
            with self.subTest(case=name):
                self.assertEqual(len(board), BOARD_ROWS)
                self.assertTrue(all(len(row) == BOARD_COLUMNS for row in board))
                self.assertEqual(sum(tile is None for row in board for tile in row), empty_count)
                self.assertEqual(find_matches(board), expected_matches)
                if expected_legal_move is not None:
                    self.assertIs(has_legal_move(board), expected_legal_move)
                self.assertIs(is_playable_board(board), expected)


class MoveTests(unittest.TestCase):
    def test_diagonal_nonadjacent_and_out_of_bounds_selections_do_not_change_state(self) -> None:
        game = Game(board=controlled_board(), rng=random.Random(1))
        cases = (
            ((0, 0), (0, 0), "not_adjacent"),
            ((0, 0), (1, 1), "not_adjacent"),
            ((0, 0), (0, 3), "not_adjacent"),
            ((0, 0), (-1, 0), "invalid_selection"),
            ((0, 0), (BOARD_ROWS, 0), "invalid_selection"),
            ((0, 0), (0, BOARD_COLUMNS), "invalid_selection"),
            ((-1, 0), (0, 0), "invalid_selection"),
            ((BOARD_ROWS, 0), (0, 0), "invalid_selection"),
        )
        for first, second, expected_reason in cases:
            with self.subTest(first=first, second=second):
                before = copy_board(game.board)
                score = game.score

                result = game.attempt_swap(first, second)

                self.assertFalse(result.accepted)
                self.assertEqual(result.reason, expected_reason)
                self.assertEqual(game.board, before)
                self.assertEqual(game.score, score)

    def test_adjacent_matchless_swap_is_reversed_without_score(self) -> None:
        game = Game(board=controlled_board(), rng=random.Random(2))
        first, second = (7, 6), (7, 7)
        self.assertFalse(swap_creates_match(game.board, first, second))
        before = copy_board(game.board)

        result = game.attempt_swap(first, second)

        self.assertFalse(result.accepted)
        self.assertEqual(result.reason, "no_match")
        self.assertEqual(game.board, before)
        self.assertEqual(game.score, 0)

    def test_valid_swap_clears_three_and_scores_exactly(self) -> None:
        game = Game(board=controlled_board(), refill_tiles=[4, 5, 4], rng=random.Random(3))

        result = game.attempt_swap((0, 1), (1, 1))

        self.assertTrue(result.accepted)
        self.assertEqual(result.cleared_tiles, 3)
        self.assertEqual(result.cascades, 1)
        self.assertEqual(game.score, 3 * POINTS_PER_TILE)
        self.assertTrue(is_playable_board(game.board))

    def test_horizontal_corner_swap_creates_vertical_match_and_scores_exactly(self) -> None:
        board = dead_board()
        board[0][0] = 1
        board[0][1] = 0
        board[1][0] = 0
        board[2][0] = 0
        game = Game(board=board, refill_tiles=[4, 5, 4], rng=random.Random(10))

        result = game.attempt_swap((0, 0), (0, 1))

        self.assertTrue(result.accepted)
        self.assertEqual(result.reason, "accepted")
        self.assertEqual(result.cleared_tiles, 3)
        self.assertEqual(result.cascades, 1)
        self.assertEqual(game.score, 3 * POINTS_PER_TILE)
        self.assertTrue(is_playable_board(game.board))

    def test_resolution_replaces_only_matched_top_cells(self) -> None:
        board = dead_board()
        board[0][0:3] = [5, 5, 5]
        before = copy_board(board)
        matched = {(0, 0), (0, 1), (0, 2)}
        game = Game(board=board, refill_tiles=[1, 2, 3], rng=random.Random(11))

        cleared, cascades = game._resolve_cascades()

        self.assertEqual((cleared, cascades), (3, 1))
        self.assertEqual(game.board[0][0:3], [1, 2, 3])
        for row in range(BOARD_ROWS):
            for column in range(BOARD_COLUMNS):
                if (row, column) not in matched:
                    self.assertEqual(game.board[row][column], before[row][column])

    def test_fully_empty_column_uses_controlled_refill_order(self) -> None:
        board = controlled_board()
        refill_column = 4
        expected_other_columns = [
            [board[row][column] for row in range(BOARD_ROWS)]
            for column in range(BOARD_COLUMNS)
            if column != refill_column
        ]
        for row in range(BOARD_ROWS):
            board[row][refill_column] = None
        refill_tiles = [5, 4, 3, 2, 1, 0, 5, 4]
        game = Game(board=board, refill_tiles=refill_tiles, rng=random.Random(12))

        game._apply_gravity_and_refill()

        self.assertEqual([game.board[row][refill_column] for row in range(BOARD_ROWS)], refill_tiles)
        actual_other_columns = [
            [game.board[row][column] for row in range(BOARD_ROWS)]
            for column in range(BOARD_COLUMNS)
            if column != refill_column
        ]
        self.assertEqual(actual_other_columns, expected_other_columns)

    def test_intersecting_match_scores_each_distinct_tile_once(self) -> None:
        board = dead_board()
        for column in range(1, 6):
            board[3][column] = 5
        for row in range(1, 6):
            board[row][3] = 5
        refill_tiles = [0, 1, 2, 3, 4, 0, 1, 2, 3]
        game = Game(board=board, refill_tiles=refill_tiles, rng=random.Random(13))

        cleared, cascades = game._resolve_cascades()

        self.assertEqual((cleared, cascades), (9, 1))
        self.assertEqual(game.score, 9 * POINTS_PER_TILE)
        self.assertFalse(find_matches(game.board))

    def test_cascade_scores_every_distinct_tile_without_multiplier(self) -> None:
        game = Game(board=controlled_board(), refill_tiles=[4, 4, 4, 1, 2, 3], rng=random.Random(4))
        observed: list[tuple[int, int, int]] = []

        result = game.attempt_swap(
            (0, 1),
            (1, 1),
            lambda step, cleared: observed.append((step, cleared, game.score)),
        )

        self.assertTrue(result.accepted)
        self.assertEqual(result.cleared_tiles, 6)
        self.assertEqual(result.cascades, 2)
        self.assertEqual(game.score, 6 * POINTS_PER_TILE)
        self.assertEqual(observed, [(1, 3, 30), (2, 3, 60)])
        self.assertFalse(find_matches(game.board))

    def test_two_step_cascade_finishes_on_full_playable_board(self) -> None:
        game = Game(board=controlled_board(), refill_tiles=[4, 4, 4, 1, 2, 3], rng=random.Random(14))

        result = game.attempt_swap((0, 1), (1, 1))

        self.assertTrue(result.accepted)
        self.assertEqual(result.cascades, 2)
        self.assertTrue(all(tile is not None for row in game.board for tile in row))
        self.assertEqual(find_matches(game.board), set())
        self.assertTrue(has_legal_move(game.board))
        self.assertTrue(is_playable_board(game.board))

    def test_gravity_compacts_tiles_down_and_preserves_their_order(self) -> None:
        board = controlled_board()
        original_column = [board[row][0] for row in range(BOARD_ROWS)]
        board[2][0] = None
        board[5][0] = None
        game = Game(board=board, refill_tiles=[4, 5], rng=random.Random(9))

        game._apply_gravity_and_refill()

        expected_remaining = [tile for index, tile in enumerate(original_column) if index not in (2, 5)]
        self.assertEqual([game.board[row][0] for row in range(BOARD_ROWS)], [4, 5] + expected_remaining)
        self.assertTrue(all(tile is not None for row in game.board for tile in row))

    def test_ten_step_cascade_finishes_within_two_seconds(self) -> None:
        refills = [tile for _ in range(9) for tile in (4, 4, 4)] + [1, 2, 3]
        game = Game(board=controlled_board(), refill_tiles=refills, rng=random.Random(5))
        started = time.perf_counter()

        result = game.attempt_swap((0, 1), (1, 1))

        self.assertLess(time.perf_counter() - started, 2.0)
        self.assertEqual(result.cascades, 10)
        self.assertEqual(result.cleared_tiles, 30)
        self.assertEqual(game.score, 300)


class SessionTests(unittest.TestCase):
    def test_dead_board_recovery_preserves_score_and_returns_playable_board(self) -> None:
        board = dead_board()
        self.assertFalse(find_matches(board))
        self.assertFalse(has_legal_move(board))
        game = Game(board=board, rng=random.Random(7))
        game.score = 80

        started = time.perf_counter()
        recovered = game.ensure_playable()

        self.assertLess(time.perf_counter() - started, 2.0)
        self.assertTrue(recovered)
        self.assertEqual(game.score, 80)
        self.assertTrue(is_playable_board(game.board))

    def test_ten_dead_board_recoveries_each_finish_within_two_seconds(self) -> None:
        for seed in range(10):
            game = Game(board=dead_board(), rng=random.Random(seed))
            started = time.perf_counter()
            game.ensure_playable()
            self.assertLess(time.perf_counter() - started, 2.0)
            self.assertTrue(is_playable_board(game.board))

    def test_restart_resets_score_and_creates_valid_board(self) -> None:
        game = Game(rng=random.Random(8))
        game.score = 120
        game.board = dead_board()

        game.restart()

        self.assertEqual(game.score, 0)
        self.assertTrue(is_playable_board(game.board))

    def test_board_dimensions_and_tile_count_constants(self) -> None:
        self.assertEqual((BOARD_ROWS, BOARD_COLUMNS, TILE_TYPES), (8, 8, 6))


if __name__ == "__main__":
    unittest.main()
