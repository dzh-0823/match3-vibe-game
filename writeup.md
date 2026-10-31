# Exercise 1: Requirements Engineering

## TODO 1: Clarify the Problem Context

### 1. Ambiguous or underspecified aspects

The phrase **"a basic locally runnable match-3 game"** does not fully define the product. The following aspects need clarification:

- The target operating system, required Python version, and permitted third-party libraries are not specified.
- "Locally runnable" could mean a desktop application, a browser application served from the local machine, or a terminal program.
- The intended player and expected session length are unknown.
- The board dimensions, number of tile types, and visual style are unspecified.
- The rules for a legal swap are unclear, including whether swaps that create no match should be rejected or reversed.
- Match detection is not fully defined: horizontal versus vertical matches, runs longer than three, and intersecting matches all need explicit behavior.
- The order of clearing, gravity, refilling, and cascade resolution is unspecified.
- It is unclear whether the initial board may contain matches or have no possible moves.
- There is no defined scoring system, move limit, timer, win condition, or loss condition.
- Input, feedback, restart behavior, sound, accessibility, and error handling requirements are not stated.

### 2. Hidden assumptions

Unless later requirements replace them, the first prototype assumes that:

- One person plays offline on a single computer using a mouse.
- The game does not require an account, network connection, server, installation service, or persistent data.
- The player swaps two orthogonally adjacent tiles; diagonal swaps are not allowed.
- A swap is valid only when it produces at least one horizontal or vertical run of three or more identical tiles. An invalid swap leaves the board unchanged and does not consume a move.
- All matches created in one resolution step are cleared together. Tiles then fall downward, empty cells are refilled, and new matches are resolved repeatedly until the board is stable.
- A run longer than three and every distinct cell in an intersecting match are cleared, with an intersecting cell counted only once for scoring.
- The game generates a starting board with no existing matches and at least one legal move.
- Random results do not need to be identical between normal play sessions, although deterministic randomness may be used for testing.
- Simple shapes, colors, and text are sufficient; polished art and audio are not required to prove the gameplay.

### 3. Unresolved design choices

The following choices remain open for later requirements or implementation planning:

- Desktop GUI framework and exact supported platforms.
- Final board size, tile set, color palette, typography, and window dimensions.
- Final scoring balance and whether cascades receive a multiplier.
- Whether the finished game uses a move limit, timer, score target, levels, or endless play.
- How a board with no legal moves is handled: reshuffle, regenerate, or end the session.
- Whether hints, animations, sound effects, keyboard/touch controls, and accessibility options are needed.
- Whether player settings, high scores, or saved sessions persist between runs.

These choices should not prevent the first prototype from using the temporary baseline defined below.

### 4. Development goal for the first playable prototype

Build a single-screen, offline desktop prototype that can be launched locally and supports one complete match-3 play loop. For this prototype, use an 8 x 8 board with six visually distinct tile types, mouse selection, orthogonally adjacent swaps, and the match-resolution rules stated above. Award 10 points for each distinct tile cleared. The session is endless; it displays the current score and provides a restart control. If the stable board has no legal move, it is reshuffled or regenerated into a valid board.

The prototype is complete when all of the following can be demonstrated:

1. Launching the documented local command opens a usable game screen without requiring a network connection.
2. The initial 8 x 8 board contains no pre-existing match and has at least one legal move.
3. A non-adjacent or diagonal selection cannot be swapped.
4. An adjacent swap that creates no match leaves the board unchanged and does not change the score.
5. A valid swap clears every resulting horizontal and vertical run of at least three tiles.
6. Cleared spaces are filled by downward gravity and new tiles, and cascades continue until no matches remain.
7. The score increases by exactly 10 points per distinct cleared tile across the initial match and any cascades.
8. Play can continue after each resolved move, including after recovery from a board with no legal moves.
9. Restart creates a fresh valid board and resets the score to zero.

### 5. Explicitly out of scope

The first playable prototype will not include:

- Online play, multiplayer, leaderboards, accounts, cloud saves, analytics, or advertisements.
- Mobile or web deployment, touch controls, or gamepad support.
- Multiple levels, a campaign, narrative, tutorials, achievements, daily challenges, or difficulty modes.
- Special tiles, power-ups, blockers, obstacles, lives, boosters, or in-app purchases.
- Production-quality artwork, complex animation, particles, music, voice acting, or a full sound system.
- Persistent settings, saved games, or high-score storage.
- Localization or a complete accessibility suite beyond keeping the six tile types visually distinguishable.
- Packaging, an installer, automatic updates, or distribution through an application store.
- Automated strategy, opponent AI, or a hint system.

