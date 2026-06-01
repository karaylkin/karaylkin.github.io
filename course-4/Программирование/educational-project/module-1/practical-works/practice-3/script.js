const gameData = [
    { id: 1, term: 'HTML', def: 'Язык разметки гипертекста' },
    { id: 2, term: 'CSS', def: 'Каскадные таблицы стилей' },
    { id: 3, term: 'JavaScript', def: 'Язык программирования для веба' },
    { id: 4, term: 'API', def: 'Интерфейс программирования приложений' },
    { id: 5, term: 'Browser', def: 'Программа для просмотра веб-страниц' },
    { id: 6, term: 'Server', def: 'Компьютер, предоставляющий ресурсы' },
    { id: 7, term: 'Database', def: 'Организованная коллекция данных' },
    { id: 8, term: 'Frontend', def: 'Клиентская часть приложения' }
];

// Game State
let cards = [];
let hasFlippedCard = false;
let lockBoard = false;
let firstCard, secondCard;
let moves = 0;
let score = 0;
let matchesFound = 0;
let totalPairs = 0;
let timerInterval;
let seconds = 0;
let currentDifficulty = 'easy';

// DOM Elements
const startScreen = document.getElementById('start-screen');
const gameScreen = document.getElementById('game-screen');
const resultScreen = document.getElementById('result-screen');
const gameBoard = document.getElementById('game-board');
const timerEl = document.getElementById('timer');
const movesEl = document.getElementById('moves');
const scoreEl = document.getElementById('score');
const finalTimeEl = document.getElementById('final-time');
const finalMovesEl = document.getElementById('final-moves');
const finalScoreEl = document.getElementById('final-score');
const newRecordMsg = document.getElementById('new-record-msg');
const highScoresList = document.getElementById('high-scores-list-preview');

// Event Listeners
document.querySelectorAll('.difficulty-btns .btn').forEach(btn => {
    btn.addEventListener('click', () => startGame(btn.dataset.difficulty));
});

document.getElementById('restart-btn-game').addEventListener('click', () => {
    stopTimer();
    showScreen(startScreen);
});

document.getElementById('restart-btn-result').addEventListener('click', () => {
    startGame(currentDifficulty);
});

document.getElementById('home-btn').addEventListener('click', () => {
    showScreen(startScreen);
    updateHighScoresUI();
});

// Init
updateHighScoresUI();

function showScreen(screen) {
    document.querySelectorAll('.screen').forEach(s => s.classList.remove('active'));
    screen.classList.add('active');
}

function startGame(difficulty) {
    currentDifficulty = difficulty;
    resetGameVars();
    
    // Select data based on difficulty
    let dataSubset;
    if (difficulty === 'easy') {
        // 4x3 = 12 cards = 6 pairs
        dataSubset = gameData.slice(0, 6);
        gameBoard.className = 'game-board easy';
    } else {
        // 4x4 = 16 cards = 8 pairs
        dataSubset = gameData.slice(0, 8);
        gameBoard.className = 'game-board hard';
    }
    
    totalPairs = dataSubset.length;
    
    // Create pairs (Term + Definition)
    const deck = [];
    dataSubset.forEach(item => {
        deck.push({ id: item.id, content: item.term, type: 'term' });
        deck.push({ id: item.id, content: item.def, type: 'def' });
    });
    
    shuffle(deck);
    renderBoard(deck);
    
    showScreen(gameScreen);
    startTimer();
}

function resetGameVars() {
    moves = 0;
    score = 0;
    seconds = 0;
    matchesFound = 0;
    hasFlippedCard = false;
    lockBoard = false;
    firstCard = null;
    secondCard = null;
    
    movesEl.textContent = moves;
    scoreEl.textContent = score;
    timerEl.textContent = '00:00';
}

function shuffle(array) {
    for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]];
    }
}

