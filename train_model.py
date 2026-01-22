import json
import os
import pickle
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# -----------------------------
# PATH SETUP
# -----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "..", "data", "dataset.json")
MODEL_DIR = os.path.join(BASE_DIR, "..", "model")

os.makedirs(MODEL_DIR, exist_ok=True)

# -----------------------------
# LOAD DATA
# -----------------------------
with open(DATA_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

# -----------------------------
# PREPARE TRAINING DATA
# IMPORTANT FIX: one question → one intent
# -----------------------------
questions = []
intents = []

for item in data:
    questions.append(item["question"].lower().strip())
    intents.append(item["intent"])

df = pd.DataFrame({
    "question": questions,
    "intent": intents
})

# -----------------------------
# VECTORIZATION
# -----------------------------
vectorizer = TfidfVectorizer(
    ngram_range=(1, 2),
    stop_words="english"
)
X = vectorizer.fit_transform(df["question"])
y = df["intent"]

# -----------------------------
# TRAIN MODEL (IMPORTANT FIX)
# -----------------------------
model = LogisticRegression(
    max_iter=1000,
    solver="lbfgs"
)
model.fit(X, y)

# -----------------------------
# SAVE MODEL
# -----------------------------
pickle.dump(model, open(os.path.join(MODEL_DIR, "intent_model.pkl"), "wb"))
pickle.dump(vectorizer, open(os.path.join(MODEL_DIR, "vectorizer.pkl"), "wb"))

print("✅ Model trained and saved successfully!")
