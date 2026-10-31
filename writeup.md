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
