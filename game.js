// Game constants
const CANVAS_WIDTH = 600;
const CANVAS_HEIGHT = 400;
const PADDLE_WIDTH = 10;
const PADDLE_HEIGHT = 60;
const BALL_SIZE = 15;
const PADDLE_SPEED = 6;
const BASE_BALL_SPEED = 4;
const FPS = 60;

// Colors
const COLORS = {
    WHITE: '#ffffff',
    BLACK: '#000000',
    BLUE: '#1e90ff',
    GREEN: '#00ff80',
    RED: '#ff4040',
    YELLOW: '#ffff00',
    ORANGE: '#ffa500'
};

// Game state
let gameState = {
    currentScreen: 'menu', // 'menu', 'game', 'instructions', 'highScore', 'achievements'
    selectedOption: 0,
    menuOptions: ['Play Game', 'High Score', 'Achievements', 'Music: ON', 'Instructions', 'Quit'],
    musicEnabled: true
};

// Game objects
let paddle = {
    x: 0,
    y: CANVAS_HEIGHT / 2 - PADDLE_HEIGHT / 2,
    width: PADDLE_WIDTH,
    height: PADDLE_HEIGHT
};

let ball = {
    x: CANVAS_WIDTH / 2,
    y: CANVAS_HEIGHT / 2,
    size: BALL_SIZE,
    velX: -BASE_BALL_SPEED,
    velY: BASE_BALL_SPEED
};

// Game variables
let score = 0;
let highScore = localStorage.getItem('bounceMasterHighScore') || 0;
let speedLevel = 1;
let gameRunning = false;
let gamePaused = false;

// Achievements
const ACHIEVEMENTS = {
    1: { name: "First Hit", description: "Score your first point", color: COLORS.GREEN },
    5: { name: "Beginner", description: "Score 5 points", color: COLORS.YELLOW },
    10: { name: "Amateur", description: "Score 10 points", color: COLORS.ORANGE },
    25: { name: "Pro", description: "Score 25 points", color: COLORS.RED },
    50: { name: "Master", description: "Score 50 points", color: COLORS.BLUE },
    100: { name: "Legend", description: "Score 100 points", color: COLORS.GREEN },
    200: { name: "Unstoppable", description: "Score 200 points", color: COLORS.YELLOW }
};

let earnedAchievements = JSON.parse(localStorage.getItem('bounceMasterAchievements') || '[]');

// Canvas setup
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

// Input handling
const keys = {};
let selectedMenuOption = 0;

// Initialize game
function init() {
    updateUI();
    showMenu();
    setupEventListeners();
    gameLoop();
}

// Event listeners
function setupEventListeners() {
    document.addEventListener('keydown', handleKeyDown);
    document.addEventListener('keyup', handleKeyUp);
    
    // Menu option clicks
    document.querySelectorAll('.menu-option').forEach((option, index) => {
        option.addEventListener('click', () => {
            selectedMenuOption = index;
            handleMenuSelection();
        });
    });
}

function handleKeyDown(e) {
    keys[e.key] = true;
    
    if (gameState.currentScreen === 'menu') {
        handleMenuInput(e);
    } else if (gameState.currentScreen === 'game') {
        handleGameInput(e);
    }
}

function handleKeyUp(e) {
    keys[e.key] = false;
}

function handleMenuInput(e) {
    if (e.key === 'ArrowUp') {
        selectedMenuOption = (selectedMenuOption - 1 + gameState.menuOptions.length) % gameState.menuOptions.length;
        updateMenuSelection();
    } else if (e.key === 'ArrowDown') {
        selectedMenuOption = (selectedMenuOption + 1) % gameState.menuOptions.length;
        updateMenuSelection();
    } else if (e.key === 'Enter') {
        handleMenuSelection();
    }
}

function handleGameInput(e) {
    if (e.key === ' ') {
        togglePause();
    }
}

function handleMenuSelection() {
    const action = gameState.menuOptions[selectedMenuOption].toLowerCase().replace(' ', '');
    
    switch(action) {
        case 'playgame':
            startGame();
            break;
        case 'highscore':
            showHighScore();
            break;
        case 'achievements':
            showAchievements();
            break;
        case 'music:on':
        case 'music:off':
            toggleMusic();
            break;
        case 'instructions':
            showInstructions();
            break;
        case 'quit':
            // In web version, just hide the game
            hideAllScreens();
            showMenu();
            break;
    }
}

