const questions = [
    {
        id: 1,
        type: 'radio',
        question: 'Какой HTML-тег используется для подключения JavaScript файла?',
        options: ['<js>', '<script>', '<javascript>', '<link>'],
        correct: 1 // Index of correct option
    },
    {
        id: 2,
        type: 'radio',
        question: 'Как объявить переменную, значение которой нельзя изменить?',
        options: ['var', 'let', 'const', 'static'],
        correct: 2
    },
    {
        id: 3,
        type: 'checkbox',
        question: 'Выберите существующие типы данных в JavaScript (несколько вариантов):',
        options: ['String', 'Number', 'Float', 'Boolean', 'Character'],
        correct: [0, 1, 3] // Indices of correct options
    },
    {
        id: 4,
        type: 'text',
        question: 'Что выведет в консоль: console.log(typeof "Hello")?',
        correct: 'string' // String answer (case insensitive check usually)
    },
    {
        id: 5,
        type: 'radio',
        question: 'Какой метод добавляет элемент в конец массива?',
        options: ['pop()', 'shift()', 'unshift()', 'push()'],
        correct: 3
    },
    {
        id: 6,
        type: 'radio',
        question: 'Что означает аббревиатура DOM?',
        options: ['Data Object Model', 'Document Object Model', 'Document Oriented Module', 'Digital Ordinance Model'],
        correct: 1
    },
    {
        id: 7,
        type: 'checkbox',
        question: 'Какие операторы сравнения существуют в JS?',
        options: ['==', '===', '!=', '><', '<>'],
        correct: [0, 1, 2]
    },
    {
        id: 8,
        type: 'text',
        question: 'Напишите ключевое слово для объявления функции.',
        correct: 'function'
    },
    {
        id: 9,
        type: 'radio',
        question: 'Как правильно вывести модальное окно с текстом "Привет"?',
        options: ['msg("Привет")', 'alert("Привет")', 'prompt("Привет")', 'log("Привет")'],
        correct: 1
    },
    {
        id: 10,
        type: 'radio',
        question: 'Какое событие срабатывает при клике мышкой на элемент?',
        options: ['onmouseover', 'change', 'click', 'mouseclick'],
        correct: 2
    }
];

let currentQuestionIndex = 0;
let score = 0;
let userAnswers = []; // Stores user answers for review
let timerInterval;
let secondsElapsed = 0;

// DOM Elements
const startScreen = document.getElementById('start-screen');
const quizScreen = document.getElementById('quiz-screen');
const resultScreen = document.getElementById('result-screen');
const questionContainer = document.getElementById('question-container');
const nextBtn = document.getElementById('next-btn');
const startBtn = document.getElementById('start-btn');
const restartBtn = document.getElementById('restart-btn');
const reviewBtn = document.getElementById('review-btn');
const reviewContainer = document.getElementById('review-container');
const reviewList = document.getElementById('review-list');

// Progress Elements
const currentQuestionNumEl = document.getElementById('current-question-num');
const totalQuestionsEl = document.getElementById('total-questions');
const progressFill = document.getElementById('progress-fill');
const timeEl = document.getElementById('time');

// Event Listeners
startBtn.addEventListener('click', startQuiz);
nextBtn.addEventListener('click', nextQuestion);
restartBtn.addEventListener('click', restartQuiz);
reviewBtn.addEventListener('click', toggleReview);

function startQuiz() {
    startScreen.classList.add('hidden');
    quizScreen.classList.remove('hidden');
    resultScreen.classList.add('hidden');
    
    currentQuestionIndex = 0;
    score = 0;
    userAnswers = [];
    secondsElapsed = 0;
    
    totalQuestionsEl.textContent = questions.length;
    
    startTimer();
    loadQuestion();
}

function startTimer() {
    clearInterval(timerInterval);
    timerInterval = setInterval(() => {
        secondsElapsed++;
        const minutes = Math.floor(secondsElapsed / 60).toString().padStart(2, '0');
        const seconds = (secondsElapsed % 60).toString().padStart(2, '0');
        timeEl.textContent = `${minutes}:${seconds}`;
    }, 1000);
}

function loadQuestion() {
    const question = questions[currentQuestionIndex];
    
    // Update Progress
    currentQuestionNumEl.textContent = currentQuestionIndex + 1;
    const progressPercent = ((currentQuestionIndex) / questions.length) * 100;
    progressFill.style.width = `${progressPercent}%`;
    
    // Clear container
    questionContainer.innerHTML = '';
    nextBtn.disabled = true;

    // Render Question Title
    const titleEl = document.createElement('div');
    titleEl.className = 'question-text';
    titleEl.textContent = `${currentQuestionIndex + 1}. ${question.question}`;
    questionContainer.appendChild(titleEl);

    // Render Options based on type
    if (question.type === 'radio' || question.type === 'checkbox') {
        const optionsList = document.createElement('div');
        optionsList.className = 'options-list';
        
        question.options.forEach((opt, idx) => {
            const item = document.createElement('label');
            item.className = 'option-item';
            
            const input = document.createElement('input');
            input.type = question.type;
            input.name = 'answer';
            input.value = idx;
            
            // Add event listener to enable button
            input.addEventListener('change', () => {
                checkInput();
                // Visual selection
                if (question.type === 'radio') {
                    document.querySelectorAll('.option-item').forEach(el => el.classList.remove('selected'));
                    item.classList.add('selected');
                } else {
                    item.classList.toggle('selected', input.checked);
                }
            });

            item.appendChild(input);
            item.appendChild(document.createTextNode(opt));
            optionsList.appendChild(item);
        });
        questionContainer.appendChild(optionsList);
    } else if (question.type === 'text') {
        const input = document.createElement('input');
        input.type = 'text';
        input.className = 'text-answer-input';
        input.placeholder = 'Введите ваш ответ...';
        input.addEventListener('input', () => {
            checkInput();
        });
        questionContainer.appendChild(input);
    }
}

