const question = document.getElementById("question");
const answer = document.getElementById("answer");
const askBtn = document.getElementById("askBtn");

const topic = document.getElementById("topic");
const count = document.getElementById("count");
const quizOutput = document.getElementById("quizOutput");
const quizBtn = document.getElementById("quizBtn");

async function postJSON(url, payload) {
  const res = await fetch(url, {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify(payload)
  });
  const data = await res.json();
  if (!res.ok) throw new Error(data.error || "Request failed");
  return data;
}

askBtn.addEventListener("click", async () => {
  const text = question.value.trim();
  if (!text) {
    answer.textContent = "Please enter a question.";
    return;
  }

  askBtn.disabled = true;
  askBtn.textContent = "Thinking...";
  answer.textContent = "EduGenie is generating your answer...";

  try {
    const data = await postJSON("/api/ask", {message: text});
    answer.textContent = data.answer;
  } catch (err) {
    answer.textContent = err.message;
  } finally {
    askBtn.disabled = false;
    askBtn.textContent = "Ask EduGenie";
  }
});

quizBtn.addEventListener("click", async () => {
  const text = topic.value.trim();
  if (!text) {
    quizOutput.textContent = "Please enter a topic.";
    return;
  }

  quizBtn.disabled = true;
  quizBtn.textContent = "Creating quiz...";
  quizOutput.textContent = "Generating questions...";

  try {
    const data = await postJSON("/api/quiz", {
      topic: text,
      count: Number(count.value)
    });
    quizOutput.textContent = data.answer;
  } catch (err) {
    quizOutput.textContent = err.message;
  } finally {
    quizBtn.disabled = false;
    quizBtn.textContent = "Generate Quiz";
  }
});
