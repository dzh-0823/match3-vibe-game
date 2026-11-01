# Match-3 First Prototype

An offline desktop match-3 prototype for Windows, implemented with Python 3.14 and the standard-library `tkinter` GUI. It has an 8 x 8 board, six color-and-letter tile types, endless play, scoring, restart, cascades, and automatic dead-board recovery. It creates no saves, settings, accounts, or network traffic.

## Requirements

- Windows 11 (the verified reference desktop environment)
- Python 3.14 with `tkinter`
- No third-party packages

## Run

From the project root in PowerShell:

```powershell
.\.venv\Scripts\python.exe main.py
```

Select one tile, then select an orthogonally adjacent tile. A swap is accepted only if it creates a horizontal or vertical run of at least three. Rejected swaps leave the board and score unchanged. Every distinct cleared tile is worth 10 points, including cascade tiles. Use **Restart** to reset the score and generate a new playable board.

## Test

From the project root in PowerShell:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Syntax-check every Python file without opening the GUI:

```powershell
.\.venv\Scripts\python.exe -m compileall -q main.py match3.py tests
```

The core rules are in `match3.py` and do not import `tkinter`, so the automated suite does not open a window. `main.py` contains only the desktop view/controller and application entry point.