// Menu functions
function showMenu() {
    gameState.currentScreen = 'menu';
    hideAllScreens();
    document.getElementById('menuOverlay').classList.remove('hidden');
    updateMenuSelection();
}

function updateMenuSelection() {
    document.querySelectorAll('.menu-option').forEach((option, index) => {
        if (index === selectedMenuOption) {
            option.classList.add('selected');
        } else {
            option.classList.remove('selected');
        }
    });
}

function hideAllScreens() {
    document.getElementById('menuOverlay').classList.add('hidden');
    document.getElementById('instructionsOverlay').classList.add('hidden');
    document.getElementById('highScoreOverlay').classList.add('hidden');
    document.getElementById('achievementsOverlay').classList.add('hidden');
    document.getElementById('achievementPopup').classList.add('hidden');
}

function showInstructions() {
    gameState.currentScreen = 'instructions';
    hideAllScreens();
    document.getElementById('instructionsOverlay').classList.remove('hidden');
    
    // Wait for any key to go back
    const handleKey = () => {
        document.removeEventListener('keydown', handleKey);
        showMenu();
    };
    document.addEventListener('keydown', handleKey);
}

function showHighScore() {
    gameState.currentScreen = 'highScore';
    hideAllScreens();
    document.getElementById('highScoreOverlay').classList.remove('hidden');
    document.getElementById('highScoreDisplay').textContent = highScore;
    
    // Wait for any key to go back
    const handleKey = () => {
        document.removeEventListener('keydown', handleKey);
        showMenu();
    };
    document.addEventListener('keydown', handleKey);
}

function showAchievements() {
    gameState.currentScreen = 'achievements';
    hideAllScreens();
    document.getElementById('achievementsOverlay').classList.remove('hidden');
    
    const achievementsList = document.getElementById('achievementsList');
    achievementsList.innerHTML = '';
    
    Object.entries(ACHIEVEMENTS).forEach(([milestone, achievement]) => {
        const isEarned = earnedAchievements.includes(achievement.name);
        const item = document.createElement('div');
        item.className = `achievement-item ${isEarned ? 'achievement-earned' : 'achievement-locked'}`;
        
        const status = isEarned ? '✓ EARNED' : `Locked (${milestone} points needed)`;
        const color = isEarned ? achievement.color : COLORS.WHITE;
        
        item.innerHTML = `
            <div class="achievement-name" style="color: ${color}">${achievement.name}</div>
            <div class="achievement-description">${achievement.description}</div>
            <div class="achievement-status" style="color: ${color}">${status}</div>
        `;
        
        achievementsList.appendChild(item);
    });
    
    // Wait for any key to go back
    const handleKey = () => {
        document.removeEventListener('keydown', handleKey);
        showMenu();
    };
    document.addEventListener('keydown', handleKey);
}

function toggleMusic() {
    gameState.musicEnabled = !gameState.musicEnabled;
    gameState.menuOptions[3] = gameState.musicEnabled ? 'Music: ON' : 'Music: OFF';
    
    // Update the menu option text
    document.querySelectorAll('.menu-option')[3].textContent = gameState.menuOptions[3];
    
    // In a real implementation, you would start/stop background music here
    console.log('Music toggled:', gameState.musicEnabled ? 'ON' : 'OFF');
}

// Game functions
function startGame() {
    gameState.currentScreen = 'game';
    hideAllScreens();
    
    // Reset game state
    score = 0;
    speedLevel = 1;
    gameRunning = true;
    gamePaused = false;
    
    // Reset ball and paddle
    ball.x = CANVAS_WIDTH / 2;
    ball.y = CANVAS_HEIGHT / 2;
    ball.velX = -BASE_BALL_SPEED;
    ball.velY = BASE_BALL_SPEED;
    
    paddle.y = CANVAS_HEIGHT / 2 - PADDLE_HEIGHT / 2;
    
    updateUI();
}

function togglePause() {
    gamePaused = !gamePaused;
}

function gameOver() {
    gameRunning = false;
    
    // Update high score
    if (score > highScore) {
        highScore = score;
        localStorage.setItem('bounceMasterHighScore', highScore);
    }
    
    // Show game over message
    ctx.fillStyle = 'rgba(0, 0, 0, 0.8)';
    ctx.fillRect(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT);
    
    ctx.fillStyle = COLORS.YELLOW;
    ctx.font = '24px Arial';
    ctx.textAlign = 'center';
    ctx.fillText(`Game Over! Score: ${score}`, CANVAS_WIDTH / 2, CANVAS_HEIGHT / 2 - 20);
    ctx.fillText(`High Score: ${highScore}`, CANVAS_WIDTH / 2, CANVAS_HEIGHT / 2 + 20);
    
    // Return to menu after 2 seconds
    setTimeout(() => {
        showMenu();
    }, 2000);
}

