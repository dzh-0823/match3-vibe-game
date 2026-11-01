"""Tkinter entry point for the match-3 prototype."""

from __future__ import annotations

import sys
import tkinter as tk
from tkinter import messagebox

from high_scores import (
    HighScoreError,
    HighScoreService,
    HighScoreStore,
    default_high_score_path,
)
from match3 import BOARD_COLUMNS, BOARD_ROWS, Game


TILE_STYLES = (
    ("A", "#e74c3c"),
    ("B", "#3498db"),
    ("C", "#2ecc71"),
    ("D", "#f1c40f"),
    ("E", "#9b59b6"),
    ("F", "#e67e22"),
)


def format_leaderboard(scores: tuple[int, ...]) -> str:
    if not scores:
        return "Top scores: No completed games yet."
    ranked_scores = "  |  ".join(f"{rank}. {score}" for rank, score in enumerate(scores, start=1))
    return f"Top scores: {ranked_scores}"


class Match3App:
    """Small desktop view/controller; all game rules live in ``match3``."""

    def __init__(self, root: tk.Tk, high_scores: HighScoreService) -> None:
        self.root = root
        self.game = Game()
        self.high_scores = high_scores
        self.selected: tuple[int, int] | None = None
        self.busy = False

        root.title("Match-3 Game")
        root.resizable(False, False)
        root.configure(bg="#20252b")
        root.protocol("WM_DELETE_WINDOW", self.close)

        header = tk.Frame(root, bg="#20252b", padx=12, pady=10)
        header.pack(fill="x")
        self.score_var = tk.StringVar()
        tk.Label(
            header,
            textvariable=self.score_var,
            font=("TkDefaultFont", 16, "bold"),
            fg="white",
            bg="#20252b",
        ).pack(side="left")
        self.restart_button = tk.Button(
            header,
            text="Restart",
            command=self.restart,
            font=("TkDefaultFont", 11, "bold"),
            padx=12,
        )
        self.restart_button.pack(side="right")

        self.high_scores_var = tk.StringVar()
        tk.Label(
            root,
            textvariable=self.high_scores_var,
            font=("TkDefaultFont", 10, "bold"),
            fg="#d8dee9",
            bg="#20252b",
            anchor="w",
            width=48,
            padx=12,
            pady=2,
        ).pack(fill="x")
        startup_warning = self._load_high_scores()

        self.board_frame = tk.Frame(root, bg="#11151a", padx=6, pady=6)
        self.board_frame.pack(padx=12)
        self.buttons: list[list[tk.Button]] = []
        for row in range(BOARD_ROWS):
            button_row: list[tk.Button] = []
            for column in range(BOARD_COLUMNS):
                button = tk.Button(
                    self.board_frame,
                    width=4,
                    height=2,
                    font=("TkDefaultFont", 15, "bold"),
                    command=lambda r=row, c=column: self.on_tile_click(r, c),
                    bd=2,
                    relief="raised",
                    takefocus=False,
                )
                button.grid(row=row, column=column, padx=2, pady=2)
                button_row.append(button)
            self.buttons.append(button_row)

        self.status_var = tk.StringVar(value=startup_warning or "Select two adjacent tiles.")
        self.status_label = tk.Label(
            root,
            textvariable=self.status_var,
            font=("TkDefaultFont", 10),
            fg="#d8dee9",
            bg="#20252b",
            anchor="w",
            width=48,
            pady=10,
        )
        self.status_label.pack(padx=12, fill="x")
        self.render()

    def render(self) -> None:
        self.score_var.set(f"Score: {self.game.score}")
        for row in range(BOARD_ROWS):
            for column in range(BOARD_COLUMNS):
                tile = self.game.board[row][column]
                if tile is None:
                    continue
                symbol, color = TILE_STYLES[tile]
                selected = self.selected == (row, column)
                self.buttons[row][column].configure(
                    text=symbol,
                    bg=color,
                    activebackground=color,
                    fg="#111111",
                    activeforeground="#111111",
                    relief="sunken" if selected else "raised",
                    bd=5 if selected else 2,
                    state="disabled" if self.busy else "normal",
                )

    def on_tile_click(self, row: int, column: int) -> None:
        if self.busy:
            return
        coordinate = (row, column)
        if self.selected is None:
            self.selected = coordinate
            self.status_var.set("Tile selected. Choose an orthogonally adjacent tile.")
            self.status_label.configure(fg="#d8dee9")
            self.render()
            return

        first = self.selected
        self.selected = None
        self._set_busy(True)
        try:
            result = self.game.attempt_swap(first, coordinate, self._show_resolution_step)
            if result.accepted:
                recovery = " The board was regenerated because no moves remained." if result.reshuffled else ""
                self.status_var.set(
                    f"Move accepted: {result.cleared_tiles} tiles cleared "
                    f"in {result.cascades} step(s).{recovery}"
                )
                self.status_label.configure(fg="#b7f7c4")
            elif result.reason == "not_adjacent":
                self.status_var.set("Rejected: tiles must be orthogonally adjacent.")
                self.status_label.configure(fg="#ffb3b3")
            elif result.reason == "no_match":
                self.status_var.set("Rejected: that swap creates no match.")
                self.status_label.configure(fg="#ffb3b3")
            else:
                self.status_var.set("Rejected: invalid tile selection.")
                self.status_label.configure(fg="#ffb3b3")
        finally:
            self._set_busy(False)

    def restart(self) -> None:
        if self.busy:
            return
        self.selected = None
        self._set_busy(True)
        try:
            save_message, save_failed = self._complete_current_game()
            self.game.restart()
            prefix = f"{save_message} " if save_message else ""
            self.status_var.set(f"{prefix}New game started. Select two adjacent tiles.")
            self.status_label.configure(fg="#ffb3b3" if save_failed else "#d8dee9")
        finally:
            self._set_busy(False)

    def close(self) -> None:
        _, save_failed = self._complete_current_game()
        if save_failed:
            messagebox.showwarning(
                "High-score warning",
                "The current score could not be saved. The game will still close normally.",
                parent=self.root,
            )
        self.root.destroy()

    def _load_high_scores(self) -> str | None:
        try:
            scores = self.high_scores.load()
        except HighScoreError:
            self.high_scores_var.set("Top scores: unavailable")
            return "High scores could not be loaded. Play can continue."
        self.high_scores_var.set(format_leaderboard(scores))
        return None

    def _complete_current_game(self) -> tuple[str, bool]:
        score = self.game.score
        try:
            result = self.high_scores.complete_game(score)
        except HighScoreError:
            return "High score could not be saved.", True
        self.high_scores_var.set(format_leaderboard(result.scores))
        if result.saved:
            return f"Saved {score} points to the leaderboard.", False
        return "", False

    def _show_resolution_step(self, step: int, cleared: int) -> None:
        self.status_var.set(f"Resolving step {step}: {cleared} tiles cleared.")
        self.status_label.configure(fg="#d8dee9")
        self.render()
        self.root.update_idletasks()

    def _set_busy(self, busy: bool) -> None:
        self.busy = busy
        self.restart_button.configure(state="disabled" if busy else "normal")
        self.render()
        self.root.update_idletasks()


def main() -> int:
    if sys.version_info[:2] < (3, 14):
        message = (
            "This prototype requires Python 3.14 or newer. "
            f"Detected {sys.version_info.major}.{sys.version_info.minor}."
        )
        print(message, file=sys.stderr)
        return 1

    root = tk.Tk()
    try:
        high_scores = HighScoreService(HighScoreStore(default_high_score_path()))
        Match3App(root, high_scores)
    except tk.TclError as exc:
        messagebox.showerror("Match-3 startup error", str(exc), parent=root)
        root.destroy()
        return 1
    root.mainloop()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
