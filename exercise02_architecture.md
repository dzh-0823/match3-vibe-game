# Exercise 2: Software Architecture

## TODO 1: Core Responsibilities

### Responsibility Overview

| Responsibility | Purpose | Owns | Must Not Own | GUI-independent | Requirement IDs |
| --- | --- | --- | --- | --- | --- |
| Board and tile management | Maintain the board and tile data used by the game. | Board content; board dimensions and tile identities; board mutation primitives; validation and tile supply; the invariant that every stable state waiting for input is full, match-free, and has at least one legal move. The invariant is not required during resolution. | The decision to replace the current board, selection state, swap legality, scoring, or presentation. | Yes | FR-01, FR-11, DR-04 |
| Move and rule processing | Evaluate a requested exchange. | Bounds and orthogonal-adjacency decisions; whether one exchange creates a match; matchless-swap rejection. | The selected tile or selection transitions, board content or its playable invariant, match scanning, score, or feedback text. | Yes | FR-02, FR-03, FR-04, DR-01 |
| Match detection | Identify every current horizontal and vertical run of at least three identical tiles. | The union of matched coordinates, including complete long and simultaneous runs with intersecting coordinates represented once. | Clearing cells, applying gravity, refilling, scoring, or UI feedback. | Yes | FR-05, DR-02 |
| Removal, refill, and cascading | Resolve all matches in the required order until the board is stable. | Simultaneous removal; downward gravity; refill; repeated detection; cascade completion and per-step cleared-cell results. | Initial swap legality, the scoring formula or score total, board replacement after a dead board, or rendering. | Yes | FR-05, FR-06, DR-03 |
| Scoring | Define the points produced by a resolution step. | The rule of exactly 10 points per distinct cleared tile, including cascades and excluding multipliers or bonuses; calculation of the score increment. | The accumulated score total, restart reset, recovery preservation, match membership, or score display. | Yes | FR-07, DR-06 |
| Game-state coordination | Coordinate the session and the state-machine workflow. | First/second selection rules and the selected tile; sequencing of move validation and resolution; the accumulated score total; score reset on restart and preservation during recovery; readiness decisions; when a new board replaces the current one; dead-board recovery; result reporting. | Board content and invariant evaluation, the scoring formula, match detection, input-event capture, the input lock, or rendering. | Yes | UR-02, UR-04, UR-05, FR-07, FR-08, FR-10, DR-04, DR-05 |
| User input | Translate desktop actions into GUI-independent coordination requests. | Mouse-click and Restart-event translation. **ASSUMPTION:** one move is resolved in one synchronous core call, so User input owns the input lock needed while the GUI presents resolution steps; the lock prevents another click from changing the board before coordination returns to a stable waiting state. | The selected tile, selection rules, swap legality, board content, score, or status wording. | No | UR-01, FR-02, FR-06 |
| Presentation | Show the current game and action outcomes. | Tile colors and symbols; selected-tile highlighting; board and score rendering; accepted, rejected, resolution, and recovery feedback; control appearance. | Selection state, domain equality, swap legality, matching, board mutation, score calculation, or recovery decisions. | No | UR-03, UR-04, FR-07, FR-09, NFR-01 |

### Responsibility Boundaries

Board and tile management is the sole owner of board content and invariant evaluation. Game-state coordination decides when initialization, restart, or recovery replaces that content. The playable-board invariant applies whenever the game is stable and waiting for input; temporary empty cells and matches are permitted during resolution.

Game-state coordination owns session state: the selected coordinate, selection transitions, score total, and move lifecycle. Move and rule processing makes stateless legality decisions. Scoring produces a score increment but does not store the total. This keeps selection and scoring testable without a GUI.

Match detection only identifies coordinates. Removal, refill, and cascading consumes that result and controls resolution order. Presentation observes results but does not make domain decisions. User input translates events and, under the stated assumption, owns the input lock rather than the selected tile.

### Cross-cutting constraints

