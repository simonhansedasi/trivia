function fetchBaseUrl() {
    return fetch('config.txt')
        .then(res => res.text())
        .then(text => text.trim());
}

function fetchQuestion() {
    fetchBaseUrl()
        .then(baseUrl => fetch(`${baseUrl}/get_question`))
        .then(res => res.json())
        .then(data => {
            console.log("Fetched:", data);
            displayQuestion(data);
        })
        .catch(err => console.error("Fetch error:", err));
}

function displayQuestion(data) {
    document.getElementById("questionText").textContent = data.question || "No question found";

    const answersDiv = document.getElementById("answers");
    answersDiv.innerHTML = "";

    let correctDiv = null; // store the correct div so we can bold it later

    data.answers.forEach(answer => {
        const div = document.createElement("div");
        div.textContent = `${answer.choice}. ${answer.text}`;
        div.classList.add("answer");

        if (answer.correct) {
            correctDiv = div;
        }

        answersDiv.appendChild(div);
    });
    document.getElementById("revealAnswerBtn").onclick = () => {
        if (correctDiv) {
            correctDiv.style.fontWeight = "bold";
        }
    };
}

document.addEventListener("DOMContentLoaded", () => {
    fetchQuestion();
    document.getElementById("newQuestionBtn").onclick = fetchQuestion;
});
