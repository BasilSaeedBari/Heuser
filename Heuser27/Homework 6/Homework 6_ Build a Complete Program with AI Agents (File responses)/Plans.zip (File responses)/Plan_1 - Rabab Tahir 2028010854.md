Stage: Core Logic
Architect model: Claude Opus    Builder model: Claude Sonnet
Result: Played start to finish in a headless-Chrome test (3 rounds, wrong pad ends the game, Play again restarts) with no console errors. Nothing broke at this stage.

# Plan 1 — Stage 1: Core Logic ("Pattern Memory")

Role: Architect. This document is the build specification for Stage 1 only. It contains no code. The builder implements exactly what is described here.

---

## 0. Goal of this stage

Produce a fully playable Simon-style game, start to finish, with plain visuals. A player can:

1. Open `index.html` by double-clicking (file:// protocol).
2. Press Start.
3. Watch a sequence of colored pads light up.
4. Repeat the sequence by clicking/tapping pads or pressing keys 1–4.
5. Advance through rounds (sequence grows by one each round).
6. Lose on a wrong input, see a Game Over message with final score.
7. Restart and play again without reloading the page.

Visual polish, animation, sound, and saved high scores are NOT part of this stage. They are only noted as extension points (Section 12).

---

## 1. Hard constraints (must be respected now and later)

| Rule | What it means for Stage 1 |
|---|---|
| Exactly 3 files | `/home/claude/hw6/build/index.html`, `/home/claude/hw6/build/style.css`, `/home/claude/hw6/build/script.js`. No other files in `build/`. |
| No assets | No images, sound files, font files, icons, SVG files. Pads are `<button>` elements colored by CSS. |
| No libraries / no internet | No CDN links, no `<link>` to Google Fonts, no frameworks. Plain DOM APIs only. |
| Works on double-click | No `type="module"`, no `import/export`, no `fetch`, no XHR, no service workers. `script.js` loaded with a classic `<script src="script.js" defer></script>`; `style.css` via `<link rel="stylesheet" href="style.css">`. Relative paths only. |
| Language level | Plain ES2015+ that runs in current Chrome/Firefox/Edge/Safari. `const`/`let`, arrow functions, template strings are fine. No transpile step. |
| No global leakage beyond one namespace | All logic lives inside a single IIFE or a single object; at most one global (`window.PatternMemory`) exposed for testing/extension (see Section 9). |

---

## 2. File responsibilities

### 2.1 `index.html`
- `<!DOCTYPE html>`, `<html lang="en">`, `<meta charset="utf-8">`, `<meta name="viewport" content="width=device-width, initial-scale=1">`, `<title>Pattern Memory</title>`.
- Static markup for all elements in Section 3 (the game must not need JS to *create* the pads; JS only wires behavior). This keeps ids stable for later stages.
- `<script src="script.js" defer></script>` at the end of `<head>` (or before `</body>` without `defer`). Pick `defer` in head.

### 2.2 `style.css`
Minimal, functional only:
- Pads: fixed size (e.g. 120×120 px), each a distinct solid background color, arranged in a 2×2 grid (CSS grid, `grid-template-columns: repeat(2, 120px)`, small gap).
- A `.lit` class that makes the active pad obviously different (e.g. much lighter color via `filter: brightness(1.8)` or an alternate background, plus a thick white/black outline). This must be visible without any transition (transitions are Stage 3).
- A `.locked` class on the board container that sets `cursor: not-allowed` (and optionally slightly reduced opacity) for pads while input is locked.
- `[hidden]` respected (browsers do it by default; do not override `display` on elements that use `hidden`).
- No custom fonts; use `font-family: sans-serif` / system defaults.

### 2.3 `script.js`
All game logic. Structure in Section 6–9.

---

## 3. DOM contract (ids and classes later stages will rely on)

These ids are a **public contract**. Later stages may restyle them but must not rename them.

```
body
└── main#app
    ├── h1#title                         "Pattern Memory"
    ├── section#hud
    │   ├── span#round-label   "Round: " + span#round-value   (initial "0")
    │   ├── span#score-label   "Score: " + span#score-value   (initial "0")
    │   └── p#status                     status message line (aria-live="polite")
    ├── div#board  (class "board")
    │   ├── button#pad-0  class="pad pad-green"  data-pad="0"  aria-label="Green pad (key 1)"   text "1"
    │   ├── button#pad-1  class="pad pad-red"    data-pad="1"  aria-label="Red pad (key 2)"     text "2"
    │   ├── button#pad-2  class="pad pad-yellow" data-pad="2"  aria-label="Yellow pad (key 3)"  text "3"
    │   └── button#pad-3  class="pad pad-blue"   data-pad="3"  aria-label="Blue pad (key 4)"    text "4"
    └── div#controls
        ├── button#start-btn            "Start"
        └── button#restart-btn  hidden  "Play again"
    (optional, same section) div#gameover-panel hidden
        ├── p#gameover-message          e.g. "Game over! You reached round 5."
        └── p#final-score               e.g. "Final score: 4"
```

Pad index → color → key mapping (fixed, single source of truth in JS as a constant array `PADS`):

| index | id | color name | CSS class | key |
|---|---|---|---|---|
| 0 | pad-0 | green | pad-green | `1` |
| 1 | pad-1 | red | pad-red | `2` |
| 2 | pad-2 | yellow | pad-yellow | `3` |
| 3 | pad-3 | blue | pad-blue | `4` |

Layout: 2×2 grid in DOM order → top-left green, top-right red, bottom-left yellow, bottom-right blue.

Pad numbers "1–4" are rendered as visible text on the pads so keyboard mapping is discoverable.

State is also mirrored on the root for CSS hooks: `#app` gets attribute `data-state="idle|showing|input|over"` updated on every transition (Stage 2/3 can style per state with zero JS changes).

---

## 4. Game rules (authoritative)

1. **Start**: game is in `idle`. Status reads "Press Start (or Enter) to play." Pads do nothing.
2. **New game** (Start pressed): `sequence = []`, `round = 0`, `score = 0`. Immediately begin round 1.
3. **Each round**:
   - Append ONE new random pad index (0–3) to `sequence`. The existing sequence is preserved (classic Simon: grows by one, never regenerated).
   - `round = sequence.length`.
   - Enter `showing`: play the full sequence back.
   - Enter `input`: player must reproduce the whole sequence from the beginning, in order.
4. **Input checking**: each player press is compared immediately to `sequence[inputIndex]`.
   - Correct and not last → `inputIndex++`, wait for next press.
   - Correct and last → round complete: `score += 1` (score = rounds fully completed), status "Correct!", brief pause, next round.
   - Wrong → game over immediately (no retry, no "strict mode" toggle in Stage 1).
5. **Score definition**: number of rounds completed successfully. So if you fail in round 5, score = 4. Round counter shows the round currently being played/failed.
6. **Repeats allowed**: the random generator may pick the same pad consecutively (true Simon behavior). The playback timing (Section 5) guarantees repeated pads are visibly distinct via a gap.
7. **No input timeout** in Stage 1 (player can think as long as they like). Noted as optional extension.
8. **Game over**: state `over`. Pads locked. Show `#gameover-panel` with round reached and final score. Hide `#start-btn`, show `#restart-btn`. Status "Game over."
9. **Restart**: `#restart-btn` (or Enter / Space while in `over`) starts a brand-new game exactly like Start (step 2). No page reload.
10. **Win condition**: none (endless). Optional cap `MAX_ROUNDS` constant is defined but set to `Infinity`; if a later stage wants a win, reaching it triggers a `win` path (not implemented now—just keep the constant).

---

## 5. Timing (playback and pacing)

All timing values are named constants in one `CONFIG` object at the top of `script.js` so later stages can tune them:

| Constant | Value | Meaning |
|---|---|---|
| `LIGHT_MS` | 600 | How long a pad stays lit during playback |
| `GAP_MS` | 250 | Dark gap between two lit pads (makes repeats visible) |
| `PRE_SHOW_DELAY_MS` | 700 | Pause after entering `showing` before first light (lets player get ready) |
| `ROUND_PAUSE_MS` | 900 | Pause after a correct full round before next playback |
| `PRESS_FLASH_MS` | 200 | How long a pad lights when the player presses it |
| `MIN_LIGHT_MS` | 250 | Floor for optional speed-up |
| `SPEEDUP_EVERY` | 5 | Optional: every 5 rounds, LIGHT_MS shrinks by `SPEEDUP_STEP_MS` (60) down to MIN_LIGHT_MS. Implement as a pure helper `getLightMs(round)`; if the builder runs short on time this can return `LIGHT_MS` constantly, the rest of the design is unaffected. |

Total playback time for round n ≈ `PRE_SHOW_DELAY_MS + n*LIGHT_MS + (n-1)*GAP_MS`.

### 5.1 Playback mechanism
- Use a **single chain of `setTimeout`s scheduled by a step function**, not `setInterval` and not a loop of pre-scheduled timeouts. The step function lights pad `sequence[i]`, schedules un-light after `lightMs`, then schedules step `i+1` after `GAP_MS`. After the last un-light, call `enterInput()`.
- Every timeout id is recorded in a `timers` array via a helper `schedule(fn, ms)`. A `clearTimers()` helper cancels all. `clearTimers()` is called on every transition to `idle` or `over` and at the start of `startGame()`. This prevents ghost lights if the player restarts mid-playback (possible only via keyboard shortcuts or later-stage UI; still must be safe).
- **Generation token**: `state.gameId` integer increments in `startGame()`. Each scheduled callback captures the id at scheduling time and returns early if `state.gameId` changed. Belt-and-braces with `clearTimers()`.

### 5.2 Player press flash
On a valid press during `input`: add `.lit` to the pad, schedule removal after `PRESS_FLASH_MS`. If the same pad is pressed again before removal, restart its flash (clear that pad's own flash timer first; keep a per-pad timer map `flashTimers[4]`). Flash is visual only and does NOT block further input.

---

## 6. State machine

### 6.1 States
`idle`, `showing`, `input`, `over`. Stored in `state.phase` (string constants in a frozen object `PHASE = { IDLE:'idle', SHOWING:'showing', INPUT:'input', OVER:'over' }`).

### 6.2 Transitions (the only legal ones)

| From | Event | To | Action |
|---|---|---|---|
| idle | Start (click / Enter / Space) | showing | `startGame()` → `nextRound()` |
| showing | playback finished | input | `enterInput()` |
| input | correct press, not last | input | `inputIndex++` |
| input | correct press, last | showing | `score++`, update HUD, after `ROUND_PAUSE_MS` → `nextRound()` |
| input | wrong press | over | `endGame()` |
| over | Restart (click / Enter / Space) | showing | `startGame()` → `nextRound()` |
| any | (Stage 1 no other events) | — | — |

Note: between the last correct press and the next playback the phase is set to `showing` *immediately* (input locked during the ROUND_PAUSE), not after the pause. This prevents an extra press during the pause being judged against the old sequence.

### 6.3 Single transition function
`setPhase(newPhase)`:
- Assigns `state.phase`.
- Sets `#app[data-state]`.
- Applies input lock: `#board` gets class `locked` and every pad gets `aria-disabled="true"` unless phase is `input`. (Do NOT use the `disabled` attribute on pads, because disabled buttons cannot be programmatically lit/styled consistently across browsers and swallow events used by later stages; lock is enforced in JS — Section 7.3.)
- Updates button visibility: Start visible only in `idle`; Restart visible only in `over`; game-over panel visible only in `over`.
- Updates `#status` text per phase via `STATUS_TEXT` map: idle "Press Start (or Enter) to play.", showing "Watch the pattern…", input "Your turn: repeat the pattern (keys 1–4).", over "Game over."
- Calls `emit('phase', newPhase)` (extension hook, Section 9).

All other code changes phase ONLY through `setPhase`.

---

## 7. Input handling

### 7.1 Pointer (mouse + touch)
- One listener on `#board` (event delegation) for `pointerdown`. Find the pad via `event.target.closest('.pad')`; read `Number(pad.dataset.pad)`.
- Use `pointerdown` (not `click`) so touch feels instant and there is no 300 ms delay or double fire. Call `event.preventDefault()` on pad pointerdowns to suppress the follow-up synthetic mouse events/focus ring jump on touch.
- Fallback: if `window.PointerEvent` is undefined, listen to `mousedown` and `touchstart` (with `preventDefault` in touchstart to avoid duplicate mousedown).
- Also add `touch-action: manipulation` to `.pad` in CSS (prevents double-tap zoom).
- Do **not** additionally listen to `click` on pads (would double-count). Keyboard activation of a focused pad via Enter/Space is handled by the keydown handler instead (Section 7.2), so `click` is not needed.

### 7.2 Keyboard
One `keydown` listener on `document`:
- Ignore if `event.repeat` is true (holding a key must not register multiple presses).
- Ignore if `event.ctrlKey || event.metaKey || event.altKey`.
- Keys `1`,`2`,`3`,`4` (check `event.key`; also accept `event.code` `Numpad1`–`Numpad4`, and `Digit1`–`Digit4`) → `handlePadInput(index)` with index 0–3.
- `Enter` or space (`' '`): if phase is `idle` → start; if `over` → restart; otherwise ignore. Call `preventDefault()` in these handled cases so a focused button doesn't also fire its own click (which would double-start). Guard anyway: `startGame()` is a no-op if phase is `showing` or `input`.
- All other keys: ignored, no preventDefault.

### 7.3 Input lock (central gate)
`handlePadInput(index)` is the only path from any device to game logic. Its first lines:
1. If `state.phase !== PHASE.INPUT` → return (ignored silently; optionally `emit('blockedInput', index)` for later stages to show a shake/tooltip).
2. Validate `index` is integer 0–3, else return.
Then flash the pad (5.2), `emit('press', index)`, and run the check in Section 4 rule 4.

Because the gate lives in one function, both pointer and keyboard are locked identically during `showing`, the round pause, `idle`, and `over`.

### 7.4 Buttons
- `#start-btn` `click` → `startGame()`.
- `#restart-btn` `click` → `startGame()`.
- After starting, move focus to `#board` (give `#board` `tabindex="-1"`) so pressing Space/Enter does not re-trigger the focused Start button; after game over, focus `#restart-btn` so Enter restarts naturally (the keydown handler's `preventDefault` + phase guard ensures no double start).

---

## 8. Function inventory (names are part of the contract)

All inside the IIFE. Pure helpers are marked (pure) and must not touch the DOM.

### Constants / data
- `CONFIG` — timing and limits (Section 5) + `MAX_ROUNDS: Infinity`, `PAD_COUNT: 4`.
- `PHASE` — frozen state names.
- `PADS` — `[{index:0,id:'pad-0',color:'green',key:'1'}, …]`.
- `STATUS_TEXT` — phase → string.

### State
Single object `state`:
```
state = {
  phase: 'idle',
  sequence: [],        // array of ints 0..3
  inputIndex: 0,       // position player must match next
  round: 0,
  score: 0,
  gameId: 0,
}
```
plus module-level `timers = []`, `flashTimers = [null,null,null,null]`, `els = {}` (cached DOM refs), `listeners = {}` (event hooks).

### Pure helpers
- `randomPad()` (pure-ish; uses `Math.random`) → int 0–3 via `Math.floor(Math.random()*CONFIG.PAD_COUNT)`. Isolated so tests/later stages can swap in a seeded RNG through `PatternMemory.setRandom(fn)`.
- `extendSequence(seq)` (pure) → returns a NEW array `seq.concat(randomPad())`.
- `checkInput(seq, inputIndex, padIndex)` (pure) → returns one of `'wrong' | 'correct' | 'complete'`.
- `getLightMs(round)` (pure) → playback light duration for that round.

### DOM helpers
- `cacheElements()` — fills `els` with every id from Section 3; throws a clear console error if any is missing.
- `lightPad(index)` / `unlightPad(index)` — add/remove `.lit`; `emit('light', index)` / `emit('unlight', index)`.
- `flashPad(index)` — press flash with per-pad timer.
- `renderHud()` — writes `state.round` to `#round-value`, `state.score` to `#score-value`.
- `setStatus(text)` — writes `#status`.
- `showGameOver()` / `hideGameOver()` — toggles `#gameover-panel` and fills messages.
- `setPhase(phase)` — Section 6.3.

### Timer helpers
- `schedule(fn, ms)` — wraps setTimeout with gameId guard, pushes id to `timers`, returns id.
- `clearTimers()` — clears all ids in `timers` and all `flashTimers`, then un-lights every pad.

### Flow
- `init()` — `cacheElements()`, attach listeners, `setPhase(PHASE.IDLE)`, `renderHud()`. Runs on `DOMContentLoaded` (or immediately if `defer` guarantees DOM; use `document.readyState` check to be safe).
- `startGame()` — guard: only from `idle` or `over`. `clearTimers()`, `state.gameId++`, reset sequence/round/score/inputIndex, `hideGameOver()`, `renderHud()`, `emit('start')`, `nextRound()`.
- `nextRound()` — `state.sequence = extendSequence(state.sequence)`, `state.round = state.sequence.length`, `state.inputIndex = 0`, `renderHud()`, `emit('round', state.round)`, `playSequence()`.
- `playSequence()` — `setPhase(SHOWING)`; schedule step 0 after `PRE_SHOW_DELAY_MS`; step function per 5.1; ends with `enterInput()`.
- `enterInput()` — `state.inputIndex = 0`, `setPhase(INPUT)`.
- `handlePadInput(index)` — Section 7.3; on `'correct'` → `inputIndex++`; on `'complete'` → `roundComplete()`; on `'wrong'` → `endGame(index)`.
- `roundComplete()` — `setPhase(SHOWING)` immediately (lock), `state.score++`, `renderHud()`, `setStatus('Correct! Get ready…')`, `emit('roundComplete', state.score)`, `schedule(nextRound, ROUND_PAUSE_MS)`. (If `state.round >= MAX_ROUNDS` → would call `winGame()`; not reachable with Infinity—leave a TODO comment only.)
- `endGame(wrongIndex)` — `clearTimers()`, `setPhase(OVER)`, `showGameOver()` with text "Game over! You reached round {round}." and "Final score: {score}", optionally flash the correct expected pad (`sequence[inputIndex]`) once so the player sees what they missed (use `lightPad` + schedule unlight after 800 ms — scheduled AFTER clearTimers, with current gameId), `emit('gameOver', {round, score, expected, got: wrongIndex})`, focus `#restart-btn`.

### Event handlers
- `onBoardPointerDown(e)`, `onKeyDown(e)`, `onStartClick()`, `onRestartClick()`.

---

## 9. Extension API (for Stages 2–5; minimal now)

Expose exactly one global: `window.PatternMemory = { on, getState, setRandom, CONFIG, PHASE }`.

- `on(eventName, handler)` — registers a listener; internal `emit(name, payload)` calls all handlers in try/catch so a broken extension can't crash the game.
- Events emitted in Stage 1: `phase`, `start`, `round`, `light`, `unlight`, `press`, `blockedInput`, `roundComplete`, `gameOver`.
- `getState()` — returns a shallow copy (`{...state, sequence: state.sequence.slice()}`), never the live object.
- `setRandom(fn)` — replace RNG (tests use it for deterministic sequences).
- `CONFIG` is exposed as the live object so a later "difficulty" setting can tweak timings.

Planned consumers (do NOT implement now):
| Stage | Hooks it will use |
|---|---|
| Theme/visual | `#app[data-state]`, `.pad-*`, `.lit`, `.locked` classes, ids in Section 3 |
| Animation | `light`/`unlight`/`press`/`gameOver` events; may replace `.lit` toggle with transitions in CSS only |
| Sound (Web Audio, generated tones) | `light` and `press` events → tone per pad index; `gameOver` → error tone. Requires user gesture: the Start click satisfies it. |
| Storage (localStorage high score) | `gameOver` payload `{score}`; new element `#best-value` to be added to `#hud` |

Stage 1 must not add placeholder UI for these.

---

## 10. Edge cases the builder must handle

1. Pressing pads or 1–4 in `idle`/`showing`/`over` → ignored, no flash, no state change.
2. Pressing during the `ROUND_PAUSE` after a correct round → ignored (phase already `showing`).
3. Holding down a key → counted once (`event.repeat` check).
4. Touch device: one tap = exactly one input (pointerdown only; no click listener on pads).
5. Same pad twice in a row in the sequence → visible as two separate lights separated by `GAP_MS`.
6. Rapid Start/Enter mashing → only one game starts (phase guard in `startGame`).
7. Restart while old timers pending (e.g. game-over reveal flash) → `clearTimers()` + gameId bump; no stray lights.
8. Window loses focus / tab hidden mid-playback → timers may be throttled; playback just resumes late. Acceptable for Stage 1 (note only).
9. Focus on a pad button + Enter → handled by keydown as start/restart only when idle/over; does not count as pad input (pads are only input via pointer or digit keys). Documented behavior.
10. Very long sequences (round 50+) → array growth trivial; no recursion (step function uses timeouts, not recursion depth).

---

## 11. Acceptance tests (manual; all must pass to call Stage 1 done)

Run by double-clicking `build/index.html` in Chrome and Firefox (and, if available, a phone or DevTools device emulation for touch). Open DevTools console: **zero errors** throughout.

Deterministic helper for testers (console): `PatternMemory.setRandom(() => 0)` makes every new pad green (index 0); a cycling stub like `let i=0; PatternMemory.setRandom(()=> (i++ % 4)/4)` yields 0,1,2,3,0,… (note: `setRandom` receives a function returning [0,1) exactly like Math.random).

| # | Test | Steps | Expected |
|---|---|---|---|
| T1 | Loads offline | Double-click index.html with network disabled | Title, 4 colored pads (green/red/yellow/blue, 2×2), Round 0, Score 0, Start button, status "Press Start…". No console errors. No network requests in Network tab. |
| T2 | File count | List `build/` | Exactly index.html, style.css, script.js. |
| T3 | Idle lock | Click pads and press 1–4 before Start | Nothing lights; round/score stay 0. |
| T4 | Start | Click Start | Start hides; status "Watch the pattern…"; Round shows 1; after ~0.7 s one pad lights ~0.6 s; then status "Your turn…". |
| T5 | Keyboard start | Reload, press Enter | Same as T4. Also Space. |
| T6 | Correct round | Repeat the shown pad (click) | Pad flashes briefly; Score 1; status "Correct!"; after ~0.9 s Round 2 plays 2 pads: the first is the same as round 1's pad. |
| T7 | Sequence growth/preservation | Play to round 4 with `setRandom` cycling stub | Playback in round 4 is green, red, yellow, blue (0,1,2,3); each round's sequence is a prefix-extension of the previous. |
| T8 | Keyboard input | Repeat sequences using keys 1–4 only | Works identically to clicking; mapping 1=green,2=red,3=yellow,4=blue. Numpad 1–4 also work. |
| T9 | Repeats visible | `setRandom(()=>0)`, play to round 3 | Green lights three separate times with clear dark gaps. |
| T10 | Lock during playback | During round ≥3 playback, mash pads and 1–4 | No flashes, no effect; after playback, input still expected from position 0 and correct entry succeeds. |
| T11 | Lock during round pause | Immediately after completing a round, press keys | Ignored; next playback proceeds normally. |
| T12 | Wrong input | At any input step press a wrong pad | Immediately: status "Game over."; panel shows "Game over! You reached round N." and "Final score: N-1"; Restart visible; Start hidden; expected pad briefly lit; pads locked. |
| T13 | Wrong mid-sequence | In round 3, enter first pad correctly, second wrong | Game over on the second press (not waiting for full length). Score = 2. |
| T14 | Score meaning | Fail in round 1 | Final score 0, round 1. |
| T15 | Restart | Click Play again | Panel hides; Round 1, Score 0; a fresh sequence of length 1 plays; full play works. |
| T16 | Keyboard restart | At game over press Enter | Restarts exactly once (Round 1, not 2; sequence length 1). |
| T17 | Key repeat | In input, hold a correct key down | Counts once. |
| T18 | Touch | In device emulation / phone, tap pads | One tap = one input; no double-tap zoom; no double count. |
| T19 | Mash start | Spam Enter / Start rapidly at idle | One game, Round 1, one playback. |
| T20 | Many games | Play 3 full games back-to-back without reload | Each starts clean; no stray lights; no console errors. |
| T21 | State attribute | Inspect `#app` during each phase | `data-state` goes idle → showing → input → showing → … → over. |
| T22 | Extension API | Console: `PatternMemory.on('press', console.log)` then play | Logs pad index for each accepted press; nothing logged for blocked presses. `PatternMemory.getState().sequence.push(9)` does not affect the game. |
| T23 | No globals | Console: compare `Object.keys(window)` before/after load (or inspect) | Only `PatternMemory` added by the game. |

Definition of done: T1–T23 pass; a non-developer can play from Start to Game Over to Play again without instructions beyond on-screen text.

---

## 12. Out of scope for Stage 1 (explicit)

- Any color theming, gradients, rounded/circular Simon layout, dark mode, responsive polish beyond "fits on a phone".
- CSS transitions/animations, shake effects, confetti.
- Sound (Web Audio oscillator tones) and mute toggle.
- localStorage high score / settings persistence.
- Difficulty selector, strict/non-strict modes, input timeout, win condition.
Each has its hook listed in Section 9; the builder must not stub UI for them.

---

## 13. Builder checklist (order of work)

1. Write `index.html` with exact ids from Section 3; verify it opens via file://.
2. Write minimal `style.css`: grid, four colors, `.lit`, `.locked`, `touch-action`.
3. In `script.js`: constants → state → pure helpers → DOM helpers → timers → `setPhase` → flow functions → handlers → `init` → expose `PatternMemory`.
4. Run T1–T23; fix; re-run T20 last.
5. Confirm `build/` contains exactly three files and no external references (search files for `http`, `import`, `fetch`, `.png`, `.mp3`, `.woff` → none).
