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
