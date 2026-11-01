from __future__ import annotations

import random
import unittest

from match3 import (
    BOARD_COLUMNS,
    BOARD_ROWS,
    POINTS_PER_TILE,
    TILE_TYPES,
    Game,
    copy_board,
    find_matches,
    has_legal_move,
    is_playable_board,
)


def controlled_board() -> list[list[int]]:
    board = [[(row + column) % TILE_TYPES for column in range(BOARD_COLUMNS)] for row in range(BOARD_ROWS)]
    board[0][2] = 0
    board[1][1] = 0
    return board


def dead_board() -> list[list[int]]:
    return [[(row + column) % TILE_TYPES for column in range(BOARD_COLUMNS)] for row in range(BOARD_ROWS)]


class GameScenarioTests(unittest.TestCase):
    def test_seeded_new_game_completes_first_move_and_reports_resolution_steps(self) -> None:
        game = Game(rng=random.Random(12345))
        observed_steps: list[tuple[int, int, int]] = []
        self.assertEqual(game.score, 0)
        self.assertTrue(is_playable_board(game.board))

        result = game.attempt_swap(
            (0, 3),
            (1, 3),
            lambda step, cleared: observed_steps.append((step, cleared, game.score)),
        )

        self.assertTrue(result.accepted)
        self.assertEqual((result.cleared_tiles, result.cascades), (9, 2))
        self.assertFalse(result.reshuffled)
        self.assertEqual(observed_steps, [(1, 3, 30), (2, 6, 90)])
        self.assertEqual(game.score, 9 * POINTS_PER_TILE)
        self.assertTrue(all(tile is not None for row in game.board for tile in row))
        self.assertEqual(find_matches(game.board), set())
        self.assertTrue(has_legal_move(game.board))
        self.assertTrue(is_playable_board(game.board))

    def test_rejected_move_leaves_session_usable_for_next_valid_move(self) -> None:
        game = Game(board=controlled_board(), refill_tiles=[4, 5, 4], rng=random.Random(21))
        original_board = copy_board(game.board)
        observed_steps: list[tuple[int, int, int]] = []

        rejected = game.attempt_swap(
            (7, 6),
            (7, 7),
            lambda step, cleared: observed_steps.append((step, cleared, game.score)),
        )

        self.assertFalse(rejected.accepted)
        self.assertEqual(rejected.reason, "no_match")
        self.assertEqual(game.board, original_board)
        self.assertEqual(game.score, 0)
        self.assertEqual(observed_steps, [])

        accepted = game.attempt_swap(
            (0, 1),
            (1, 1),
            lambda step, cleared: observed_steps.append((step, cleared, game.score)),
        )

        self.assertTrue(accepted.accepted)
        self.assertEqual(game.score, 3 * POINTS_PER_TILE)
        self.assertEqual(observed_steps, [(1, 3, 30)])
        self.assertNotEqual(game.board, original_board)
        self.assertTrue(is_playable_board(game.board))

    def test_two_valid_moves_accumulate_score_on_updated_board(self) -> None:
        game = Game(board=controlled_board(), refill_tiles=[4, 5, 4], rng=random.Random(50))

        first = game.attempt_swap((0, 1), (1, 1))
        board_after_first = copy_board(game.board)

        self.assertTrue(first.accepted)
        self.assertEqual((first.cleared_tiles, first.cascades), (3, 1))
        self.assertEqual(game.score, 3 * POINTS_PER_TILE)
        self.assertTrue(is_playable_board(game.board))

        second = game.attempt_swap((0, 3), (1, 3))

        self.assertTrue(second.accepted)
        self.assertEqual((second.cleared_tiles, second.cascades), (3, 1))
        self.assertFalse(second.reshuffled)
        self.assertEqual(game.score, 6 * POINTS_PER_TILE)
        self.assertNotEqual(game.board, board_after_first)
        self.assertTrue(is_playable_board(game.board))

    def test_valid_move_triggers_automatic_dead_board_recovery(self) -> None:
        board = dead_board()
        board[0][0:4] = [2, 0, 2, 2]
        self.assertEqual(find_matches(board), set())
        self.assertTrue(has_legal_move(board))
        game = Game(board=board, refill_tiles=[1, 2, 3], rng=random.Random(77))
        observed_steps: list[tuple[int, int, int, list[list[int | None]]]] = []

        result = game.attempt_swap(
            (0, 0),
            (0, 1),
            lambda step, cleared: observed_steps.append((step, cleared, game.score, copy_board(game.board))),
        )

        expected_dead_board = dead_board()
        self.assertEqual(observed_steps, [(1, 3, 30, expected_dead_board)])
        self.assertTrue(result.accepted)
        self.assertEqual((result.cleared_tiles, result.cascades), (3, 1))
        self.assertTrue(result.reshuffled)
        self.assertEqual(game.score, 3 * POINTS_PER_TILE)
        self.assertNotEqual(game.board, expected_dead_board)
        self.assertTrue(is_playable_board(game.board))

        next_move = game.attempt_swap((0, 6), (1, 6))

        self.assertTrue(next_move.accepted)
        self.assertEqual((next_move.cleared_tiles, next_move.cascades), (3, 1))
        self.assertFalse(next_move.reshuffled)
        self.assertEqual(game.score, 6 * POINTS_PER_TILE)
        self.assertTrue(is_playable_board(game.board))


if __name__ == "__main__":
    unittest.main()