## TODO 2: Identify Stakeholders and Elicit Needs

### 1. Stakeholder analysis

#### Player

**Interests**

- Enjoying a recognizable and satisfying match-3 play loop.
- Understanding the board, available actions, score, and results of each action.
- Starting and restarting a game with little effort.

**Expectations**

- Tile selection and swapping feel clear and responsive.
- Valid matches, invalid moves, cascades, scoring, and board recovery behave consistently.
- Tiles are visually distinguishable and the game provides enough feedback to understand what happened.
- The game remains playable without an internet connection.

**Constraints**

- The player may have no prior knowledge of this particular game.
- The player uses the input devices and display available on the local computer.
- The player should not need an account, server, or complicated setup.
- Differences in vision, display quality, or window size may make color-only distinctions difficult.

#### Developer

**Interests**

- Delivering the first playable prototype within limited time and scope.
- Translating the agreed match-3 behavior into logic that can be tested and debugged.
- Keeping gameplay rules separate enough from presentation details to support safe changes.

**Expectations**

- The prototype scope, gameplay terms, and completion criteria are unambiguous.
- Important cases such as intersecting matches, cascades, invalid swaps, and boards with no legal moves have defined outcomes.
- Failures can be reproduced and diagnosed without depending entirely on random play.
- Dependencies and setup steps remain minimal and documented.

**Constraints**

- The developer must work within the available language, libraries, tools, and schedule.
- Random board generation creates edge cases that may be difficult to reproduce.
- A prototype should avoid architecture or features that are unnecessary for its stated goal.
- Implementation choices must remain compatible with the intended local runtime.

#### Maintainer

**Interests**

- Understanding and changing the game safely after the first implementation.
- Locating defects quickly and avoiding regressions in core gameplay.
- Updating dependencies or runtime versions with limited effort.

**Expectations**

- Code responsibilities, gameplay rules, setup, and execution steps are understandable and documented.
- Core behavior can be checked independently of visual presentation where practical.
- Constants and configurable values are not unnecessarily duplicated throughout the implementation.
- Failures are reported clearly enough to support diagnosis.

**Constraints**

- The maintainer may not be the original developer.
- Future maintenance time and knowledge of undocumented decisions may be limited.
- Changes to the runtime or external libraries may introduce compatibility problems.

#### Platform/runtime environment

This is a supporting technical stakeholder representing the local computer, operating system, language runtime, display system, and installed dependencies on which the game relies.

**Interests**

- Running the game within available CPU, memory, display, input, and storage resources.
- Loading only compatible, available dependencies.
- Starting and stopping without damaging the host environment.

**Expectations**

- The game has a documented launch method and supported runtime configuration.
- Normal play does not require network access, elevated privileges, or external services.
- Input events, rendering, and game-state updates are handled promptly.
- The program exits cleanly and handles foreseeable startup problems in an understandable way.

**Constraints**

- Runtime versions, operating systems, screen sizes, permissions, and dependency availability may vary.
- Local machines may have modest processing power and memory.
- The environment cannot compensate for missing dependencies or undocumented setup steps.
- Platform-specific behavior may limit portability unless supported environments are deliberately chosen.

### 2. Initial stakeholder needs

The following statements are elicited stakeholder needs, not yet formal system requirements. **Explicit** needs follow directly from stated stakeholder expectations or the prototype context. **Implicit** needs are necessary to support those expectations even when a stakeholder may not request them directly. Later requirements work should refine, prioritize, and make them fully measurable.

