document.addEventListener('DOMContentLoaded', () => {
    
    // --- Logic for Show/Hide Answer buttons ---
    const toggleButtons = document.querySelectorAll('.toggle-answer-btn');

    toggleButtons.forEach(button => {
        button.addEventListener('click', () => {
            const answerDiv = button.nextElementSibling;
            
            if (answerDiv.classList.contains('hidden')) {
                answerDiv.classList.remove('hidden');
                button.textContent = 'Скрыть ответ';
            } else {
                answerDiv.classList.add('hidden');
                button.textContent = 'Показать ответ';
            }
        });
    });

    // --- Logic for Bubble Sort Visualization ---
    const container = document.getElementById('visualization-area');
    const animateBtn = document.getElementById('animate-btn');
    
    // Initial state
    let array = [5, 1, 4, 2, 8];
    let i = 0;
    let j = 0;
    let isSorting = true;

    // Function to render the array
    function renderArray() {
        container.innerHTML = '';
        array.forEach((val, idx) => {
            const el = document.createElement('div');
            el.className = 'array-item';
            el.textContent = val;
            el.style.height = `${val * 10 + 20}px`; // Dynamic height based on value
            
            // Highlight elements being compared
            if (isSorting && (idx === j || idx === j + 1)) {
                el.style.backgroundColor = '#e74c3c'; // Accent color for comparison
            }
            
            container.appendChild(el);
        });
    }

    renderArray();

    animateBtn.addEventListener('click', () => {
        if (!isSorting) {
            // Reset
            array = [5, 1, 4, 2, 8];
            i = 0;
            j = 0;
            isSorting = true;
            animateBtn.textContent = 'Запустить шаг сортировки';
            renderArray();
            return;
        }

        // Perform one step of bubble sort
        if (i < array.length) {
            if (j < array.length - i - 1) {
                // Compare and swap if needed
                if (array[j] > array[j + 1]) {
                    let temp = array[j];
                    array[j] = array[j + 1];
                    array[j + 1] = temp;
                }
                j++;
            } else {
                // Inner loop finished, reset j, increment i
                j = 0;
                i++;
            }
        }

        // Check if sorting is done
        if (i >= array.length - 1) {
            isSorting = false;
            animateBtn.textContent = 'Сбросить';
            // Render one last time to clear highlights
            container.innerHTML = '';
            array.forEach(val => {
                const el = document.createElement('div');
                el.className = 'array-item';
                el.textContent = val;
                el.style.height = `${val * 10 + 20}px`;
                el.style.backgroundColor = '#2ecc71'; // Green for sorted
                container.appendChild(el);
            });
            return;
        }

        renderArray();
    });
});