const questionText = document.getElementById("questionText");
const progressText = document.getElementById("progressText");
const optionsFieldset = document.getElementById("optionsFieldset");
const feedbackBox = document.getElementById("feedbackBox");
const scoreValue = document.getElementById("scoreValue");
const quizForm = document.getElementById("quizForm");
const startStandardBtn = document.getElementById("startStandardBtn");
const startTimedBtn = document.getElementById("startTimedBtn");
const timerSelect = document.getElementById("timerSelect");
const timerText = document.getElementById("timerText");
const modeText = document.getElementById("modeText");
const modeControls = document.getElementById("modeControls");

let currentQuestion = null;
let questionTimer = null;
let currentMode = "standard";
let isFinishingQuiz = false;

function showFeedback(text, ok) {
  feedbackBox.textContent = text;
  feedbackBox.classList.remove("hidden", "success", "error");
  feedbackBox.classList.add(ok ? "success" : "error");
}

function clearQuestionTimer() {
  if (questionTimer) {
    window.clearInterval(questionTimer);
    questionTimer = null;
  }
}

function updateTimerPill(secondsLeft) {
  if (currentMode !== "timed") {
    timerText.classList.add("hidden");
    timerText.classList.remove("warning");
    timerText.textContent = "Time left: --s";
    return;
  }

  timerText.classList.remove("hidden");
  timerText.textContent = `Time left: ${Math.max(Math.ceil(secondsLeft), 0)}s`;
  if (secondsLeft <= 5) {
    timerText.classList.add("warning");
  } else {
    timerText.classList.remove("warning");
  }
}

function startQuestionTimer(initialSeconds) {
  clearQuestionTimer();
  if (currentMode !== "timed") {
    updateTimerPill(0);
    return;
  }

  let secondsLeft = Number(initialSeconds || 0);
  updateTimerPill(secondsLeft);

  questionTimer = window.setInterval(async () => {
    secondsLeft -= 1;
    updateTimerPill(secondsLeft);
    if (secondsLeft <= 0) {
      clearQuestionTimer();
      await handleQuestionTimeout();
    }
  }, 1000);
}

async function saveDisplayName(defaultName = "") {
  const entered = window.prompt("Quiz complete. Enter your name for the leaderboard:", defaultName || "");
  if (entered === null) {
    return;
  }

  const trimmed = entered.trim();
  const res = await fetch("/api/quiz/display-name", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ display_name: trimmed })
  });

  if (!res.ok) {
    const data = await res.json();
    showFeedback(data.error || "Could not save name.", false);
    await saveDisplayName(defaultName);
    return;
  }
}

async function handleQuizCompletion(data) {
  if (isFinishingQuiz) {
    return;
  }
  isFinishingQuiz = true;
  clearQuestionTimer();

  if (data.result) {
    await saveDisplayName(data.result.display_name || "");
  }

  window.location.href = data.redirect_url;
}

async function handleQuestionTimeout() {
  if (isFinishingQuiz) {
    return;
  }

  const res = await fetch("/api/quiz/timeout", {
    method: "POST",
    headers: { "Content-Type": "application/json" }
  });

  const data = await res.json();
  if (!res.ok) {
    showFeedback(data.error || "Timer expired, but ending the quiz failed.", false);
    return;
  }

  scoreValue.textContent = data.score;
  showFeedback(data.feedback || "Time is up.", false);
  await handleQuizCompletion(data);
}

function renderQuestion(question) {
  currentQuestion = question;
  questionText.textContent = question.question;
  progressText.textContent = `Question ${question.question_number} / ${question.total_questions}`;
  currentMode = question.challenge_mode || currentMode;
  modeText.textContent = `Mode: ${currentMode === "timed" ? "Timed Challenge" : "Standard"}`;

  if (currentMode === "timed") {
    startQuestionTimer(question.time_left_seconds || question.time_limit_seconds || 0);
  } else {
    clearQuestionTimer();
    updateTimerPill(0);
  }

  optionsFieldset.innerHTML = "";
  Object.entries(question.options).forEach(([key, label]) => {
    const optionId = `opt-${key}`;
    const wrapper = document.createElement("label");
    wrapper.className = "option-label";

    const input = document.createElement("input");
    input.type = "checkbox";
    input.name = "answer";
    input.value = key;
    input.id = optionId;

    const text = document.createElement("span");
    text.textContent = `${key.toUpperCase()}. ${label}`;

    wrapper.appendChild(input);
    wrapper.appendChild(text);
    optionsFieldset.appendChild(wrapper);
  });
}

async function startQuiz(challengeMode = "standard") {
  const timeLimit = Number(timerSelect?.value || 20);
  const res = await fetch("/api/quiz/start", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      challenge_mode: challengeMode,
      time_limit_seconds: timeLimit
    })
  });

  const data = await res.json();
  if (!res.ok) {
    showFeedback(data.error || "Unable to start quiz.", false);
    return;
  }

  scoreValue.textContent = data.score;
  currentMode = data.challenge_mode || "standard";
  modeText.textContent = `Mode: ${currentMode === "timed" ? "Timed Challenge" : "Standard"}`;
  if (modeControls) {
    modeControls.classList.add("hidden");
  }
  renderQuestion(data.question);
}

quizForm?.addEventListener("submit", async (event) => {
  event.preventDefault();

  if (!currentQuestion) {
    showFeedback("Question data is not loaded yet.", false);
    return;
  }

  const selected = Array.from(document.querySelectorAll("input[name='answer']:checked")).map(
    (input) => input.value
  );

  const res = await fetch("/api/quiz/answer", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ answers: selected })
  });

  const data = await res.json();
  if (!res.ok) {
    showFeedback(data.error || "Answer submission failed.", false);
    return;
  }

  clearQuestionTimer();
  scoreValue.textContent = data.score;
  showFeedback(data.feedback, data.is_correct);

  if (data.completed) {
    await handleQuizCompletion(data);
    return;
  }

  renderQuestion(data.next_question);
});

if (quizForm) {
  startStandardBtn?.addEventListener("click", () => startQuiz("standard"));
  startTimedBtn?.addEventListener("click", () => startQuiz("timed"));
}