| ID | Type | Source stakeholder | Concern | Stakeholder need |
| --- | --- | --- | --- | --- |
| NEED-01 | Explicit | Player | Gameplay | The player needs to select and attempt swaps between tiles using simple, understandable controls. |
| NEED-02 | Explicit | Player | Gameplay | The player needs valid matches, clearing, gravity, refilling, cascades, and scoring to follow consistent rules. |
| NEED-03 | Explicit | Player | Usability | The player needs clear visual feedback for selection, accepted moves, rejected moves, board changes, and score changes. |
| NEED-04 | Implicit | Player | Usability | The player needs tile types to remain distinguishable without relying only on subtle color differences. |
| NEED-05 | Explicit | Player | Usability | The player needs to see the current score and restart play without restarting the entire application. |
| NEED-06 | Implicit | Player | Reliability | The player needs the game to remain recoverable and playable when the board has no legal move. |
| NEED-07 | Explicit | Player | Local execution | The player needs to launch and play the game offline on the supported local computer without an account or external service. |
| NEED-08 | Explicit | Developer | Gameplay | The developer needs agreed outcomes for invalid swaps, long and intersecting matches, cascades, initial boards, and boards with no legal moves. |
| NEED-09 | Implicit | Developer | Reliability | The developer needs controllable or reproducible game states so edge cases and reported defects can be investigated. |
| NEED-10 | Explicit | Developer | Maintainability | The developer needs a bounded prototype scope and a clear separation between core game behavior and presentation concerns. |
| NEED-11 | Explicit | Developer | Local execution | The developer needs a small, documented dependency and setup footprint compatible with the selected local runtime. |
| NEED-12 | Explicit | Maintainer | Maintainability | The maintainer needs readable structure and documentation for setup, launch, gameplay rules, and important design decisions. |
| NEED-13 | Implicit | Maintainer | Maintainability | The maintainer needs central definitions for changeable gameplay values so routine changes do not require scattered edits. |
| NEED-14 | Explicit | Maintainer | Reliability | The maintainer needs practical checks for core gameplay behavior so changes can be made without silently breaking established behavior. |
| NEED-15 | Implicit | Maintainer | Reliability | The maintainer needs understandable diagnostic information when startup or gameplay processing fails. |
| NEED-16 | Explicit | Platform/runtime environment | Local execution | The local environment needs a documented, compatible runtime configuration and launch method. |
| NEED-17 | Implicit | Platform/runtime environment | Performance | The local environment needs the game to keep input and visual updates responsive during ordinary play on modest hardware. |
| NEED-18 | Implicit | Platform/runtime environment | Performance | The local environment needs board generation and cascade resolution to finish without unbounded processing or excessive resource use. |
| NEED-19 | Explicit | Platform/runtime environment | Reliability | The local environment needs the game to start and exit cleanly without elevated privileges, network availability, or unintended changes outside the game process. |
| NEED-20 | Implicit | Developer; Maintainer; Platform/runtime environment | Portability | The involved technical stakeholders need supported platforms and runtime versions to be identified so compatibility can be evaluated and maintained. |

## TODO 3: Transform Needs into Structured Requirements

### 1. User requirements

User requirements express the outcomes that stakeholders need in language that can be reviewed without reference to an implementation. They remain consistent with the first playable prototype defined in TODO 1.

| ID | Category | Requirement statement | Source need IDs | Verification method |
| --- | --- | --- | --- | --- |
| UR-01 | Player interaction | The player must be able to select tiles and attempt swaps with clear, simple mouse controls. | NEED-01, NEED-03 | Acceptance demonstration using the game screen. |
| UR-02 | Core gameplay | The player must receive a consistent match-3 loop covering valid and invalid swaps, clearing, gravity, refilling, cascades, and scoring. | NEED-02, NEED-08 | Scenario-based acceptance test using controlled board states. |
| UR-03 | Visual usability | The player must be able to distinguish tile types and understand selections, accepted actions, rejected actions, and resulting board changes. | NEED-03, NEED-04 | Visual inspection and usability test. |
| UR-04 | Session control | The player must be able to view the current score and start a fresh session without relaunching the application. | NEED-05 | Acceptance demonstration of scoring and restart. |
| UR-05 | Continuity of play | The player must be able to continue an endless session after each resolved move, including when the board reaches a state with no legal move. | NEED-06 | Acceptance test with a controlled dead-board state. |
| UR-06 | Local execution | The player must be able to launch, play, and close the prototype on a documented supported local environment without an account, network connection, external service, or elevated privileges. | NEED-07, NEED-11, NEED-16, NEED-19, NEED-20 | Installation and execution test in a disconnected, standard-permission environment. |
| UR-07 | Development assurance | The developer must be able to reproduce important game states and check core gameplay behavior after changes. | NEED-09, NEED-14 | Inspection and execution of deterministic test scenarios. |
| UR-08 | Maintenance support | A maintainer must be able to understand the project, locate changeable gameplay values, diagnose failures, and modify core behavior without unnecessary changes to presentation code. | NEED-10, NEED-12, NEED-13, NEED-15 | Documentation and architecture review followed by a small change exercise. |
| UR-09 | Responsiveness | The player must receive prompt input feedback, and ordinary board generation and resolution must not interrupt play with excessive delays. | NEED-17, NEED-18 | Timed acceptance and stress tests on the documented reference environment. |

### 2. System requirements

#### 2.1 Functional requirements

