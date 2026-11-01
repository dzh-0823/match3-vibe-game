# Match-3 Game with Persistent High Scores

An offline desktop match-3 game for Windows, implemented with Python 3.14 and the standard-library `tkinter` GUI. It has an 8 x 8 board, six color-and-letter tile types, endless play, scoring, restart, cascades, automatic dead-board recovery, and a persistent top-five leaderboard. It requires no account, server, network connection, or third-party package.

## Requirements

- Windows 11 (the verified reference desktop environment)
- Python 3.14 with `tkinter`
- No third-party packages

## Run

From the project root in PowerShell:

```powershell
.\.venv\Scripts\python.exe main.py
```

Select one tile, then select an orthogonally adjacent tile. A swap is accepted only if it creates a horizontal or vertical run of at least three. Rejected swaps leave the board and score unchanged. Every distinct cleared tile is worth 10 points, including cascade tiles.

The top five completed positive-score games are shown when the application starts. A game is completed when the player chooses **Restart** or closes the window normally. The completed score is saved before Restart creates a fresh playable board; zero-point games are not added. Duplicate scores are retained and the leaderboard is sorted from highest to lowest.

## High-score data

On Windows, scores are stored as versioned JSON at:

```text
%LOCALAPPDATA%\Match3VibeGame\high_scores.json
```

The file is created only after the first positive-score game is completed. Updates use a temporary file and atomic replacement. A missing file is treated as an empty leaderboard. Malformed data does not stop gameplay and is replaced by valid data after the next completed positive-score game. Other read or write failures are reported to the player without breaking the current game.

## Test

From the project root in PowerShell:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Syntax-check every Python file without opening the GUI:

```powershell
.\.venv\Scripts\python.exe -m compileall -q main.py match3.py high_scores.py tests
```

The core rules remain in `match3.py`. The GUI-independent high-score store and session policy are in `high_scores.py`, and `main.py` contains the desktop view/controller plus the application entry point. The standard automated suite does not open a window.