function renderBoard(deck) {
    gameBoard.innerHTML = '';
    deck.forEach(item => {
        const card = document.createElement('div');
        card.classList.add('card');
        card.dataset.id = item.id;
        
        const frontFace = document.createElement('div');
        frontFace.classList.add('card-face', 'card-front');
        frontFace.textContent = item.content;
        
        const backFace = document.createElement('div');
        backFace.classList.add('card-face', 'card-back');
        
        card.appendChild(frontFace);
        card.appendChild(backFace);
        
        card.addEventListener('click', flipCard);
        gameBoard.appendChild(card);
    });
}

function flipCard() {
    if (lockBoard) return;
    if (this === firstCard) return;

    this.classList.add('flipped');

    if (!hasFlippedCard) {
        // First click
        hasFlippedCard = true;
        firstCard = this;
        return;
    }

    // Second click
    secondCard = this;
    incrementMoves();
    checkForMatch();
}

function checkForMatch() {
    let isMatch = firstCard.dataset.id === secondCard.dataset.id;

    if (isMatch) {
        disableCards();
        score += 10;
        scoreEl.textContent = score;
        matchesFound++;
        
        if (matchesFound === totalPairs) {
            endGame();
        }
    } else {
        unflipCards();
    }
}

function disableCards() {
    firstCard.classList.add('matched');
    secondCard.classList.add('matched');
    
    // Remove event listeners logic handled by class check or just leave them
    // Reset board state
    resetBoard();
}

function unflipCards() {
    lockBoard = true;
    setTimeout(() => {
        firstCard.classList.remove('flipped');
        secondCard.classList.remove('flipped');
        resetBoard();
    }, 1000);
}

function resetBoard() {
    [hasFlippedCard, lockBoard] = [false, false];
    [firstCard, secondCard] = [null, null];
}

function incrementMoves() {
    moves++;
    movesEl.textContent = moves;
}

function startTimer() {
    clearInterval(timerInterval);
    timerInterval = setInterval(() => {
        seconds++;
        const mins = Math.floor(seconds / 60).toString().padStart(2, '0');
        const secs = (seconds % 60).toString().padStart(2, '0');
        timerEl.textContent = `${mins}:${secs}`;
    }, 1000);
}

function stopTimer() {
    clearInterval(timerInterval);
}

function endGame() {
    stopTimer();
    
    // Bonus for time (max 60 seconds bonus)
    const timeBonus = Math.max(0, 60 - seconds);
    const finalScore = score + timeBonus;
    
    finalTimeEl.textContent = timerEl.textContent;
    finalMovesEl.textContent = moves;
    finalScoreEl.textContent = finalScore;
    
    const isRecord = saveHighScore(finalScore);
    
    if (isRecord) {
        newRecordMsg.classList.remove('hidden');
    } else {
        newRecordMsg.classList.add('hidden');
    }
    
    setTimeout(() => {
        showScreen(resultScreen);
    }, 500);
}

// LocalStorage Logic
function saveHighScore(newScore) {
    const key = `memory-game-highscores-${currentDifficulty}`;
    let scores = JSON.parse(localStorage.getItem(key)) || [];
    
    // Check if it's a record (top 1)
    const currentBest = scores.length > 0 ? scores[0].score : 0;
    const isRecord = newScore > currentBest;
    
    const date = new Date().toLocaleDateString();
    scores.push({ score: newScore, date: date, moves: moves, time: timerEl.textContent });
    
    // Sort desc
    scores.sort((a, b) => b.score - a.score);
    
    // Keep top 5
    scores = scores.slice(0, 5);
    
    localStorage.setItem(key, JSON.stringify(scores));
    return isRecord;
}

function updateHighScoresUI() {
    // Show easy scores by default or current selected
    const key = `memory-game-highscores-easy`; // Just showing easy for preview
    const scores = JSON.parse(localStorage.getItem(key)) || [];
    
    highScoresList.innerHTML = '';
    
    if (scores.length === 0) {
        highScoresList.innerHTML = '<li>Пока нет рекордов (Легкий)</li>';
        return;
    }
    
    scores.forEach((s, i) => {
        const li = document.createElement('li');
        li.innerHTML = `<span>#${i+1} ${s.date}</span> <span>${s.score} очков</span>`;
        highScoresList.appendChild(li);
    });
}