| ID | Category | Requirement statement | Source need IDs | Verification method |
| --- | --- | --- | --- | --- |
| FR-01 | Session initialization | The system shall create an 8 x 8 board containing exactly six tile types at the start of every session. Before accepting input, that board shall contain no existing match and at least one legal move. | NEED-02, NEED-06, NEED-08 | Automated initialization tests across controlled random seeds, plus board-state inspection. |
| FR-02 | Tile input | The system shall allow the player to select a tile with the mouse and attempt a swap only with a horizontally or vertically adjacent tile. | NEED-01, NEED-08 | GUI acceptance tests for each orthogonal direction. |
| FR-03 | Invalid selection | The system shall reject attempts to swap diagonal, non-adjacent, or out-of-board positions without changing the board or score. | NEED-01, NEED-03, NEED-08 | Automated and GUI tests comparing state before and after invalid attempts. |
| FR-04 | Matchless swap | The system shall reject an adjacent swap that creates no match, leaving the board and score unchanged. | NEED-02, NEED-03, NEED-08 | Automated test using a controlled board with a known matchless swap. |
| FR-05 | Match processing | After a valid swap, the system shall identify and clear all matched cells in the current resolution step according to DR-02. | NEED-02, NEED-08 | Automated tests for horizontal, vertical, long, simultaneous, and intersecting matches. |
| FR-06 | Board resolution | After clearing matched cells, the system shall apply downward gravity, refill every empty cell, and repeat match processing until the board is stable. | NEED-02, NEED-08, NEED-18 | Automated cascade tests using controlled board states and tile sequences. |
| FR-07 | Scoring | The system shall initialize the score to zero, add 10 points for each distinct cleared tile in every resolution step, and display the updated score after each step. | NEED-02, NEED-05, NEED-08 | Automated score calculations and GUI display checks for simple, long, intersecting, and cascading matches. |
| FR-08 | Dead-board recovery | When a stable board has no legal move, the system shall reshuffle or regenerate it before accepting further input. The recovered board shall meet DR-04, and recovery shall not change the score. | NEED-06, NEED-08 | Automated test that injects a dead board and validates the recovered state and unchanged score. |
| FR-09 | Gameplay feedback | The system shall visibly indicate the selected tile and whether an attempted move was rejected; accepted moves shall result in a visibly updated board. | NEED-03, NEED-04 | GUI inspection covering selection, rejection, and acceptance scenarios. |
| FR-10 | Restart | The system shall provide a restart control that sets the score to zero and creates a fresh board satisfying FR-01 without restarting the process. | NEED-05, NEED-06 | GUI acceptance test after scoring points and invoking restart. |
| FR-11 | Reproducible test state | The system shall provide a developer-only mechanism to use a fixed random seed or predefined board and refill sequence during automated testing. This mechanism shall not be required during normal play. | NEED-09, NEED-14 | Inspection and repeated test runs showing identical states and outcomes from identical test inputs. |

#### 2.2 Non-functional requirements

The non-functional requirements are categorized as **Product**, **Organizational**, or **External**. Product requirements constrain qualities of the delivered prototype; organizational requirements constrain project practices and artifacts; external requirements constrain interaction with the execution environment.

