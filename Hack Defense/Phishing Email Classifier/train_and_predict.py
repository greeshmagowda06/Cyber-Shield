# phish_classifier/train_and_predict.py
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import joblib, sys

# Minimal demo dataset (replace with real dataset)
data = [
    ("Your account is compromised, click http://evil.com",1),
    ("Meeting tomorrow at 10am",0),
    ("Verify your login at http://login.example.com",1),
    ("Lunch plans?",0)
]
df = pd.DataFrame(data, columns=["text","label"])
X = df["text"]; y = df["label"]

vec = TfidfVectorizer(ngram_range=(1,2))
Xv = vec.fit_transform(X)
Xtr,Xte,ytr,yte = train_test_split(Xv,y,test_size=0.3,random_state=42)

clf = LogisticRegression(max_iter=1000).fit(Xtr,ytr)
print("Acc:", clf.score(Xte,yte))
joblib.dump((vec,clf),"phish_model.pkl")
print("Saved model.")

if len(sys.argv)>1 and sys.argv[1]=="predict":
    vec,clf = joblib.load("phish_model.pkl")
    s = " ".join(sys.argv[2:])
    p = clf.predict_proba(vec.transform([s]))[0][1]
    print("Phishing probability:", p)