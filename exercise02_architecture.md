# Exercise 2: Software Architecture

## TODO 1: Core Responsibilities

### Responsibility Overview

| Responsibility | Purpose | Owns | Must Not Own | GUI-independent | Requirement IDs |
| --- | --- | --- | --- | --- | --- |
| Board and tile management | Maintain the board and tile data used by the game and generate playable boards for initialization, restart, and dead-board recovery. | Board content; board dimensions and tile identities; board mutation primitives; validation and tile supply; playable-board generation; the invariant that every stable state waiting for input is full, match-free, and has at least one legal move. The invariant is not required during resolution. **ASSUMPTION:** every generated board contains all six tile identities. **ASSUMPTION:** dead-board recovery regenerates a board rather than reshuffling the existing one. | The decision about when initialization, restart, or recovery replaces the current board; selection state; swap legality; scoring; or presentation. | Yes | FR-01, FR-08, FR-11, DR-04 |
| Move and rule processing | Evaluate a requested exchange. | Bounds and orthogonal-adjacency decisions; whether one exchange creates a match; matchless-swap rejection. | The selected tile or selection transitions, board content or its playable invariant, match scanning, score, or feedback text. | Yes | FR-02, FR-03, FR-04, DR-01 |
| Match detection | Identify every current horizontal and vertical run of at least three identical tiles. | The union of matched coordinates, including complete long and simultaneous runs with intersecting coordinates represented once. | Clearing cells, applying gravity, refilling, scoring, or UI feedback. | Yes | FR-05, DR-02 |
| Removal, refill, and cascading | Resolve all matches in the required order until the board is stable. | Simultaneous removal; downward gravity; refill; repeated detection; cascade completion and per-step cleared-cell results. | Initial swap legality, the scoring formula or score total, board replacement after a dead board, or rendering. | Yes | FR-05, FR-06, DR-03 |
| Scoring | Define the points produced by a resolution step. | The rule of exactly 10 points per distinct cleared tile, including cascades and excluding multipliers or bonuses; calculation of the score increment. | The accumulated score total, restart reset, recovery preservation, match membership, or score display. | Yes | FR-07, DR-03, DR-06 |
| Game-state coordination | Coordinate the session and the state-machine workflow. | First/second selection rules and the selected tile; sequencing of move validation and resolution; the accumulated score total; score reset on restart and preservation during recovery; readiness decisions; deciding when initialization, restart, or recovery requests a generated board to replace the current one; dead-board recovery; result reporting. | Board content, playable-board generation and invariant evaluation, the scoring formula, match detection, input-event capture, the input lock, or rendering. | Yes | UR-01, UR-02, UR-04, UR-05, FR-02, FR-03, FR-04, FR-07, FR-08, FR-10, DR-04, DR-05 |
| User input | Translate desktop actions into GUI-independent coordination requests. | Mouse-click and Restart-event translation. **ASSUMPTION:** one move is resolved in one synchronous core call, so User input owns the input lock needed while the GUI presents resolution steps; the lock prevents another click from changing the board before coordination returns to a stable waiting state. | The selected tile, selection rules, swap legality, board content, score, or status wording. | No | UR-01, FR-02, FR-06 |
| Presentation | Show the current game and action outcomes. | Tile colors and symbols; selected-tile highlighting; board and score rendering; accepted, rejected, resolution, and recovery feedback; control appearance. | Selection state, domain equality, swap legality, matching, board mutation, score calculation, or recovery decisions. | No | UR-03, UR-04, FR-07, FR-09, NFR-01 |

### Responsibility Boundaries

Board and tile management is the sole owner of board content, playable-board generation, and invariant evaluation. It generates boards for initialization, restart, and dead-board recovery. Game-state coordination only decides when one of those generated boards replaces the current content. The playable-board invariant applies whenever the game is stable and waiting for input; temporary empty cells and matches are permitted during resolution.

Game-state coordination owns session state: the selected coordinate, selection transitions, score total, and move lifecycle. Move and rule processing makes stateless legality decisions. Scoring produces a score increment but does not store the total. This keeps selection and scoring testable without a GUI.

Match detection only identifies coordinates. Removal, refill, and cascading consumes that result and controls resolution order. Presentation observes results but does not make domain decisions. User input translates events and, under the stated assumption, owns the input lock rather than the selected tile.

### Cross-cutting constraints