| ID | Subcategory | Requirement statement | Source need IDs | Verification method |
| --- | --- | --- | --- | --- |
| NFR-01 | Product — Usability | The system shall represent each of the six tile types with a distinct shape, symbol, or pattern in addition to any color difference, so color alone is not required to distinguish tiles. | NEED-03, NEED-04 | Visual inspection of all six tile types, including a grayscale view. |
| NFR-02 | Product — Performance | On the documented reference environment, the system shall display selection or rejection feedback within 100 milliseconds of a mouse action during a stable-board state. | NEED-17 | Instrumented response-time test over 100 input actions. |
| NFR-03 | Product — Performance | On the documented reference environment, initial board generation, dead-board recovery, and the non-visual processing for one complete cascade shall each finish within two seconds. | NEED-06, NEED-18 | Timed automated tests over a documented set of normal and worst-case controlled states. |
| NFR-04 | Product — Reliability | The system shall complete 1,000 controlled board-generation and resolution scenarios without an uncaught exception, unresolved empty cell, pre-existing match on a returned stable board, or stable board with no legal move. | NEED-14, NEED-18 | Automated stress test with recorded seeds and assertions. |
| NFR-05 | Product — Maintainability | The implementation shall separate core board and scoring logic from graphical input and rendering, and shall define board size, tile count, and points per tile once as named configuration values. | NEED-10, NEED-12, NEED-13 | Static code inspection and a change-impact exercise for each named value. |
| NFR-06 | Organizational — Documentation | Project documentation shall identify setup steps, the launch command, dependencies, supported operating system and runtime versions, gameplay rules, test command, and important design decisions. | NEED-11, NEED-12, NEED-16, NEED-20 | Documentation checklist review performed from a clean local setup. |
| NFR-07 | Organizational — Verification | The project shall include repeatable automated checks for initialization, legal and illegal swaps, long and intersecting matches, cascades, scoring, dead-board recovery, restart, and deterministic test setup. | NEED-09, NEED-14 | Execute the documented automated test command and inspect the reported cases. |
| NFR-08 | Organizational — Scope control | The prototype implementation and acceptance evidence shall be limited to the baseline and completion criteria in TODO 1; features explicitly listed there as out of scope shall not be required for acceptance. | NEED-10 | Scope review of implemented features and acceptance evidence against TODO 1. |
| NFR-09 | External — Offline operation | The system shall support normal play with networking disabled and shall not require an account, external service, or elevated operating-system privileges. | NEED-07, NEED-19 | Launch-and-play test with networking disabled under a standard user account. |
| NFR-10 | External — Compatibility | The system shall launch and complete the prototype acceptance scenarios on at least one explicitly documented desktop operating-system and runtime-version combination. | NEED-11, NEED-16, NEED-20 | Execute all acceptance scenarios on the documented supported combination. |
| NFR-11 | External — Startup diagnostics | If a required dependency is missing or the runtime version is unsupported, the launch attempt shall stop safely and present a message that identifies the missing or incompatible prerequisite. | NEED-15, NEED-16 | Negative launch tests with one prerequisite removed or replaced at a time. |
| NFR-12 | External — Host integrity | During normal play, the system shall not create persistent player or game-state data and shall not modify application-owned files outside its project directory; operating-system and runtime temporary artifacts are excluded. | NEED-07, NEED-19 | File-system snapshot comparison before and after a play session. |
| NFR-13 | Product — Reliability | When the player closes the game normally, the process shall terminate within two seconds without an uncaught exception or a remaining game process. | NEED-19 | Timed close test with process and error-output inspection. |

#### 2.3 Domain-specific requirements

These requirements capture rules inherent to the selected match-3 domain and define terms used by the functional requirements.

| ID | Category | Requirement statement | Source need IDs | Verification method |
| --- | --- | --- | --- | --- |
| DR-01 | Match-3 move rule | The system shall treat a swap as a legal move only when it exchanges two orthogonally adjacent tiles and the exchange creates at least one horizontal or vertical match. | NEED-01, NEED-02, NEED-08 | Table-driven tests covering legal, diagonal, non-adjacent, and matchless swaps. |
| DR-02 | Match definition | The system shall define a match as a contiguous horizontal or vertical run of at least three tiles of the same type. Runs longer than three shall be included in full, simultaneous matches shall all be included, and a cell at an intersection shall be included only once in that resolution step. | NEED-02, NEED-08 | Controlled-board tests for runs of three, four, and five; simultaneous runs; and T- or L-shaped intersections. |
| DR-03 | Resolution order | The system shall resolve a step in this order: clear all current matches simultaneously, score each distinct cleared cell once, move remaining tiles downward, refill empty cells, and then search again. The cycle shall repeat until no match remains. | NEED-02, NEED-08, NEED-18 | State-by-state automated cascade test with a predefined refill sequence. |
| DR-04 | Playable stable board | The system shall consider a board ready for player input only when all 64 cells are occupied, no match exists, and at least one legal move exists. | NEED-06, NEED-08 | Automated board predicate tests using valid, matched, incomplete, and dead boards. |
| DR-05 | Dead-board rule | The system shall treat a stable board with no legal move as a dead board requiring recovery rather than as the end of the endless prototype session. | NEED-06, NEED-08 | Controlled dead-board test followed by a continuity-of-play check. |
| DR-06 | Prototype scoring rule | The system shall award exactly 10 points per distinct tile cleared, with no cascade multiplier or special-tile bonus in the prototype. | NEED-02, NEED-05, NEED-08 | Score calculation tests across multiple match sizes and cascade depths. |

### 3. Traceability matrix

Every stakeholder need from TODO 2 maps to at least one user or system requirement. The matrix lists the principal derived requirements; additional supporting links are retained in the source columns above.

