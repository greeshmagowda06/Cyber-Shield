"""
train_and_predict.py
--------------------
Interactive ML tool to detect phishing emails.

Features:
- Train model from sample or custom data
- Predict if an email text is phishing or legitimate
- Fully user-driven (no command-line args)

Author: You :)
"""

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
import joblib, os

MODEL_FILE = "phish_model.pkl"
DATA_FILE = "phishing_emails.csv"


# -------------------------------
# 📘 Train the phishing classifier
# -------------------------------
def train_model():
    """Trains and saves phishing detection model."""
    print("\n--- TRAINING MODE ---")
    if not os.path.exists(DATA_FILE):
        print(f"⚠️  '{DATA_FILE}' not found.")
        choice = input("Would you like to create a demo dataset? (y/n): ").strip().lower()
        if choice == "y":
            demo = pd.DataFrame([
                {"text": "Verify your account immediately to avoid suspension!", "label": 1},
                {"text": "Your invoice for this month is attached.", "label": 0},
                {"text": "We detected unusual login activity, click here to reset.", "label": 1},
                {"text": "Meeting at 3 PM, please confirm your availability.", "label": 0},
                {"text": "Congratulations! You've won a free iPhone, claim now!", "label": 1},
                {"text": "The project update is attached in the document.", "label": 0}
            ])
            demo.to_csv(DATA_FILE, index=False)
            print(f"✅ Demo dataset written to '{DATA_FILE}'.")
        else:
            print("❌ Cannot train without data file.")
            return

    df = pd.read_csv(DATA_FILE)
    if 'text' not in df.columns or 'label' not in df.columns:
        print("❌ CSV must contain 'text' and 'label' columns.")
        return

    X = df["text"]
    y = df["label"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    pipeline = Pipeline([
        ('vectorizer', TfidfVectorizer(ngram_range=(1, 2), max_features=5000)),
        ('classifier', LogisticRegression(max_iter=1000, solver='liblinear'))
    ])

    print("🧠 Training model...")
    pipeline.fit(X_train, y_train)
    acc = pipeline.score(X_test, y_test)
    joblib.dump(pipeline, MODEL_FILE)
    print(f"✅ Model trained with accuracy: {acc:.2f}")
    print(f"💾 Saved as '{MODEL_FILE}'.\n")


# -------------------------------
# 🔍 Predict phishing text
# -------------------------------
def predict_phishing():
    """Takes user input and predicts phishing probability."""
    if not os.path.exists(MODEL_FILE):
        print("⚠️  Model not found — please train one first.")
        return

    pipeline = joblib.load(MODEL_FILE)

    print("\n--- PREDICTION MODE ---")
    while True:
        text = input("\n📧 Enter email text (or 'exit' to go back):\n> ").strip()
        if text.lower() == "exit":
            break
        if not text:
            print("❌ Empty input, try again.")
            continue

        prob = pipeline.predict_proba([text])[0][1]
        verdict = "⚠️  Phishing likely!" if prob > 0.5 else "✅ Legitimate email."
        print(f"\nPhishing probability: {prob:.4f}")
        print(f"Verdict: {verdict}\n")


# -------------------------------
# 📂 Manage dataset
# -------------------------------
def view_or_edit_dataset():
    """Allows user to view or add samples to dataset."""
    print("\n--- DATASET MANAGEMENT ---")

    if not os.path.exists(DATA_FILE):
        print(f"⚠️  '{DATA_FILE}' not found. Creating new empty file.")
        pd.DataFrame(columns=["text", "label"]).to_csv(DATA_FILE, index=False)

    while True:
        print("""
1️⃣  View dataset
2️⃣  Add new sample
3️⃣  Back to main menu
""")
        choice = input("Choose an option (1-3): ").strip()

        if choice == "1":
            df = pd.read_csv(DATA_FILE)
            print("\n--- Dataset Preview ---")
            print(df.head())
            print(f"\n📊 Total samples: {len(df)}\n")

        elif choice == "2":
            text = input("Enter email text:\n> ").strip()
            label = input("Label (1 = phishing, 0 = legitimate): ").strip()
            if label not in ["0", "1"]:
                print("❌ Invalid label.")
                continue
            new_row = pd.DataFrame([[text, int(label)]], columns=["text", "label"])
            new_row.to_csv(DATA_FILE, mode="a", header=not os.path.getsize(DATA_FILE), index=False)
            print("✅ Sample added.\n")

        elif choice == "3":
            break
        else:
            print("❌ Invalid choice. Try again.")


# -------------------------------
# 🎯 Main interactive menu
# -------------------------------
def main_menu():
    print("===========================================")
    print("🤖 AI-Powered Phishing Email Classifier")
    print("===========================================")

    while True:
        print("""
1️⃣  Train or retrain model
2️⃣  Test an email text
3️⃣  View/Edit dataset
4️⃣  Exit
""")
        choice = input("Choose an option (1-4): ").strip()

        if choice == "1":
            train_model()
        elif choice == "2":
            predict_phishing()
        elif choice == "3":
            view_or_edit_dataset()
        elif choice == "4":
            print("👋 Exiting. Stay safe online!")
            break
        else:
            print("❌ Invalid choice. Try again.")


# -------------------------------
# 🧩 Entry point
# -------------------------------
if __name__ == "__main__":
    main_menu()
