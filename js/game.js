// Home page functionality and game start logic
function startGame() {
    document.querySelector('.home-container').style.display = 'none';  // Hide home page
    document.querySelector('.rules-container').style.display = 'none'; // Hide rules
    document.querySelector('.game-container').style.display = 'flex';  // Show game canvas
    showMobileControls(); // Show mobile controls only if on mobile
    initGame();
}

function showRules() {
    document.querySelector('.home-container').style.display = 'none';  // Hide home page
    document.querySelector('.rules-container').style.display = 'flex'; // Show rules
    document.querySelector('.mobile-controls').style.display = 'none'; // Hide mobile controls
}

function hideRules() {
    document.querySelector('.rules-container').style.display = 'none'; // Hide rules
    document.querySelector('.home-container').style.display = 'flex';  // Show home page
    document.querySelector('.mobile-controls').style.display = 'none'; // Hide mobile controls
}

// Game initialization logic
const canvas = document.getElementById("mazeCanvas");
const ctx = canvas.getContext("2d");

const CELL_SIZE = 20;
let COLS = 21;
let ROWS = 21;
canvas.width = COLS * CELL_SIZE;
canvas.height = ROWS * CELL_SIZE;

const WALL_COLOR = "#000000";
const PATH_COLOR = "#DCDCDC";
const PLAYER_COLOR = "#32C832";
const EXIT_COLOR = "#FF5733";

// Power-up settings
const POWERUP_COLOR = "#FFD700"; // Gold color for power-ups
let powerUps = [];

// Score system
let score = 0;

// Update the score display
function updateScore(points) {
    score += points;
    document.getElementById("scoreInfo").innerText = `Score: ${score}`;
}

let maze = Array.from({ length: ROWS }, () => Array(COLS).fill(0));
let player = { x: 1, y: 1 };
let exit = { x: COLS - 2, y: ROWS - 2 };

const DIRS = [
    [0, -2], [0, 2],
    [-2, 0], [2, 0]
];

function generateMaze(x = 1, y = 1) {
    maze[y][x] = 1;
    const dirs = [...DIRS].sort(() => Math.random() - 0.5);

    for (let [dx, dy] of dirs) {
        const nx = x + dx;
        const ny = y + dy;
        if (nx > 0 && nx < COLS - 1 && ny > 0 && ny < ROWS - 1 && maze[ny][nx] === 0) {
            maze[y + dy / 2][x + dx / 2] = 1;
            generateMaze(nx, ny);
        }
    }
}

// Generate power-ups based on maze difficulty
function generatePowerUps() {
    powerUps = [];
    const numPowerUps = Math.floor((COLS + ROWS) / 10); // Number of power-ups increases with maze size
    for (let i = 0; i < numPowerUps; i++) {
        let x, y;
        do {
            x = Math.floor(Math.random() * COLS);
            y = Math.floor(Math.random() * ROWS);
        } while (!isWalkable(x, y) || (x === player.x && y === player.y) || (x === exit.x && y === exit.y));
        powerUps.push({ x, y });
    }
}

function drawMaze() {
    for (let y = 0; y < ROWS; y++) {
        for (let x = 0; x < COLS; x++) {
            ctx.fillStyle = maze[y][x] === 1 ? PATH_COLOR : WALL_COLOR;
            ctx.fillRect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE);
        }
    }
}

// Draw power-ups on the maze
function drawPowerUps() {
    ctx.fillStyle = POWERUP_COLOR;
    powerUps.forEach(({ x, y }) => {
        ctx.beginPath();
        ctx.arc(x * CELL_SIZE + CELL_SIZE / 2, y * CELL_SIZE + CELL_SIZE / 2, CELL_SIZE / 3, 0, Math.PI * 2);
        ctx.fill();
    });
}

function drawPlayer() {
    ctx.fillStyle = PLAYER_COLOR;
    ctx.fillRect(player.x * CELL_SIZE, player.y * CELL_SIZE, CELL_SIZE, CELL_SIZE);
}

function drawExit() {
    ctx.fillStyle = EXIT_COLOR;
    ctx.fillRect(exit.x * CELL_SIZE, exit.y * CELL_SIZE, CELL_SIZE, CELL_SIZE);
}

function isWalkable(x, y) {
    return x >= 0 && y >= 0 && x < COLS && y < ROWS && maze[y][x] === 1;
}

// Adjust estimated time for human reaction
function findMinTimeToWin() {
    const queue = [];
    const visited = Array.from({ length: ROWS }, () => Array(COLS).fill(false));
    const directions = [[1, 0], [-1, 0], [0, 1], [0, -1]];

    queue.push({ x: 1, y: 1, dist: 0 });
    visited[1][1] = true;

    while (queue.length > 0) {
        const { x, y, dist } = queue.shift();
        

        if (x === exit.x && y === exit.y) {
            const moveDelay = 0.1; // in seconds (100ms per move)
            const baseTime = 10; // Base time for human reaction
            const hardnessFactor = Math.floor((COLS + ROWS) / 10); // Adjust based on maze size
            const time = (dist * moveDelay + baseTime + hardnessFactor).toFixed(2); // Add base time and hardness factor
            console.log(`Minimum steps: ${dist}, Estimated minimum time: ${time} seconds`);
            
            return { steps: dist, timeInSeconds: parseFloat(time) };
        }

        for (let [dx, dy] of directions) {
            const nx = x + dx;
            const ny = y + dy;
            if (isWalkable(nx, ny) && !visited[ny][nx]) {
                visited[ny][nx] = true;
                queue.push({ x: nx, y: ny, dist: dist + 1 });
            }
        }
    }

    return { steps: -1, timeInSeconds: -1 }; // No path found
}