- **GUI-independent testability and deterministic verification:** core responsibilities must be exercisable without opening a window, with controlled state or randomness. IDs: UR-07, FR-11, NFR-07.
- **Performance and reliability:** input feedback, generation, recovery, cascade processing, and controlled robustness must meet their validated limits. IDs: UR-09, NFR-02, NFR-03. NFR-04 is deferred (Won't have for this prototype).
- **Maintainability and core/GUI separation:** responsibilities must remain understandable and avoid duplicating central gameplay values. IDs: UR-08 and NFR-05, both deferred (Should have).
- **Documentation and scope control:** the supported environment, commands, dependencies, rules, and design decisions must be documented without adding out-of-scope product features. IDs: NFR-06, NFR-08.
- **Local runtime, offline operation, host integrity, and shutdown:** the architecture must run locally without accounts, services, elevated privileges, or persistent game data and must close cleanly. IDs: UR-06, NFR-09, NFR-10, NFR-12, NFR-13. NFR-11 is deferred (Could have).
- **Concrete TODO 6 delivery constraints:** Python 3.13, standard-library tkinter, and no third-party packages are the documented realization of NFR-06, NFR-09, and NFR-10.

### Requirement Traceability

This list covers the 39 formal requirements in TODO 3. NEED identifiers are stakeholder-need sources rather than requirements.

- UR-01 → User input; Game-state coordination.
- UR-02 → Game-state coordination.
- UR-03 → Presentation.
- UR-04 → Game-state coordination; Presentation.
- UR-05 → Game-state coordination.
- UR-06 → Cross-cutting: local runtime, offline operation, host integrity, and shutdown.
- UR-07 → Cross-cutting: GUI-independent testability and deterministic verification.
- UR-08 → Cross-cutting: maintainability and core/GUI separation — **deferred (Should have)**.
- UR-09 → Cross-cutting: performance and reliability.
- FR-01 → Board and tile management.
- FR-02 → User input; Game-state coordination; Move and rule processing.
- FR-03 → Move and rule processing; Game-state coordination.
- FR-04 → Move and rule processing; Game-state coordination.
- FR-05 → Match detection; Removal, refill, and cascading.
- FR-06 → Removal, refill, and cascading; User input.
- FR-07 → Scoring; Game-state coordination; Presentation.
- FR-08 → Game-state coordination; Board and tile management.
- FR-09 → Presentation.
- FR-10 → Game-state coordination.
- FR-11 → Cross-cutting: GUI-independent testability and deterministic verification.
- NFR-01 → Presentation.
- NFR-02 → Cross-cutting: performance and reliability.
- NFR-03 → Cross-cutting: performance and reliability.
- NFR-04 → Cross-cutting: performance and reliability — **deferred (Won't have for this prototype)**.
- NFR-05 → Cross-cutting: maintainability and core/GUI separation — **deferred (Should have)**.
- NFR-06 → Cross-cutting: documentation and scope control; local runtime.
- NFR-07 → Cross-cutting: GUI-independent testability and deterministic verification.
- NFR-08 → Cross-cutting: documentation and scope control.
- NFR-09 → Cross-cutting: local runtime, offline operation, host integrity, and shutdown.
- NFR-10 → Cross-cutting: local runtime, offline operation, host integrity, and shutdown.
- NFR-11 → Cross-cutting: local runtime diagnostics — **deferred (Could have)**.
- NFR-12 → Cross-cutting: local runtime, offline operation, host integrity, and shutdown.
- NFR-13 → Cross-cutting: local runtime, offline operation, host integrity, and shutdown.
- DR-01 → Move and rule processing.
- DR-02 → Match detection.
- DR-03 → Removal, refill, and cascading; Scoring.
- DR-04 → Board and tile management; Game-state coordination.
- DR-05 → Game-state coordination.
- DR-06 → Scoring.

## Notes for TODO 6 (current code)

### Current Implementation Observations

The current implementation already has a useful coarse-grained division. `match3.py` imports no tkinter code and contains the constants, type aliases, pure board predicates, `MoveResult`, generation logic, and the stateful `Game` class. `main.py` contains the application entry point and one `Match3App` view/controller that creates widgets, tracks the current selection and busy flag, forwards swap and restart requests to `Game`, and renders the returned state. `tests/test_match3.py` targets `match3.py` directly with deterministic data. This matches the Exercise 1 requirement to keep logic testable without opening a window.

Within `match3.py`, the responsibility areas are logical boundaries rather than separate components. `Game` currently combines board ownership, scoring, cascade orchestration, refill, restart, and recovery, while standalone functions provide detection and move predicates. Within `main.py`, user-input handling and presentation are both methods of `Match3App`. These combinations are proportionate to the small prototype and are observations, not a proposal to split the code at this stage.

There are several differences between the requirements model and the concrete implementation. TODO 5 describes explicit lifecycle states such as Validating, Detecting Matches, Refilling, and Recovering, but the code does not define a state enum or state-machine object; synchronous `Game` calls plus `Match3App.selected` and `busy` provide the required observable behavior. FR-08 permits reshuffling or regeneration, while `ensure_playable` specifically regenerates a dead board. The generator also enforces that all six configured identities occur on a returned board, which is a concrete interpretation of FR-01.

The implementation provides some separation requested by the deferred NFR-05 even though TODO 4 did not make the broader maintainability exercise part of prototype acceptance. Conversely, the automated suite focuses on domain behavior and non-visual processing. Exercise 1 identified GUI response timing, visible feedback, and close behavior as manual acceptance concerns rather than fully automated tkinter tests.

### Responsibility → current code location

- Board and tile management → constants, board types, `copy_board`, `has_legal_move`, `is_playable_board`, `generate_playable_board`, and board/refill members of `Game` in `match3.py`.
- Move and rule processing → `in_bounds`, `are_adjacent`, `_swap`, `swap_creates_match`, and validation in `Game.attempt_swap` in `match3.py`.
- Match detection → `find_matches` in `match3.py`.
- Removal, refill, and cascading → `Game._resolve_cascades` and `Game._apply_gravity_and_refill` in `match3.py`.
- Scoring → `POINTS_PER_TILE` and score-increment logic in `Game._resolve_cascades` in `match3.py`; the current score total is also stored in `Game`.
- Game-state coordination → `Game.attempt_swap`, `Game.restart`, and `Game.ensure_playable` in `match3.py`; selection is currently stored in `Match3App.selected` in `main.py`.
- User input → `Match3App.on_tile_click`, `Match3App.restart`, and the current `Match3App.busy` input lock in `main.py`.
- Presentation → `TILE_STYLES`, `Match3App.render`, `Match3App._show_resolution_step`, and tkinter status/score widgets in `main.py`.

## Prompt log

```text
Revise only the TODO 1 section of architecture.md. Do not change code.
1. Derive the responsibilities from writeup.md and cite only requirement IDs in the table. Move the section "Current Implementation Observations" unchanged into a new section "Notes for TODO 6 (current code)" at the end of the file, and add there a short mapping "responsibility → current code location" built from the code references you remove from the table.
2. Remove "Testing and validation" as a responsibility. Add a short list "Cross-cutting constraints": requirements that the whole architecture must satisfy rather than one responsibility (e.g. testability without a GUI, platform, Python version, dependencies), with their IDs.
3. Give every piece of state and every decision exactly one owner:
   - selection rules and the selected tile belong to game-state coordination (the Selected state of the Exercise 1 state machine), so they can be tested without a GUI; user input only turns clicks into requests;
   - the scoring rule belongs to scoring; the score total belongs to game-state coordination, which also decides reset on restart and preservation on dead-board recovery;
   - board content and its invariants belong to board management; coordination only decides when a new board replaces the current one;
   - the input lock: name its single owner and the reason. ASSUMPTION unless writeup.md says otherwise: a move is resolved in one synchronous core call, so the lock is only needed while the GUI shows resolution steps and belongs to user input.
4. Add a column "GUI-independent" (yes/no).
5. State that the board invariant (full, match-free, at least one legal move) holds in every stable state waiting for input, not during resolution.
6. Add a traceability list: every requirement ID in writeup.md → the responsibility or cross-cutting constraint that covers it, or "not covered"; mark deferred requirements as deferred.
7. Mark every interpretation not stated in writeup.md with "ASSUMPTION:".
Shorten the prose sections to what still applies. Append this prompt to the Prompt log (create the section at the end of the file if it is missing).
```
