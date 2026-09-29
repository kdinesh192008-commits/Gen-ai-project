import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from google import genai

load_dotenv()

app = Flask(__name__)

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")

client = genai.Client(api_key=API_KEY) if API_KEY else None

SYSTEM_PROMPT = """You are EduGenie, a friendly educational learning assistant.
Help students understand academic topics clearly and safely.
Use simple language, examples, step-by-step explanations, short summaries,
practice questions, and revision tips when useful. Do not invent sources.
If the user asks for an answer to an active test or exam, explain the concept
and provide study help rather than assisting with cheating."""

@app.route("/")
def index():
    return render_template("index.html")

@app.post("/api/ask")
def ask():
    data = request.get_json(silent=True) or {}
    message = (data.get("message") or "").strip()

    if not message:
        return jsonify({"error": "Please enter a question."}), 400

    if not client:
        return jsonify({
            "error": "Gemini API key is not configured. Add GEMINI_API_KEY to the .env file."
        }), 500

    prompt = f"{SYSTEM_PROMPT}\n\nStudent question:\n{message}"

    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=prompt
        )
        return jsonify({"answer": response.text or "I could not generate an answer."})
    except Exception as exc:
        return jsonify({"error": f"Gemini API error: {exc}"}), 500

@app.post("/api/quiz")
def quiz():
    data = request.get_json(silent=True) or {}
    topic = (data.get("topic") or "").strip()
    count = int(data.get("count") or 5)
    count = max(1, min(count, 10))

    if not topic:
        return jsonify({"error": "Enter a topic."}), 400
    if not client:
        return jsonify({"error": "Gemini API key is not configured."}), 500

    prompt = f"""Create {count} multiple-choice questions for a student about: {topic}.
For each question provide 4 options A-D and identify the correct answer.
Add a one-sentence explanation after each answer.
Return plain text with clear numbering."""

    try:
        response = client.models.generate_content(model=MODEL, contents=prompt)
        return jsonify({"answer": response.text or "No quiz generated."})
    except Exception as exc:
        return jsonify({"error": f"Gemini API error: {exc}"}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
