# net_ids/detector.py - Interactive AI Network Intrusion Detector
import pandas as pd
from sklearn.ensemble import IsolationForest
import joblib, os

# -------------------------
# Helper Functions
# -------------------------

def make_demo_csv():
    """Create a demo CSV with synthetic network flow data."""
    df = pd.DataFrame([
        {"src": "10.0.0.1", "dst": "10.0.0.2", "pkts": 5, "bytes": 400, "unique_ports": 2},
        {"src": "10.0.0.3", "dst": "10.0.0.2", "pkts": 200, "bytes": 10000, "unique_ports": 100},  # anomaly
        {"src": "10.0.0.4", "dst": "10.0.0.2", "pkts": 7, "bytes": 800, "unique_ports": 3},
    ])
    df.to_csv("flows.csv", index=False)
    print("\n✅ Demo 'flows.csv' created successfully!\n")

def train():
    """Train IsolationForest on network flow data."""
    if not os.path.exists("flows.csv"):
        print("❌ 'flows.csv' not found. Please create demo data or provide your own dataset.")
        return

    df = pd.read_csv("flows.csv")
    X = df[["pkts", "bytes", "unique_ports"]]

    print("\n🧠 Training Isolation Forest model...")
    model = IsolationForest(contamination="auto", random_state=42).fit(X)
    joblib.dump(model, "flow_if.pkl")
    print("✅ Model trained and saved as 'flow_if.pkl'\n")

def score():
    """Evaluate flows for anomalies."""
    if not os.path.exists("flows.csv"):
        print("❌ 'flows.csv' not found. Please create demo data or use your dataset.")
        return

    if not os.path.exists("flow_if.pkl"):
        print("❌ Model 'flow_if.pkl' not found. Please train the model first.")
        return

    df = pd.read_csv("flows.csv")
    model = joblib.load("flow_if.pkl")

    df["score"] = model.decision_function(df[["pkts", "bytes", "unique_ports"]])
    df["anomaly"] = model.predict(df[["pkts", "bytes", "unique_ports"]])

    anomalies = df[df["anomaly"] == -1]
    print("\n--- 🚨 Anomaly Detection Results ---")
    print(anomalies if not anomalies.empty else "No anomalies detected.")
    print("\n--- 📊 All Flows ---")
    print(df[["src", "dst", "pkts", "bytes", "unique_ports", "score", "anomaly"]])

    # Optional: save results
    df.to_csv("scored_flows.csv", index=False)
    print("\n✅ Results saved to 'scored_flows.csv'\n")

# -------------------------
# Interactive Menu
# -------------------------
def main():
    while True:
        print("""
===============================
🌐 AI Network Intrusion Detector
===============================
1️⃣  Create demo flow CSV
2️⃣  Train the model
3️⃣  Run anomaly detection
4️⃣  Exit
""")

        choice = input("Enter your choice (1-4): ").strip()

        if choice == "1":
            make_demo_csv()
        elif choice == "2":
            train()
        elif choice == "3":
            score()
        elif choice == "4":
            print("👋 Exiting... Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please enter 1, 2, 3, or 4.\n")

if __name__ == "__main__":
    main()
