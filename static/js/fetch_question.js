let selectedCategory = '';
let selectedDifficulty = '';

function fetchQuestion() {
    document.getElementById('questionMeta').textContent = '';
    document.getElementById('questionText').innerHTML = '<span class="status">Loading...</span>';
    document.getElementById('answers').innerHTML = '';

    const params = new URLSearchParams();
    if (selectedCategory) params.set('category', selectedCategory);
    if (selectedDifficulty) params.set('difficulty', selectedDifficulty);

    fetch('/get_question?' + params.toString())
        .then(res => {
            if (res.status === 429) throw new Error('rate_limit');
            if (!res.ok) throw new Error('no_results');
            return res.json();
        })
        .then(data => displayQuestion(data))
        .catch(err => {
            const msg = err.message === 'rate_limit'
                ? 'Too many requests — wait a moment and try again.'
                : 'No questions found for that combination. Try different settings.';
            document.getElementById('questionText').innerHTML = `<span class="status">${msg}</span>`;
        });
}

function displayQuestion(data) {
    const diff = data.difficulty.charAt(0).toUpperCase() + data.difficulty.slice(1);
    document.getElementById('questionMeta').textContent = `${data.category} — ${diff}`;
    document.getElementById('questionText').textContent = data.question;

    const answersDiv = document.getElementById('answers');
    answersDiv.innerHTML = '';

    let correctDiv = null;

    data.answers.forEach(answer => {
        const div = document.createElement('div');
        div.textContent = `${answer.choice}.  ${answer.text}`;
        div.classList.add('answer');
        if (answer.correct) correctDiv = div;
        answersDiv.appendChild(div);
    });

    document.getElementById('revealAnswerBtn').onclick = () => {
        if (correctDiv) correctDiv.classList.add('correct');
    };
}

function loadCategories() {
    fetch('/categories')
        .then(res => res.json())
        .then(cats => {
            const select = document.getElementById('categorySelect');
            cats.forEach(cat => {
                const opt = document.createElement('option');
                opt.value = cat.id;
                opt.textContent = cat.name;
                select.appendChild(opt);
            });
        })
        .catch(() => {});
}

document.addEventListener('DOMContentLoaded', () => {
    loadCategories();
    fetchQuestion();

    document.getElementById('newQuestionBtn').onclick = fetchQuestion;

    document.getElementById('categorySelect').onchange = e => {
        selectedCategory = e.target.value;
    };

    document.querySelectorAll('.diff-btn').forEach(btn => {
        btn.onclick = () => {
            document.querySelectorAll('.diff-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            selectedDifficulty = btn.dataset.value;
        };
    });
});
