from flask import Flask, request, jsonify, render_template
import os
import json
import pickle
import numpy as np
import random

# ------------------------------------
# CREATE FLASK APP
# ------------------------------------
app = Flask(
    __name__,
    template_folder="../frontend/templates",
    static_folder="../frontend/static"
)

# ------------------------------------
# PATH SETUP
# ------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(BASE_DIR, "..", "model", "intent_model.pkl")
VECT_PATH  = os.path.join(BASE_DIR, "..", "model", "vectorizer.pkl")
DATA_PATH  = os.path.join(BASE_DIR, "..", "data", "dataset.json")

# ------------------------------------
# LOAD MODEL, VECTORIZER, DATASET
# ------------------------------------
model = pickle.load(open(MODEL_PATH, "rb"))
vectorizer = pickle.load(open(VECT_PATH, "rb"))

with open(DATA_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

# ------------------------------------
# HOME ROUTE
# ------------------------------------
@app.route("/")
def home():
    return render_template("index.html")

# ------------------------------------
# CHAT ROUTE (REAL AI LOGIC)
# ------------------------------------
@app.route("/chat", methods=["POST"])
def chat():
    user_msg = request.json.get("message", "").lower().strip()

    if user_msg == "":
        return jsonify({"reply": "Please type something 😊"})

    # Vectorize input
    vector = vectorizer.transform([user_msg])

    # Predict probabilities
    probs = model.predict_proba(vector)[0]
    max_prob = np.max(probs)
    intent = model.classes_[np.argmax(probs)]

    # Confidence threshold
    if max_prob < 0.20:
        return jsonify({
            "reply": "Sorry 😕 I didn't understand that. Please ask about admissions, fees, results, hostel, etc."
        })

    # Find matching intent and reply
    for item in data:
        if item["intent"] == intent:
            answer = item["answer"]

            # ⭐ RANDOM RESPONSE FIX ⭐
            if isinstance(answer, list):
                return jsonify({"reply": random.choice(answer)})
            else:
                return jsonify({"reply": answer})

    return jsonify({"reply": "Sorry, I couldn't find an answer."})

# ------------------------------------
# RUN SERVER
# ------------------------------------
if __name__ == "__main__":
    app.run(port=8080, debug=True)