function updateGame() {
    if (!gameRunning || gamePaused) return;
    
    // Paddle movement
    if (keys['ArrowUp'] && paddle.y > 0) {
        paddle.y -= PADDLE_SPEED;
    }
    if (keys['ArrowDown'] && paddle.y < CANVAS_HEIGHT - PADDLE_HEIGHT) {
        paddle.y += PADDLE_SPEED;
    }
    
    // Ball movement
    ball.x += ball.velX;
    ball.y += ball.velY;
    
    // Ball collision with top/bottom
    if (ball.y <= 0 || ball.y >= CANVAS_HEIGHT - BALL_SIZE) {
        ball.velY *= -1;
    }
    
    // Ball collision with paddle
    if (ball.x <= PADDLE_WIDTH && 
        paddle.y < ball.y + BALL_SIZE && 
        ball.y < paddle.y + PADDLE_HEIGHT) {
        ball.velX *= -1;
        score++;
        
        // Increase ball speed every 10 points
        const newSpeedLevel = Math.floor(score / 10) + 1;
        if (newSpeedLevel > speedLevel) {
            speedLevel = newSpeedLevel;
            // Update ball speed
            const speedMultiplier = speedLevel;
            ball.velX = (ball.velX > 0 ? BASE_BALL_SPEED : -BASE_BALL_SPEED) * speedMultiplier;
            ball.velY = (ball.velY > 0 ? BASE_BALL_SPEED : -BASE_BALL_SPEED) * speedMultiplier;
        }
        
        // Check achievements
        checkAchievements();
        
        updateUI();
    }
    
    // Ball out of bounds (game over)
    if (ball.x < 0) {
        gameOver();
        return;
    }
    
    // Ball collision with right wall
    if (ball.x > CANVAS_WIDTH - BALL_SIZE) {
        ball.velX *= -1;
    }
}

function checkAchievements() {
    Object.entries(ACHIEVEMENTS).forEach(([milestone, achievement]) => {
        if (score >= parseInt(milestone) && !earnedAchievements.includes(achievement.name)) {
            earnedAchievements.push(achievement.name);
            localStorage.setItem('bounceMasterAchievements', JSON.stringify(earnedAchievements));
            showAchievementPopup(achievement.name, achievement.color);
        }
    });
}

function showAchievementPopup(achievementName, color) {
    document.getElementById('achievementName').textContent = achievementName;
    document.getElementById('achievementPopup').classList.remove('hidden');
    
    // Hide after 3 seconds
    setTimeout(() => {
        document.getElementById('achievementPopup').classList.add('hidden');
    }, 3000);
}

function updateUI() {
    document.getElementById('score').textContent = `Score: ${score}`;
    document.getElementById('highScore').textContent = `High Score: ${highScore}`;
    document.getElementById('speedLevel').textContent = `Speed Level: ${speedLevel}`;
}

function render() {
    // Clear canvas
    ctx.fillStyle = COLORS.BLUE;
    ctx.fillRect(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT);
    
    if (gameState.currentScreen === 'game') {
        // Draw paddle
        ctx.fillStyle = COLORS.GREEN;
        ctx.fillRect(paddle.x, paddle.y, paddle.width, paddle.height);
        
        // Draw ball
        ctx.fillStyle = COLORS.RED;
        ctx.beginPath();
        ctx.arc(ball.x + BALL_SIZE / 2, ball.y + BALL_SIZE / 2, BALL_SIZE / 2, 0, Math.PI * 2);
        ctx.fill();
        
        // Draw pause screen if paused
        if (gamePaused) {
            ctx.fillStyle = 'rgba(0, 0, 0, 0.8)';
            ctx.fillRect(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT);
            
            ctx.fillStyle = COLORS.YELLOW;
            ctx.font = '24px Arial';
            ctx.textAlign = 'center';
            ctx.fillText('PAUSED', CANVAS_WIDTH / 2, CANVAS_HEIGHT / 2 - 20);
            ctx.fillText('Press SPACEBAR to resume', CANVAS_WIDTH / 2, CANVAS_HEIGHT / 2 + 20);
        }
    }
}

function gameLoop() {
    updateGame();
    render();
    requestAnimationFrame(gameLoop);
}

// Start the game when page loads
window.addEventListener('load', init); 