- **GUI-independent testability, deterministic verification, and core/GUI separation:** core responsibilities must be exercisable without opening a window, with controlled state or randomness, and must remain independent of graphical input and rendering. This separation is required, not deferred. IDs: UR-07, FR-11, NFR-07.
- **Performance and reliability:** input feedback, generation, recovery, cascade processing, and controlled robustness must meet their validated limits. IDs: UR-09, NFR-02, NFR-03. NFR-04 is deferred (Won't have for this prototype).
- **Further maintainability goals:** responsibilities should remain easy to understand and central gameplay values should not be duplicated. IDs: UR-08 and NFR-05, both deferred (Should have).
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
- UR-07 → Cross-cutting: GUI-independent testability, deterministic verification, and core/GUI separation.
- UR-08 → Cross-cutting: further maintainability goals — **deferred (Should have)**.
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
- FR-11 → Board and tile management; Cross-cutting: GUI-independent testability, deterministic verification, and core/GUI separation.
- NFR-01 → Presentation.
- NFR-02 → Cross-cutting: performance and reliability.
- NFR-03 → Cross-cutting: performance and reliability.
- NFR-04 → Cross-cutting: performance and reliability — **deferred (Won't have for this prototype)**.
- NFR-05 → Cross-cutting: further maintainability goals — **deferred (Should have)**.
- NFR-06 → Cross-cutting: documentation and scope control; local runtime.
- NFR-07 → Cross-cutting: GUI-independent testability, deterministic verification, and core/GUI separation.
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

## TODO 2: Architectural Components

**ASSUMPTION:** The seven fixed component names and boundaries below are the Exercise 2 decomposition of the Exercise 1 responsibilities; Exercise 1 specifies behavior and ownership concepts but does not name software components.

### Proposed component decomposition

The components are grouped only as GUI-independent core or GUI. No architectural pattern or detailed interface is selected here.

#### GUI-independent core components

No component in this group imports tkinter. `GameCoordinator`, including selection rules, move flow, score total, restart, and recovery, remains fully testable without a GUI.

| Fixed component name | Purpose | Main responsibilities | Not responsible for | State | Requirement IDs and cross-cutting constraints |
| --- | --- | --- | --- | --- | --- |
| `BoardManager` | Own the current board, tile-provider state, and playable-board generation. | Store and validate board content; expose controlled mutations; evaluate the stable playable-board invariant; generate boards for initialization, restart, and recovery; own a constructor-injected random, seeded, or deterministic tile provider used for generation and refill. | Deciding when to replace the board, selection, move or match rules, cascade order, scoring, or GUI behavior. | Current board content plus RNG state or deterministic tile-sequence position. | FR-01, FR-06, FR-08, FR-10, FR-11, DR-03, DR-04; GUI-independent testability/core separation; performance and reliability; further maintainability goals (deferred). |
| `RuleEngine` | Own all stateless move-legality and match-detection rules. | Check bounds and orthogonal adjacency; decide whether an exchange creates a match; determine whether a legal move exists; return the distinct coordinates in all horizontal and vertical runs of three or more, including long, simultaneous, and intersecting matches. | Holding selection or board state, mutating the board, clearing matches, controlling cascades, scoring, or presentation. | Stateless. | FR-02, FR-03, FR-04, FR-05, DR-01, DR-02, DR-04; GUI-independent testability/core separation; performance and reliability. |
| `ScoreRules` | Convert a resolution result into a score increment while keeping scoring policy isolated as an explicit evolution concern. | Apply exactly 10 points per distinct cleared coordinate, including cascades and without multipliers or bonuses. | Holding the score total, resetting or preserving it, detecting matches, or displaying score. | Stateless. | FR-07, DR-03, DR-06; GUI-independent testability/core separation. |
| `CascadeResolver` | Resolve accepted matches until the board becomes stable while remaining separate from rule evaluation. | Sequence simultaneous removal, gravity, refill through `BoardManager`, repeated match queries through `RuleEngine`, and score-increment calculation through `ScoreRules`; return per-step results to coordination. | Implementing match detection or move legality, holding selection or accumulated score, deciding dead-board replacement, or updating the GUI. | Stateless between resolution calls. | UR-02, FR-05, FR-06, FR-07, DR-03; GUI-independent testability/core separation; performance and reliability. |
| `GameCoordinator` | Own session state and coordinate the complete game workflow. | Own first/second selection rules and selected coordinate; accept a given board at construction and initialize `BoardManager` with it; sequence `RuleEngine` and `CascadeResolver`; own the score total; decide score reset and preservation; decide when `BoardManager` generates and installs a board; coordinate restart, recovery, readiness, and move results. | Owning board or tile-provider state, generating or validating boards itself, defining move/match/scoring rules, capturing GUI events, owning the input lock, or rendering. | Selected coordinate, accumulated score, and current lifecycle/readiness state; references to core collaborators. | UR-01, UR-02, UR-04, UR-05, FR-02, FR-03, FR-04, FR-07, FR-08, FR-10, DR-04, DR-05; GUI-independent testability/core separation; performance and reliability; further maintainability goals (deferred). |

#### GUI components

| Fixed component name | Purpose | Main responsibilities | Not responsible for | State | Requirement IDs and cross-cutting constraints |
| --- | --- | --- | --- | --- | --- |
| `DesktopUIAdapter` | Adapt tkinter input and presentation to the GUI-independent `GameCoordinator`. | Translate tile clicks and Restart activation into coordination requests; create and update board, tile, score, status, selection-highlight, and Restart widgets; render coordination and cascade results. **ASSUMPTION:** because a move resolves in one synchronous core call, own the GUI input-lock flag while resolution steps are presented and release it only after coordination returns to a stable waiting state. | Holding selected-tile, board, score-total, or workflow state; applying selection, move, match, cascade, or scoring rules; deciding recovery. | Tkinter widget references, derived display state, and the GUI input-lock flag. | UR-01, UR-03, UR-04, FR-02, FR-06, FR-07, FR-09, NFR-01; core/GUI separation; performance and reliability; local runtime constraints. |
| `ApplicationStartup` | Construct the application, wire all six collaborators, run the GUI loop, and close it cleanly. | Create the normal tile provider owned by `BoardManager`; create the remaining core components, `GameCoordinator`, and `DesktopUIAdapter`; start tkinter; route normal close to process termination. | Gameplay rules, session decisions, board or tile-provider state, score, rendering decisions, networking, persistence, or run-time plug-in discovery. | Application/root-window references while the process is running; no game state. | UR-06, NFR-09, NFR-10, NFR-12, NFR-13; documentation/scope control; local runtime/offline/host-integrity/shutdown constraints; concrete TODO 6 delivery constraints. |

### Responsibility-to-component mapping

| TODO 1 responsibility | Component(s) | Merge or split justification |
| --- | --- | --- |
| Board and tile management | `BoardManager` | Board content, playable-board generation, and the replaceable random or deterministic tile provider are merged for this small prototype. `BoardManager` remains their single state owner, and provider injection supports deterministic tests without a plug-in system. |
| Move and rule processing | `RuleEngine` | Merged with match detection because both are stateless rules over board snapshots. `RuleEngine` is the only authority for move legality. |
| Match detection | `RuleEngine` | Merged with move rules, but the match definition still has exactly one implementation in `RuleEngine` and remains outside cascade resolution. |
| Removal, refill, and cascading | `CascadeResolver`, `BoardManager`, `RuleEngine`, `ScoreRules` | `CascadeResolver` alone owns resolution order; `BoardManager` alone mutates/stores board content and supplies tiles; `RuleEngine` alone detects matches; `ScoreRules` alone calculates each score increment. |
| Scoring | `ScoreRules` | Kept separate and stateless; only the scoring formula lives here, while the total remains session state in `GameCoordinator`. |
| Game-state coordination | `GameCoordinator` | Kept as its own GUI-independent component because selection, move flow, score total, restart, and recovery must be testable without tkinter. |
| User input | `DesktopUIAdapter` | Merged with presentation because event translation, widgets, derived display state, and the GUI input lock share the same tkinter boundary; no domain state or rule moves into the adapter. |
| Presentation | `DesktopUIAdapter` | Merged with user input for the same small desktop boundary; the adapter owns rendering and widget state but no domain decision. |

The two merges reduce overhead without creating an all-purpose game-logic component: `RuleEngine` combines only stateless rules, and `DesktopUIAdapter` combines only tkinter-facing concerns. `ScoreRules` and `CascadeResolver` remain separate evolution and workflow boundaries. `ApplicationStartup` is an additional composition/lifecycle component required to create and connect the other six components; it owns no gameplay rule. The Must scope contains no networking, persistence, or general plug-in component.

### Logical versus physical implementation

These seven names define logical ownership, not a required one-class-per-file layout. A later physical implementation may place small stateless components together or keep them in separate modules, but it must preserve the authoritative state and rule owners above. The current TODO 6 code remains described separately in the notes below and does not determine this proposed decomposition. Detailed interfaces, dependency-call shapes, and architectural-pattern selection are intentionally deferred to later TODOs.

## TODO 3: Interfaces and Dependencies

**ASSUMPTION:** The contracts and conceptual operations below are an interface design derived from the validated behavior and TODO 2 ownership; Exercise 1 does not prescribe these interface shapes or names. They define information and dependency boundaries without selecting an architectural pattern or physical implementation.

### Shared Data Contracts

| Contract | Purpose | Producer | Consumers | Immutable or copied | GUI-specific information |
| --- | --- | --- | --- | --- | --- |
| `Coordinate` | Identify one board cell by row and column. | `DesktopUIAdapter`; core components when reporting results | `GameCoordinator`, `RuleEngine`, `BoardManager`, result contracts | Immutable value | None |
| `BoardSnapshot` | Provide a read-only view of all tile identities without sharing mutable board storage. | `BoardManager` | `RuleEngine`, `CascadeResolver`, `GameCoordinator`; `DesktopUIAdapter` only through `SessionSnapshot` or resolution results | Immutable representation or defensive copy | None |
| `MatchSet` | Represent every distinct coordinate matched in one resolution step. | `RuleEngine` | `CascadeResolver`, `ScoreRules` | Immutable set | None |
| `ResolutionStep` | Describe one completed clear/gravity/refill step for ordered presentation and scoring evidence. | `CascadeResolver` | `GameCoordinator`; `DesktopUIAdapter` through `InteractionResult` | Immutable record containing the cleared `MatchSet`, post-step `BoardSnapshot`, and score increment | None |
| `ResolutionResult` | Summarize all cascades from one accepted move. | `CascadeResolver` | `GameCoordinator`; `DesktopUIAdapter` through `InteractionResult` | Immutable ordered collection of `ResolutionStep` values plus total score increment | None |
| `SessionSnapshot` | Expose current session state without transferring ownership. | `GameCoordinator` | `DesktopUIAdapter` | Immutable record containing `BoardSnapshot`, accumulated score, selected coordinate or no selection, and readiness state | None |
| `InteractionResult` | Report the outcome of selection, move, restart, and recovery coordination. | `GameCoordinator` | `DesktopUIAdapter` | Immutable record containing a result code, `SessionSnapshot`, optional `ResolutionResult`, and recovery indicator | None |
| `ResultReason` | Give stable domain outcome/rejection codes that the GUI can translate into text. | `RuleEngine` for rule decisions; `GameCoordinator` for workflow outcomes | `GameCoordinator`, `DesktopUIAdapter` | Immutable enumerated value | None; no widget, color, or complete user-facing string |

Shared contracts carry values only. Passing a `BoardSnapshot`, `SessionSnapshot`, or result does not transfer or create ownership of another component's mutable state.

### Provided Component Interfaces

The operations below are conceptual capabilities, not Python method definitions.

#### BoardManager

| Provided operation | Input | Output | State changed | Allowed caller | Important precondition or postcondition |
| --- | --- | --- | --- | --- | --- |
| Obtain board snapshot | None | `BoardSnapshot` | None | `GameCoordinator`, `CascadeResolver` | Output cannot mutate the owned board. |
| Install supplied initial board | `BoardSnapshot` | Installed `BoardSnapshot` | Board content | `GameCoordinator` | Input is structurally valid; input is copied. Coordination must not expose input until the stable invariant holds. |
| Generate and install playable board | Generation request | `BoardSnapshot` | Board content and tile-provider state | `GameCoordinator` | Postcondition: full, match-free, and at least one legal move; TODO 1 generation assumptions apply. |
| Perform controlled swap | Two `Coordinate` values | `BoardSnapshot` | Board content | `GameCoordinator` | Coordinates are in bounds; only `BoardManager` mutates the stored board. |
| Clear coordinates | `MatchSet` | `BoardSnapshot` | Board content | `CascadeResolver` | Every supplied coordinate is cleared as one conceptual step. |
| Apply downward gravity | None | `BoardSnapshot` | Board content | `CascadeResolver` | Remaining tile order is preserved within each column. |
| Refill empty cells | None | `BoardSnapshot` | Board content and tile-provider state | `CascadeResolver` | Postcondition: all cells are occupied; tiles come from the owned provider. |
| Evaluate stable playable-board invariant | None | Boolean result | None | `GameCoordinator`; internal generation validation | Uses `RuleEngine`; the invariant is required only for a stable state waiting for input. |

#### RuleEngine

| Provided operation | Input | Output | State changed | Allowed caller | Important precondition or postcondition |
| --- | --- | --- | --- | --- | --- |
| Check bounds | `BoardSnapshot`, `Coordinate` | Boolean result | None | `GameCoordinator` | Snapshot is structurally readable. |
| Check orthogonal adjacency | Two `Coordinate` values | Boolean result | None | `GameCoordinator` | No board mutation occurs. |
| Determine whether swap creates a match | `BoardSnapshot`, two `Coordinate` values | Boolean result or rule rejection code | None | `GameCoordinator` | Evaluation uses snapshot data only and never mutates `BoardManager`. |
| Find all matches | `BoardSnapshot` | `MatchSet` | None | `CascadeResolver`, `BoardManager` | Returns the union of every qualifying run with no duplicate coordinate. |
| Determine whether a legal move exists | `BoardSnapshot` | Boolean result | None | `BoardManager` | Snapshot is full and stable when used for the playable-board invariant. |

#### ScoreRules

| Provided operation | Input | Output | State changed | Allowed caller | Important precondition or postcondition |
| --- | --- | --- | --- | --- | --- |
| Calculate score increment | `MatchSet` | Non-negative point increment | None | `CascadeResolver` | Exactly 10 points per distinct coordinate; no multiplier or bonus. |

#### CascadeResolver

| Provided operation | Input | Output | State changed | Allowed caller | Important precondition or postcondition |
| --- | --- | --- | --- | --- | --- |
| Resolve all cascades | Initial non-empty `MatchSet` | `ResolutionResult` | Board content and tile-provider state, only through `BoardManager` | `GameCoordinator` | Precondition: accepted swap is installed. Postcondition: board is full and match-free; accumulated session score is unchanged. |

#### GameCoordinator

| Provided operation | Input | Output | State changed | Allowed caller | Important precondition or postcondition |
| --- | --- | --- | --- | --- | --- |
| Initialize session | Optional supplied `BoardSnapshot` | Initial `SessionSnapshot` | Selected coordinate, score total, lifecycle state; board through `BoardManager` | `ApplicationStartup` | A supplied board is copied; input is exposed only after the stable invariant holds. |
| Handle tile-selection request | `Coordinate` | `InteractionResult` | Selected coordinate; for an accepted move, score total and board through collaborators | `DesktopUIAdapter` | Session is waiting for input. Result is selected, rejected, or accepted with ordered resolution data and a final stable playable snapshot. |
| Restart session | Restart request | `InteractionResult` | Selection cleared, score total set to zero, lifecycle state, board through `BoardManager` | `DesktopUIAdapter` | Postcondition: fresh playable board, zero score, no selection. |
| Obtain session snapshot | None | `SessionSnapshot` | None | `DesktopUIAdapter` | Output is immutable and contains no GUI object. |

#### DesktopUIAdapter

| Provided operation | Input | Output | State changed | Allowed caller | Important precondition or postcondition |
| --- | --- | --- | --- | --- | --- |
| Initialize desktop UI | Window/lifecycle context, `GameCoordinator` | Ready GUI adapter | Widget and derived display state | `ApplicationStartup` | The adapter's only gameplay dependency is `GameCoordinator`. |
| Translate tile event | Pointer event mapped to `Coordinate` | None; renders returned `InteractionResult` | Derived display state; input-lock flag while required | Tkinter event loop | Domain request is sent only to `GameCoordinator`; no board mutation occurs in the adapter. |
| Translate Restart event | Restart event | None; renders returned `InteractionResult` | Derived display state; input-lock flag while required | Tkinter event loop | Restart is sent only to `GameCoordinator`. |
| Render state and interaction result | `SessionSnapshot`, optional `InteractionResult` | Visible GUI update | Widget and derived display state | `DesktopUIAdapter` itself; `ApplicationStartup` for initial display | Domain reason codes are translated to user-facing wording here. |
| Acquire or release GUI input lock | Lock or unlock request | None | GUI input-lock flag | `DesktopUIAdapter` itself | Locked input cannot issue another board-changing request; no domain state is stored. |

#### ApplicationStartup

| Provided operation | Input | Output | State changed | Allowed caller | Important precondition or postcondition |
| --- | --- | --- | --- | --- | --- |
| Create and wire dependencies | Runtime configuration | Constructed application | Application/window references only | Application entry point | Dependencies follow the acyclic table below; no gameplay decision is made. |
| Start application | Constructed application | Running GUI loop | Application lifecycle state | Application entry point | All components are wired before player input is accepted. |
| Close application | Normal close request | Terminated application | Application/window references released | Window manager through startup-installed close handling | Process exits cleanly without persisting game state. |

### Dependency Table

| Caller | Dependency | Information or operation used | Why the dependency is necessary | Why the reverse dependency is forbidden |
| --- | --- | --- | --- | --- |
| `ApplicationStartup` | All other six components | Construction, wiring, GUI start, and close lifecycle | It is the composition root and lifecycle owner. | Components must not construct the application or make startup own gameplay. |
| `DesktopUIAdapter` | `GameCoordinator` | Tile/restart requests and immutable interaction/session results | It must translate GUI events without accessing domain internals. | Core coordination must remain GUI-independent and cannot call tkinter. |
| `GameCoordinator` | `BoardManager` | Snapshot, supplied-board install, controlled swap, playable-board generation, invariant result | Coordination sequences workflow while board ownership stays singular. | Board management must not own selection, score total, restart decisions, or session flow. |
| `GameCoordinator` | `RuleEngine` | Bounds, adjacency, and swap-legality decisions | Coordination needs rule facts without duplicating rules. | Stateless rules must not depend on session state or control workflow. |
| `GameCoordinator` | `CascadeResolver` | Complete `ResolutionResult` for an accepted move | Coordination delegates the ordered resolution process. | Resolution must not own selection, score total, or session recovery. |
| `BoardManager` | `RuleEngine` | Match-free and legal-move facts for invariant evaluation | It must validate generated and stable boards without duplicating rules. | Rules must not access or mutate the owned board. |
| `CascadeResolver` | `BoardManager` | Controlled clear, gravity, refill, and snapshots | Resolution order requires board changes through the sole board owner. | Board management must not control cascade order. |
| `CascadeResolver` | `RuleEngine` | Repeated `MatchSet` detection | Cascades require the one authoritative match implementation. | Rule evaluation must remain stateless and cannot control resolution. |
| `CascadeResolver` | `ScoreRules` | Per-step score increment | Resolution needs point deltas but must not duplicate scoring policy. | Scoring policy must not control cascades or mutate board/session state. |

`RuleEngine` and `ScoreRules` have no production-component dependencies. Shared data contracts are values and do not create dependencies on, or ownership of, the state of their producer.

### Player-Move Information Flow

1. **First tile click:** `DesktopUIAdapter` converts the event to a `Coordinate` and calls `GameCoordinator`. Coordination stores the selected coordinate and returns an `InteractionResult` with a selected reason code and immutable `SessionSnapshot`. The adapter renders the highlight.
2. **Second adjacent tile click:** `DesktopUIAdapter` acquires its GUI input lock and sends the second `Coordinate`. `GameCoordinator` asks `RuleEngine` for bounds, adjacency, and match-producing-swap decisions using a `BoardSnapshot` from `BoardManager`.
3. **Rejected move:** If a selection is invalid, non-adjacent, or matchless, `GameCoordinator` clears the selected coordinate, preserves board and score, and returns a rejection reason plus unchanged domain state. `DesktopUIAdapter` maps the code to wording and renders it.
4. **Accepted move with cascades:** `GameCoordinator` directs `BoardManager` to install the accepted swap and passes the initial `MatchSet` from `RuleEngine` to `CascadeResolver`. The resolver clears, applies gravity, refills through `BoardManager`, queries `RuleEngine` again, and uses `ScoreRules` for each increment until no match remains. It returns ordered immutable steps and a total increment.
5. **Score update:** `CascadeResolver` never changes the session total. `GameCoordinator` applies the returned total increment to its accumulated score and includes the authoritative final total in the resulting `SessionSnapshot`.
6. **Dead-board recovery:** `GameCoordinator` asks `BoardManager` to evaluate the stable invariant. If no legal move remains, coordination preserves its score and directs `BoardManager` to generate and install a playable replacement, then records recovery in the interaction result.
7. **Final rendering and unlock:** `DesktopUIAdapter` renders ordered `ResolutionStep` data, recovery feedback, and the final `SessionSnapshot`, then releases its GUI input lock. Core results contain only domain data and reason codes; the adapter owns all displayed wording and widgets.

This is an interface-level flow only; detailed alternatives and timing belong to TODO 5.

### Undesirable Dependencies and Coupling Controls

| Rejected coupling | Architectural control |
| --- | --- |
| `DesktopUIAdapter` directly mutating `BoardManager` | Its only gameplay dependency is `GameCoordinator`; board operations are not exposed to the adapter. |
| Core components importing or calling tkinter | Only `DesktopUIAdapter` and `ApplicationStartup` may use tkinter; all core inputs and outputs use shared domain contracts. |
| `RuleEngine` mutating board state | It accepts only `BoardSnapshot` values and has no dependency on `BoardManager`. |
| `CascadeResolver` changing accumulated score | It receives score increments from `ScoreRules` and returns a total; only `GameCoordinator` stores and updates accumulated score. |
| Duplicate match or scoring rules | `RuleEngine` is the sole match-rule owner and `ScoreRules` is the sole scoring-policy owner; all consumers call them. |
| Passing shared mutable board lists | `BoardManager` exposes immutable or defensive-copy `BoardSnapshot` values; all mutations use its controlled operations. |
| Core results containing GUI wording or widget objects | Results use domain contracts and `ResultReason` codes; `DesktopUIAdapter` maps them to text, colors, and widgets. |
| Cyclic dependencies | The dependency table is one-way: startup → GUI → coordination → core services, with resolver/board dependencies ending at stateless rules. Reverse calls are forbidden. |
| `ApplicationStartup` making gameplay decisions | Startup is limited to construction, lifecycle, and clean close; `GameCoordinator` owns every session decision. |

### Assumptions and Open Interface Questions

- **ASSUMPTION:** A second-tile or Restart request completes through one synchronous core call. `DesktopUIAdapter` therefore holds its input lock while it presents returned resolution steps rather than while core work continues in the background.
- **ASSUMPTION:** A supplied construction board needs to be structurally valid but may be non-playable for a controlled test; `GameCoordinator` must not expose player input until `BoardManager` reports the stable invariant.
- **ASSUMPTION:** For per-cascade score display, `DesktopUIAdapter` derives intermediate displayed totals from the pre-move `SessionSnapshot` and ordered `ResolutionStep` increments; the authoritative accumulated total remains only in `GameCoordinator`.
- **Open question:** The physical immutable representation of `BoardSnapshot` and `MatchSet` is deferred, provided callers cannot mutate owned board state.
- **Open question:** The exact enumerated identifiers for `ResultReason` are deferred; their semantics must still distinguish selection, acceptance, restart/recovery, invalid selection, non-adjacency, and no-match rejection.
- **Open question:** The adapter may present ordered steps immediately with GUI refreshes or schedule their presentation; either choice must retain the input lock and does not introduce a gameplay animation requirement.

No architectural pattern or component/sequence diagram is selected in TODO 3.

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

### Revision prompt 2

```text
Same rules as before (write only to architecture.md, no code changes, cite requirement IDs, mark ASSUMPTIONs, append this prompt to the Prompt log).

Part A – small corrections to TODO 1:
1. Make the "Requirement IDs" column and the Requirement Traceability list consistent. Currently UR-01 and FR-02–FR-04 are traced to Game-state coordination but missing in its row; FR-08 is traced to Board and tile management and DR-03 to Scoring but missing in those rows; FR-11 appears in the Board row but is traced only to a cross-cutting constraint (it is functional: trace it to the responsibility that supplies tiles as well).
2. State explicitly that board and tile management generates playable boards (initial, restart, dead-board recovery) and game-state coordination only decides when.
3. Core/GUI separation is already required by the testability constraint (UR-07, NFR-07), so it must not appear as deferred; only the further maintainability goals of UR-08/NFR-05 are deferred.
4. Check FR-01 and FR-08 in writeup.md: if they now state all six identities and regeneration only, update the outdated sentence in "Notes for TODO 6"; otherwise mark both points as ASSUMPTION in TODO 1.

Part B – TODO 2: Define architectural components, based on TODO 1 (not on the current code).
For each component: a fixed name that all later sections must reuse; purpose; main responsibilities; boundaries ("not responsible for ..."); the state it holds, or "stateless"; the requirement IDs and cross-cutting constraints it realizes.
Add a mapping "TODO 1 responsibility → component(s)" and justify every merge or split.
Constraints:
- No game-logic component imports tkinter. Game-state coordination (selection rules, move flow, score total, dead-board recovery, restart) is its own component and does not import tkinter either.
- The tile source must be replaceable so tests can be deterministic, and the coordination component must be constructible with a given board.
- Each rule (e.g. match detection) lives in exactly one component; no component does everything; each piece of state has exactly one owner, as in TODO 1.
- Include the startup component that creates and wires all objects and starts and closes the GUI.
- Must scope only (KISS/YAGNI): no networking, persistence or plug-in system.
- Do not choose an architectural pattern yet (that is TODO 4); group components only as GUI-independent core vs GUI.
Insert the result as section "TODO 2: Architectural Components" directly after TODO 1, before "Notes for TODO 6".
```

### Revision prompt 3

```text
Revise only TODO 2 in exercise02_architecture.md. Do not change TODO 1,
Notes for TODO 6, source code, or tests.

The current ten-component decomposition is internally consistent but too
fine-grained for this small prototype. Reduce it to these seven fixed
architectural components:

1. BoardManager
2. RuleEngine
3. ScoreRules
4. CascadeResolver
5. GameCoordinator
6. DesktopUIAdapter
7. ApplicationStartup

Apply these merges:

- Merge MoveRules and MatchDetector into RuleEngine.
  RuleEngine owns all stateless move-legality and match-detection rules.
  Match detection must still have exactly one implementation and must remain
  separate from cascade resolution.

- Merge InputController and GameView into DesktopUIAdapter.
  It owns tkinter event translation, rendering, widget state, derived display
  state, and the GUI input-lock flag. It owns no domain state or game rule.

- Remove TileSource as a top-level architectural component.
  Treat the random or deterministic tile provider as a replaceable dependency
  owned by BoardManager. BoardManager owns its RNG or deterministic-sequence
  state. This remains constructor-injectable for deterministic tests but is not
  a plug-in system.

Keep:

- ScoreRules separate because future scoring policies are an explicit evolution
  concern.
- CascadeResolver separate from RuleEngine.
- GameCoordinator as the only owner of selected tile, score total, and session
  workflow.
- ApplicationStartup as the composition and lifecycle component.

Update all TODO 2 tables and prose consistently:

- Proposed component decomposition
- Responsibility-to-component mapping
- Component names and ownership descriptions
- Logical-versus-physical implementation explanation

Every TODO 1 responsibility must still be covered.
Every mutable state and domain decision must still have one authoritative owner.
Do not define detailed interfaces yet.
Do not select an architectural pattern.
Do not create diagrams.
Do not commit yet.

Append this exact revision prompt to the Prompt log.
Run git diff --check when finished.
```

### TODO 3 prompt

```text
Continue Exercise 2 in exercise02_architecture.md.

Complete only TODO 3: Specify Interfaces and Dependencies.

Insert TODO 3 immediately after TODO 2 and before
"Notes for TODO 6 (current code)".

Use these seven component names exactly:

- BoardManager
- RuleEngine
- ScoreRules
- CascadeResolver
- GameCoordinator
- DesktopUIAdapter
- ApplicationStartup

Do not modify TODO 1 or TODO 2.

## Dependency rules

Use this acyclic dependency direction:

- ApplicationStartup constructs and wires all components.
- DesktopUIAdapter depends only on GameCoordinator during gameplay.
- GameCoordinator depends on BoardManager, RuleEngine, and CascadeResolver.
- BoardManager may depend on RuleEngine only to evaluate the stable playable-board
  invariant.
- CascadeResolver depends on BoardManager, RuleEngine, and ScoreRules.
- RuleEngine and ScoreRules depend on no other production component.
- No GUI-independent component imports or calls tkinter.
- No core component depends on DesktopUIAdapter.
- ApplicationStartup performs construction and lifecycle work, not gameplay.

Preserve the ownership established in TODO 1 and TODO 2:

- BoardManager is the only owner of mutable board content and tile-provider state.
- RuleEngine is stateless and never mutates the board.
- ScoreRules is stateless and never stores the accumulated score.
- CascadeResolver owns resolution order but mutates the board only through
  BoardManager.
- GameCoordinator owns selected tile, accumulated score, and session workflow.
- DesktopUIAdapter owns widgets, derived display state, and the GUI input lock.
- ApplicationStartup owns no game state.

## Required structure

## TODO 3: Interfaces and Dependencies

### Shared Data Contracts

Define a small table containing the conceptual data passed between components.
Include only the data needed by this prototype, such as:

- Coordinate
- BoardSnapshot
- MatchSet
- ResolutionStep
- ResolutionResult
- SessionSnapshot
- InteractionResult or MoveResult
- Result/rejection reason codes

For each contract state:

- purpose,
- producer,
- consumers,
- whether it is immutable or copied,
- whether it contains any GUI-specific information.

Core results must contain domain data or reason codes, not tkinter widgets,
colors, or complete user-facing message strings.

### Provided Component Interfaces

For each of the seven components, define a minimal conceptual interface table
with:

- Provided operation
- Input
- Output
- State changed
- Allowed caller
- Important precondition or postcondition

Use concise conceptual signatures, not Python implementation code.

The interfaces should cover at least:

BoardManager:
- obtain a read-only board snapshot,
- install a supplied initial board,
- generate and install a playable board,
- perform controlled swap, clear, gravity, and refill operations,
- evaluate the stable playable-board invariant.

RuleEngine:
- check bounds and adjacency,
- determine whether a swap creates a match,
- find all matches,
- determine whether a legal move exists.

ScoreRules:
- calculate the increment for a set of cleared coordinates.

CascadeResolver:
- resolve all cascades and return ordered ResolutionStep results plus the total
  score increment, without changing the accumulated session score.

GameCoordinator:
- handle a tile-selection request,
- restart the session,
- expose an immutable SessionSnapshot,
- coordinate accepted/rejected moves, score updates, and recovery.

DesktopUIAdapter:
- translate tile and Restart events into GameCoordinator requests,
- render a SessionSnapshot and interaction results,
- manage the GUI input lock.

ApplicationStartup:
- create dependencies,
- start the application,
- close it cleanly.

### Dependency Table

Create a table with:

- Caller
- Dependency
- Information or operation used
- Why the dependency is necessary
- Why the reverse dependency is forbidden

State explicitly that shared data contracts do not create ownership of another
component's state.

### Player-Move Information Flow

Describe the information flow for:

1. first tile click,
2. second adjacent tile click,
3. rejected move,
4. accepted move with one or more cascades,
5. score update,
6. dead-board recovery,
7. final rendering and release of the GUI input lock.

Keep this at interface-flow level. The detailed sequence scenario belongs to
TODO 5.

### Undesirable Dependencies and Coupling Controls

Identify and reject at least these coupling problems:

- DesktopUIAdapter directly mutating BoardManager,
- core components importing tkinter,
- RuleEngine mutating board state,
- CascadeResolver changing the accumulated score,
- duplicate match or scoring rules,
- passing shared mutable board lists between components,
- core results containing GUI wording or widget objects,
- cyclic dependencies,
- ApplicationStartup making gameplay decisions.

For each, state the architectural control that prevents it.

### Assumptions and Open Interface Questions

List only genuine unresolved questions that affect later implementation.
Mark every interpretation not stated in writeup.md as "ASSUMPTION:".

Do not select an architectural pattern; that belongs to TODO 4.
Do not create component or sequence diagrams; that belongs to TODO 5.
Do not modify Python code, README.md, writeup.md, or tests.
Do not commit yet.

Append this exact prompt to the Prompt log.
Run git diff --check when finished.
```