| Need ID | Derived requirement IDs |
| --- | --- |
| NEED-01 | UR-01, FR-02, FR-03, DR-01 |
| NEED-02 | UR-02, FR-01, FR-04, FR-05, FR-06, FR-07, DR-01, DR-02, DR-03, DR-06 |
| NEED-03 | UR-01, UR-03, FR-03, FR-04, FR-09, NFR-01 |
| NEED-04 | UR-03, FR-09, NFR-01 |
| NEED-05 | UR-04, FR-07, FR-10, DR-06 |
| NEED-06 | UR-05, FR-01, FR-08, FR-10, NFR-03, DR-04, DR-05 |
| NEED-07 | UR-06, NFR-09, NFR-12 |
| NEED-08 | UR-02, FR-01, FR-02, FR-03, FR-04, FR-05, FR-06, FR-07, FR-08, DR-01, DR-02, DR-03, DR-04, DR-05, DR-06 |
| NEED-09 | UR-07, FR-11, NFR-07 |
| NEED-10 | UR-08, NFR-05, NFR-08 |
| NEED-11 | UR-06, NFR-06, NFR-10 |
| NEED-12 | UR-08, NFR-05, NFR-06 |
| NEED-13 | UR-08, NFR-05 |
| NEED-14 | UR-07, FR-11, NFR-04, NFR-07 |
| NEED-15 | UR-08, NFR-11 |
| NEED-16 | UR-06, NFR-06, NFR-10, NFR-11 |
| NEED-17 | UR-09, NFR-02 |
| NEED-18 | UR-09, FR-06, NFR-03, NFR-04, DR-03 |
| NEED-19 | UR-06, NFR-09, NFR-12, NFR-13 |
| NEED-20 | UR-06, NFR-06, NFR-10 |

### 4. Overlaps, dependencies, and possible conflicts

#### Overlaps

- UR-01 through UR-09 state stakeholder-visible outcomes, while the FR, NFR, and DR entries refine those outcomes into verifiable system behavior. This is intentional refinement, not duplicate scope.
- FR-02 through FR-08 overlap with DR-01 through DR-06. The DR entries define the match-3 vocabulary and invariant rules; the FR entries define when the system applies those rules and what externally observable behavior results.
- NFR-06 and NFR-10 both refer to the supported environment. NFR-06 requires it to be documented, while NFR-10 requires the prototype to work on it.
- FR-11 and NFR-07 both support repeatable testing. FR-11 supplies controllable state; NFR-07 requires checks that use that capability.

#### Dependencies

- FR-01, FR-08, and FR-10 depend on the playable-board invariant in DR-04.
- FR-04 and FR-05 depend on the legal-move and match definitions in DR-01 and DR-02.
- FR-06 and FR-07 depend on the resolution order in DR-03 and the scoring rule in DR-06.
- NFR-02 and NFR-03 depend on NFR-06 identifying a reference environment on which timing is measured.
- NFR-04 and NFR-07 depend on FR-11 so randomized edge cases can be repeated.
- UR-06 depends jointly on documentation, compatibility, offline operation, host integrity, and clean shutdown rather than on a single system requirement.

#### Possible conflicts and resolutions

- **Random play versus reproducible testing:** Normal sessions may remain random, while FR-11 permits fixed seeds or predefined states only for development and automated verification. This preserves player variability without sacrificing defect reproduction.
- **Dead-board behavior versus an endless session:** TODO 1 allowed reshuffling or regeneration. FR-08 retains that implementation choice but fixes the observable outcome: the score is preserved and the replacement board is stable and playable.
- **Responsiveness versus visual effects:** Complex animation is out of scope. NFR-02 measures immediate input feedback, and NFR-03 measures non-visual board processing, so optional presentation delays cannot hide slow logic or violate the prototype scope.
- **Maintainable separation versus limited prototype effort:** NFR-05 requires only separation of core logic from the GUI and centralized baseline values. It does not require a large framework or speculative extension points.
- **Portability versus an unspecified target platform:** Universal portability is not assumed. NFR-06 and NFR-10 resolve the ambiguity by requiring at least one explicit supported desktop OS/runtime combination to be documented and verified before acceptance.
- **Diagnostic output versus no persistent data:** NFR-11 requires an understandable on-screen or console message, not a persistent log file. This remains compatible with NFR-12 and TODO 1's exclusion of saved data.
- **Stress-test termination versus random cascades:** NFR-03 and NFR-04 require bounded, successful processing. An implementation may control refills or regenerate an exceptional state, but it may not hang, return an incomplete board, or accept input on an invalid board.
