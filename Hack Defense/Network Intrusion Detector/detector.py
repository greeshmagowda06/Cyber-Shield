# net_ids/detector.py
import pandas as pd
from sklearn.ensemble import IsolationForest
import joblib, sys

# Example: create synthetic flow CSV or load real dataset
def make_demo_csv():
    df = pd.DataFrame([
        {"src":"10.0.0.1","dst":"10.0.0.2","pkts":5,"bytes":400,"unique_ports":2},
        {"src":"10.0.0.3","dst":"10.0.0.2","pkts":200,"bytes":10000,"unique_ports":100}, # anomalous
        {"src":"10.0.0.4","dst":"10.0.0.2","pkts":7,"bytes":800,"unique_ports":3},
    ])
    df.to_csv("flows.csv", index=False)
    print("demo flows.csv written")

def train():
    df = pd.read_csv("flows.csv")
    X = df[["pkts","bytes","unique_ports"]]
    model = IsolationForest(contamination=0.2, random_state=42).fit(X)
    joblib.dump(model,"flow_if.pkl")
    print("Model trained")

def score():
    df = pd.read_csv("flows.csv")
    model = joblib.load("flow_if.pkl")
    df["score"] = model.decision_function(df[["pkts","bytes","unique_ports"]])
    df["anomaly"] = model.predict(df[["pkts","bytes","unique_ports"]])
    print(df)

if __name__=="__main__":
    if sys.argv[1]=="demo": make_demo_csv()
    elif sys.argv[1]=="train": train()
    elif sys.argv[1]=="score": score()