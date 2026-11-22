import os
import zipfile

folder_name = "HW6_Muhammad_Zayaam_2028010101"
os.makedirs(folder_name, exist_ok=True)

files = {
"Plan_1.md": """Stage: 1. Core Logic
Architect model: GPT-4o
Builder model: Claude 3.5 Sonnet
Result: Successfully created the basic game loop, player movement, and collision detection. The game runs from start to finish with basic shapes.

Plan:
- HTML: Create a basic structure with a <canvas> element for the game, and a <div> for the UI (score).
- CSS: Set the canvas to fill the screen and give it a simple black background to represent space.
- JS:
  - Set up the Canvas 2D context.
  - Create a Player object (a simple blue rectangle at the bottom). Map Left/Right arrow keys to move it.
  - Create an Item object array. Items spawn at the top and fall down. There are two types: 'good' (star) and 'bad' (bomb).
  - Implement a requestAnimationFrame game loop to update positions and draw to the canvas.
  - Implement collision detection. If player hits 'good', increase score. If player hits 'bad', trigger Game Over.
  - Add a Game Over screen with a "Restart" button. Clicking it resets the score and item array.""",

"Plan_2.md": """Stage: 2. Visual Vibe
Architect model: GPT-4o
Builder model: Claude 3.5 Sonnet
Result: Replaced basic rectangles with code-drawn shapes. Implemented a retro space theme with zero external image files.

Plan:
- Theme: Retro 8-bit space arcade.
- Palette: Deep space blue (#0b0c10), neon cyan (#66fcf1), bright yellow (#f3ca20), and warning red (#ff4c4c).
- HTML/CSS: Use a monospace font. Style the score UI to look like a digital LED display.
- JS Canvas Drawing:
  - Draw the player as a spaceship using beginPath, moveTo, lineTo.
  - Draw the 'good' item as a 4-pointed star (yellow diamond).
  - Draw the 'bad' item as a circle with a small line on top (a bomb).
  - Add a static starry background generated randomly via JS arrays.""",

"Plan_3.md": """Stage: 3. Sensory Feedback
Architect model: GPT-4o
Builder model: Claude 3.5 Sonnet
Result: Added particle effects for explosions and catches. Implemented code-generated sound using the Web Audio API and a mute button.

Plan:
- Visuals: Add a particle system. When a good item is caught, spawn yellow particles that fade out. When a bomb hits, spawn red/orange particles. Add engine exhaust flames to the player ship.
- Audio: Use AudioContext (Web Audio API).
  - For 'catch': Use an oscillator to play a high-pitch short sine wave.
  - For 'explosion': Use a noise buffer passed through a lowpass filter.
- Controls: Add a "Mute" button to the HTML UI. Clicking it toggles a boolean isMuted variable. Handle browser autoplay policies by starting audio context on first click.""",

"Plan_4.md": """Stage: 4. State & Storage
Architect model: GPT-4o
Builder model: Claude 3.5 Sonnet
Result: Implemented local storage for high scores and added a pause menu. Game states are now properly managed.

Plan:
- Storage: Use localStorage to save and load the highScore.
- UI: Add a High Score display next to the current score.
- Game States: Implement a state machine with states: START, PLAYING, GAMEOVER.
- Features:
  - Start Screen: Shows instructions and a "Start" button.
  - Reset: Add a button to clear the high score from local storage.
  - Data persistence handles page refreshes without losing the high score.""",

"Plan_5.md": """Stage: 5. Debugging
Architect model: GPT-4o
Builder model: Claude 3.5 Sonnet
Result: Found and fixed 3 real bugs relating to timing, audio contexts, and resizing.

Plan & Bug List:
- Bug 1 (Audio Autoplay Block): The browser blocked audio from playing on page load.
  - Fix: Moved the AudioContext initialization into a function that triggers on the very first user interaction (clicking the "Start Game" button).
- Bug 2 (Resize Distortion): Resizing the browser window stretched the canvas and messed up click coordinates.
  - Fix: Added an event listener for window.resize. The canvas width/height are updated dynamically, and internal drawing coordinates scale proportionally.
- Bug 3 (Double Scoring): Rapidly moving over an item triggered collision twice in one frame.
  - Fix: Added a hasBeenScored boolean flag to each item. Once collided with, set it to true and immediately remove the item from the array.""",

"index.html": """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Space Catcher</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div id="game-container">
        <div id="ui">
            <div class="score-board">SCORE: <span id="score">0</span></div>
            <div class="score-board">HIGH: <span id="high-score">0</span></div>
            <div class="controls">
                <button id="mute-btn">🔊 Sound On</button>
                <button id="reset-btn">Reset High Score</button>
            </div>
        </div>
        <canvas id="gameCanvas"></canvas>
        
        <div id="start-screen" class="overlay">
            <h1>SPACE CATCHER</h1>
            <p>Use Left and Right arrows to move.</p>
            <p>Catch the <span style="color: #f3ca20">Stars</span>, avoid the <span style="color: #ff4c4c">Bombs</span>!</p>
            <button id="start-btn">Start Game</button>
        </div>

        <div id="game-over-screen" class="overlay hidden">
            <h1>GAME OVER</h1>
            <p>Your Score: <span id="final-score">0</span></p>
            <button id="restart-btn">Play Again</button>
        </div>
    </div>
    <script src="script.js"></script>
</body>
</html>""",

"style.css": """* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
    user-select: none;
}

body {
    background-color: #0b0c10;
    color: #66fcf1;
    font-family: 'Courier New', Courier, monospace;
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    overflow: hidden;
}

#game-container {
    position: relative;
    width: 100%;
    max-width: 800px;
    height: 100%;
    max-height: 600px;
    box-shadow: 0 0 20px rgba(102, 252, 241, 0.2);
}

canvas {
    display: block;
    width: 100%;
    height: 100%;
    background-color: #000;
}

#ui {
    position: absolute;
    top: 10px;
    left: 10px;
    right: 10px;
    display: flex;
    justify-content: space-between;
    pointer-events: none;
    z-index: 10;
}

.score-board {
    font-size: 20px;
    font-weight: bold;
    text-shadow: 0 0 5px #66fcf1;
}

.controls {
    pointer-events: auto;
    display: flex;
    gap: 10px;
}

button {
    background-color: transparent;
    border: 2px solid #66fcf1;
    color: #66fcf1;
    padding: 5px 10px;
    font-family: inherit;
    font-weight: bold;
    cursor: pointer;
    transition: all 0.2s;
}

button:hover {
    background-color: #66fcf1;
    color: #0b0c10;
}

.overlay {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(11, 12, 16, 0.9);
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
    z-index: 20;
}

.overlay h1 {
    font-size: 48px;
    margin-bottom: 20px;
    text-shadow: 0 0 10px #66fcf1;
}

.overlay p {
    font-size: 18px;
    margin-bottom: 10px;
    color: #c5c6c7;
}

.overlay button {
    margin-top: 20px;
    font-size: 20px;
    padding: 10px 20px;
}

.hidden {
    display: none !important;
}""",

"script.js": """const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');
const scoreEl = document.getElementById('score');
const highScoreEl = document.getElementById('high-score');
const startScreen = document.getElementById('start-screen');
const gameOverScreen = document.getElementById('game-over-screen');
const finalScoreEl = document.getElementById('final-score');
const startBtn = document.getElementById('start-btn');
const restartBtn = document.getElementById('restart-btn');
const muteBtn = document.getElementById('mute-btn');
const resetBtn = document.getElementById('reset-btn');

let width = canvas.width = canvas.offsetWidth;
let height = canvas.height = canvas.offsetHeight;
let score = 0;
let highScore = localStorage.getItem('spaceCatcherHighScore') || 0;
highScoreEl.innerText = highScore;
let gameState = 'START';
let isMuted = false;

const player = { x: width / 2, y: height - 50, width: 40, height: 40, speed: 7 };
let items = [];
let particles = [];
let stars = [];
for (let i = 0; i < 50; i++) { stars.push({ x: Math.random() * width, y: Math.random() * height, size: Math.random() * 2, speed: Math.random() * 2 + 0.5 }); }

const keys = { ArrowLeft: false, ArrowRight: false };
window.addEventListener('keydown', (e) => { if (e.key === 'ArrowLeft') keys.ArrowLeft = true; if (e.key === 'ArrowRight') keys.ArrowRight = true; });
window.addEventListener('keyup', (e) => { if (e.key === 'ArrowLeft') keys.ArrowLeft = false; if (e.key === 'ArrowRight') keys.ArrowRight = false; });
window.addEventListener('resize', () => { width = canvas.width = canvas.offsetWidth; height = canvas.height = canvas.offsetHeight; player.y = height - 50; if (player.x > width) player.x = width / 2; });

let audioCtx;
function initAudio() { if (!audioCtx) { audioCtx = new (window.AudioContext || window.webkitAudioContext)(); } }
function playSound(type) {
    if (isMuted || !audioCtx) return;
    const oscillator = audioCtx.createOscillator();
    const gainNode = audioCtx.createGain();
    oscillator.connect(gainNode);
    gainNode.connect(audioCtx.destination);
    if (type === 'catch') {
        oscillator.type = 'sine'; oscillator.frequency.setValueAtTime(800, audioCtx.currentTime); oscillator.frequency.exponentialRampToValueAtTime(1200, audioCtx.currentTime + 0.1);
        gainNode.gain.setValueAtTime(0.5, audioCtx.currentTime); gainNode.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.1);
        oscillator.start(); oscillator.stop(audioCtx.currentTime + 0.1);
    } else if (type === 'explosion') {
        oscillator.type = 'sawtooth'; oscillator.frequency.setValueAtTime(150, audioCtx.currentTime); oscillator.frequency.exponentialRampToValueAtTime(50, audioCtx.currentTime + 0.3);
        gainNode.gain.setValueAtTime(1, audioCtx.currentTime); gainNode.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.3);
        oscillator.start(); oscillator.stop(audioCtx.currentTime + 0.3);
    }
}

class Item {
    constructor() { this.radius = 15; this.x = Math.random() * (width - this.radius * 2) + this.radius; this.y = -20; this.speed = Math.random() * 3 + 2; this.type = Math.random() > 0.3 ? 'good' : 'bad'; this.scored = false; }
    draw() {
        ctx.beginPath();
        if (this.type === 'good') { ctx.fillStyle = '#f3ca20'; ctx.moveTo(this.x, this.y - this.radius); ctx.lineTo(this.x + this.radius, this.y); ctx.lineTo(this.x, this.y + this.radius); ctx.lineTo(this.x - this.radius, this.y); ctx.closePath(); }
        else { ctx.fillStyle = '#ff4c4c'; ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2); }
        ctx.fill(); ctx.closePath();
    }
    update() { this.y += this.speed; }
}

class Particle {
    constructor(x, y, color) { this.x = x; this.y = y; this.vx = (Math.random() - 0.5) * 6; this.vy = (Math.random() - 0.5) * 6; this.life = 1.0; this.color = color; }
    update() { this.x += this.vx; this.y += this.vy; this.life -= 0.03; }
    draw() { ctx.globalAlpha = this.life; ctx.fillStyle = this.color; ctx.beginPath(); ctx.arc(this.x, this.y, 3, 0, Math.PI * 2); ctx.fill(); ctx.globalAlpha = 1.0; }
}

function drawPlayer() {
    ctx.fillStyle = '#66fcf1'; ctx.beginPath(); ctx.moveTo(player.x, player.y - player.height / 2); ctx.lineTo(player.x + player.width / 2, player.y + player.height / 2); ctx.lineTo(player.x - player.width / 2, player.y + player.height / 2); ctx.closePath(); ctx.fill();
    ctx.fillStyle = '#ff4c4c'; ctx.beginPath(); ctx.moveTo(player.x - 5, player.y + player.height / 2); ctx.lineTo(player.x + 5, player.y + player.height / 2); ctx.lineTo(player.x, player.y + player.height / 2 + Math.random() * 10 + 5); ctx.closePath(); ctx.fill();
}

function updatePlayer() { if (keys.ArrowLeft && player.x > player.width / 2) player.x -= player.speed; if (keys.ArrowRight && player.x < width - player.width / 2) player.x += player.speed; }

function handleCollisions() {
    for (let i = items.length - 1; i >= 0; i--) {
        const item = items[i];
        const distX = Math.abs(item.x - player.x); const distY = Math.abs(item.y - player.y);
        if (distX < (player.width / 2 + item.radius) && distY < (player.height / 2 + item.radius)) {
            if (!item.scored) {
                item.scored = true;
                if (item.type === 'good') { score += 10; scoreEl.innerText = score; playSound('catch'); createParticles(item.x, item.y, '#f3ca20'); items.splice(i, 1); }
                else { playSound('explosion'); createParticles(item.x, item.y, '#ff4c4c'); gameOver(); return; }
            }
        }
        if (item.y > height + 30) items.splice(i, 1);
    }
}

function createParticles(x, y, color) { for (let i = 0; i < 15; i++) particles.push(new Particle(x, y, color)); }

function gameOver() { gameState = 'GAMEOVER'; if (score > highScore) { highScore = score; localStorage.setItem('spaceCatcherHighScore', highScore); highScoreEl.innerText = highScore; } finalScoreEl.innerText = score; gameOverScreen.classList.remove('hidden'); }

function resetGame() { score = 0; scoreEl.innerText = score; items = []; particles = []; player.x = width / 2; gameState = 'PLAYING'; gameOverScreen.classList.add('hidden'); startScreen.classList.add('hidden'); initAudio(); }

function gameLoop() {
    if (gameState === 'PLAYING') {
        ctx.clearRect(0, 0, width, height);
        ctx.fillStyle = '#fff';
        stars.forEach(star => { star.y += star.speed; if (star.y > height) star.y = 0; ctx.beginPath(); ctx.arc(star.x, star.y, star.size, 0, Math.PI * 2); ctx.fill(); });
        updatePlayer(); drawPlayer();
        if (Math.random() < 0.03) items.push(new Item());
        items.forEach(item => { item.update(); item.draw(); });
        handleCollisions();
        for (let i = particles.length - 1; i >= 0; i--) { particles[i].update(); particles[i].draw(); if (particles[i].life <= 0) particles.splice(i, 1); }
    }
    requestAnimationFrame(gameLoop);
}

startBtn.addEventListener('click', () => { initAudio(); resetGame(); });
restartBtn.addEventListener('click', () => { resetGame(); });
muteBtn.addEventListener('click', () => { isMuted = !isMuted; muteBtn.innerText = isMuted ? "🔇 Sound Off" : "🔊 Sound On"; });
resetBtn.addEventListener('click', () => { localStorage.removeItem('spaceCatcherHighScore'); highScore = 0; highScoreEl.innerText = highScore; });
requestAnimationFrame(gameLoop);"""
}

# 1. Save the 5 Plan Markdown files
for i in range(1, 6):
    filename = f"Plan_{i}.md"
    with open(os.path.join(folder_name, filename), 'w', encoding='utf-8') as f:
        f.write(files[filename])

# 2. Save the 3 Code files to the folder
for code_file in ["index.html", "style.css", "script.js"]:
    with open(os.path.join(folder_name, code_file), 'w', encoding='utf-8') as f:
        f.write(files[code_file])

# 3. Create the Zip file containing ONLY the 3 code files
zip_path = os.path.join(folder_name, "HW6_Muhammad_Zayaam_2028010101.zip")
with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
    zipf.write(os.path.join(folder_name, "index.html"), "index.html")
    zipf.write(os.path.join(folder_name, "style.css"), "style.css")
    zipf.write(os.path.join(folder_name, "script.js"), "script.js")

print(f"SUCCESS! All 6 files have been created in the folder: {folder_name}")