// Check if the player collects a power-up
function checkPowerUpCollection() {
    powerUps = powerUps.filter(({ x, y }) => {
        if (player.x === x && player.y === y) {
            remainingTime += 5; // Add 5 seconds for each power-up collected
            updateScore(5); // Add 5 points for collecting a power-up
            document.getElementById("minTimeInfo").innerText = `Time left: ${remainingTime.toFixed(1)} sec`;
            return false; // Remove the collected power-up
        }
        return true;
    });
}

// Update the draw function to include power-ups
function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    drawMaze();
    drawPlayer();
    drawExit();
    drawPowerUps();
}

// Update the keydown event listener for instant movement
document.addEventListener("keydown", e => {
    let dx = 0, dy = 0;
    if (e.key === "ArrowLeft") dx = -1;
    else if (e.key === "ArrowRight") dx = 1;
    else if (e.key === "ArrowUp") dy = -1;
    else if (e.key === "ArrowDown") dy = 1;

    const nx = player.x + dx;
    const ny = player.y + dy;

    if (isWalkable(nx, ny)) {
        player.x = nx;
        player.y = ny;
        checkPowerUpCollection(); // Check if the player collects a power-up
    }

    if (player.x === exit.x && player.y === exit.y) {
        updateScore(10); // Add 10 points for winning
        showPopup("You won! Generating a harder maze...");
        increaseDifficulty();
    }

    draw();
});

// Handle on-screen button clicks for mobile controls
function movePlayer(direction) {
    let dx = 0, dy = 0;
    if (direction === 'up') dy = -1;
    else if (direction === 'down') dy = 1;
    else if (direction === 'left') dx = -1;
    else if (direction === 'right') dx = 1;

    const nx = player.x + dx;
    const ny = player.y + dy;

    if (isWalkable(nx, ny)) {
        player.x = nx;
        player.y = ny;
        checkPowerUpCollection(); // Check if the player collects a power-up
    }

    if (player.x === exit.x && player.y === exit.y) {
        updateScore(10); // Add 10 points for winning
        showPopup("You won! Generating a harder maze...");
        increaseDifficulty();
    }

    draw();
}

// Detect device orientation and show a message if not in landscape mode
function checkOrientation() {
    const orientationMessage = document.getElementById("orientationMessage");
    if (window.innerWidth < window.innerHeight) {
        // Portrait mode
        orientationMessage.style.display = "block";
    } else {
        // Landscape mode
        orientationMessage.style.display = "none";
    }
}

// Show a popup message
function showPopup(message) {
    const popup = document.getElementById("popup");
    const popupMessage = document.getElementById("popupMessage");
    popupMessage.innerText = message;
    popup.style.display = "flex";
}

// Close the popup
function closePopup() {
    const popup = document.getElementById("popup");
    popup.style.display = "none";
}

// Show mobile controls if the device is a mobile phone
function showMobileControls() {
    const isMobile = /iPhone|iPad|iPod|Android/i.test(navigator.userAgent);
    if (isMobile) {
        document.querySelector('.mobile-controls').style.display = 'flex';
    } else {
        document.querySelector('.mobile-controls').style.display = 'none';
    }
}

// Toggle control button position between left and right
function toggleControlPosition() {
    const controls = document.querySelector('.mobile-controls');
    if (controls.classList.contains('left')) {
        controls.classList.remove('left');
        controls.classList.add('right');
    } else {
        controls.classList.remove('right');
        controls.classList.add('left');
    }
}

// Add event listeners for orientation change and page load
window.addEventListener("resize", checkOrientation);
window.addEventListener("load", () => {
    checkOrientation();
    document.querySelector('.mobile-controls').style.display = 'none'; // Ensure buttons are hidden on load
});

// Increase movement speed and ensure win within estimated time
let timerInterval;
let remainingTime;

function startTimer(duration) {
    remainingTime = duration;
    document.getElementById("minTimeInfo").innerText = `Time left: ${remainingTime.toFixed(1)} sec`;

    timerInterval = setInterval(() => {
        remainingTime -= 0.1;
        document.getElementById("minTimeInfo").innerText = `Time left: ${remainingTime.toFixed(1)} sec`;

        if (remainingTime <= 0) {
            clearInterval(timerInterval);
            showPopup("Time's up! You lost. Try again.");
            resetGame();
        }
    }, 100); // Update every 100ms
}

function resetGame() {
    COLS = 21;
    ROWS = 21;
    canvas.width = COLS * CELL_SIZE;
    canvas.height = ROWS * CELL_SIZE;
    maze = Array.from({ length: ROWS }, () => Array(COLS).fill(0));
    generateMaze();
    generatePowerUps(); // Generate power-ups
    player = { x: 1, y: 1 };
    exit = { x: COLS - 2, y: ROWS - 2 };

    const result = findMinTimeToWin();
    startTimer(result.timeInSeconds);
    draw();
}

// Update the increaseDifficulty function to include power-ups
function increaseDifficulty() {
    COLS += 2;
    ROWS += 2;
    canvas.width = COLS * CELL_SIZE;
    canvas.height = ROWS * CELL_SIZE;
    maze = Array.from({ length: ROWS }, () => Array(COLS).fill(0));
    generateMaze();
    generatePowerUps(); // Generate new power-ups
    player = { x: 1, y: 1 };
    exit = { x: COLS - 2, y: ROWS - 2 };

    const result = findMinTimeToWin();
    startTimer(result.timeInSeconds);
    draw();
}

// Update the initGame function to include power-ups
function initGame() {
    generateMaze();
    generatePowerUps(); // Generate power-ups
    draw();
    const result = findMinTimeToWin();
    startTimer(result.timeInSeconds);
}