function checkInput() {
    const question = questions[currentQuestionIndex];
    let hasAnswer = false;

    if (question.type === 'radio') {
        const selected = document.querySelector('input[name="answer"]:checked');
        if (selected) hasAnswer = true;
    } else if (question.type === 'checkbox') {
        const selected = document.querySelectorAll('input[name="answer"]:checked');
        if (selected.length > 0) hasAnswer = true;
    } else if (question.type === 'text') {
        const input = document.querySelector('.text-answer-input');
        if (input.value.trim().length > 0) hasAnswer = true;
    }

    nextBtn.disabled = !hasAnswer;
}

function nextQuestion() {
    saveAnswer();
    
    currentQuestionIndex++;
    
    if (currentQuestionIndex < questions.length) {
        loadQuestion();
    } else {
        finishQuiz();
    }
}

function saveAnswer() {
    const question = questions[currentQuestionIndex];
    let answer;
    let isCorrect = false;

    if (question.type === 'radio') {
        const selected = document.querySelector('input[name="answer"]:checked');
        answer = parseInt(selected.value);
        if (answer === question.correct) isCorrect = true;
        
        userAnswers.push({
            questionId: question.id,
            userAnswer: answer,
            isCorrect: isCorrect,
            formattedAnswer: question.options[answer]
        });

    } else if (question.type === 'checkbox') {
        const selected = Array.from(document.querySelectorAll('input[name="answer"]:checked')).map(el => parseInt(el.value));
        // Check if arrays match (sort both to compare)
        const sortedSelected = [...selected].sort();
        const sortedCorrect = [...question.correct].sort();
        
        isCorrect = JSON.stringify(sortedSelected) === JSON.stringify(sortedCorrect);
        answer = selected;
        
        userAnswers.push({
            questionId: question.id,
            userAnswer: answer,
            isCorrect: isCorrect,
            formattedAnswer: selected.map(i => question.options[i]).join(', ')
        });

    } else if (question.type === 'text') {
        const input = document.querySelector('.text-answer-input');
        answer = input.value.trim();
        if (answer.toLowerCase() === question.correct.toLowerCase()) isCorrect = true;
        
        userAnswers.push({
            questionId: question.id,
            userAnswer: answer,
            isCorrect: isCorrect,
            formattedAnswer: answer
        });
    }

    if (isCorrect) score++;
}

function finishQuiz() {
    clearInterval(timerInterval);
    quizScreen.classList.add('hidden');
    resultScreen.classList.remove('hidden');
    
    // Calculate results
    const percent = Math.round((score / questions.length) * 100);
    
    document.getElementById('score-points').textContent = score;
    document.getElementById('score-total').textContent = questions.length;
    document.getElementById('score-percent').textContent = `${percent}%`;
    
    const feedbackEl = document.getElementById('feedback-message');
    if (percent === 100) {
        feedbackEl.textContent = "Отлично! Вы эксперт!";
        feedbackEl.style.color = "var(--success-color)";
    } else if (percent >= 70) {
        feedbackEl.textContent = "Хороший результат!";
        feedbackEl.style.color = "var(--primary-color)";
    } else {
        feedbackEl.textContent = "Стоит повторить материал.";
        feedbackEl.style.color = "var(--error-color)";
    }

    generateReview();
}

function generateReview() {
    reviewList.innerHTML = '';
    
    userAnswers.forEach((ans, idx) => {
        const question = questions[idx];
        const item = document.createElement('div');
        item.className = `review-item ${ans.isCorrect ? 'correct' : 'wrong'}`;
        
        let correctText = '';
        if (question.type === 'radio') {
            correctText = question.options[question.correct];
        } else if (question.type === 'checkbox') {
            correctText = question.correct.map(i => question.options[i]).join(', ');
        } else {
            correctText = question.correct;
        }

        item.innerHTML = `
            <div class="review-question">${idx + 1}. ${question.question}</div>
            <div class="review-answer user-ans">Ваш ответ: ${ans.formattedAnswer} ${ans.isCorrect ? '✅' : '❌'}</div>
            ${!ans.isCorrect ? `<div class="review-answer correct-ans">Правильный ответ: ${correctText}</div>` : ''}
        `;
        
        reviewList.appendChild(item);
    });
}

function toggleReview() {
    reviewContainer.classList.toggle('hidden');
    reviewBtn.textContent = reviewContainer.classList.contains('hidden') ? 'Посмотреть ошибки' : 'Скрыть ошибки';
}

function restartQuiz() {
    reviewContainer.classList.add('hidden');
    reviewBtn.textContent = 'Посмотреть ошибки';
    startQuiz();
}