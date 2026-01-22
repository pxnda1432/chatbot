@app.route("/chat", methods=["POST"])
def chat():
    user_msg = request.json.get("message", "").lower().strip()

    if not user_msg:
        return jsonify({"reply": "Please type something 😊"})

    vector = vectorizer.transform([user_msg])
    probs = model.predict_proba(vector)[0]

    intent = model.classes_[probs.argmax()]
    confidence = probs.max()

    if confidence < 0.20:
        return jsonify({
            "reply": "Sorry 😕 I didn't understand that. Please ask about admissions, fees, results, hostel, etc."
        })

    matches = [item for item in data if item["intent"] == intent]

    if not matches:
        return jsonify({"reply": "Sorry, I couldn't find an answer."})

    answer = random.choice(matches)["answer"]

    if isinstance(answer, list):
        answer = random.choice(answer)

    return jsonify({"reply": answer})
