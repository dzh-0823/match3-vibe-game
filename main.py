"""Tkinter entry point for the match-3 prototype."""

from __future__ import annotations

import sys
import tkinter as tk
from tkinter import messagebox

from match3 import BOARD_COLUMNS, BOARD_ROWS, Game


TILE_STYLES = (
    ("A", "#e74c3c"),
    ("B", "#3498db"),
    ("C", "#2ecc71"),
    ("D", "#f1c40f"),
    ("E", "#9b59b6"),
    ("F", "#e67e22"),
)


class Match3App:
    """Small desktop view/controller; all game rules live in ``match3``."""

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.game = Game()
        self.selected: tuple[int, int] | None = None
        self.busy = False

        root.title("Match-3 Prototype")
        root.resizable(False, False)
        root.configure(bg="#20252b")

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

        self.status_var = tk.StringVar(value="Select two adjacent tiles.")
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
            self.game.restart()
            self.status_var.set("New game started. Select two adjacent tiles.")
            self.status_label.configure(fg="#d8dee9")
        finally:
            self._set_busy(False)

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
    if sys.version_info[:2] != (3, 13):
        message = (
            "This prototype requires Python 3.13. "
            f"Detected {sys.version_info.major}.{sys.version_info.minor}."
        )
        print(message, file=sys.stderr)
        return 1

    root = tk.Tk()
    try:
        Match3App(root)
    except tk.TclError as exc:
        messagebox.showerror("Match-3 startup error", str(exc), parent=root)
        root.destroy()
        return 1
    root.mainloop()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
