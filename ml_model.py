from sklearn.ensemble import IsolationForest
import numpy as np

model = None

def train_model(transactions):
    global model

    if len(transactions) < 5:
        return None

    X = np.array([[t.amount] for t in transactions])

    model = IsolationForest(contamination=0.2, random_state=42)
    model.fit(X)

    return model

def detect_anomalies(transactions):
    global model

    if model is None:
        return []

    X = np.array([[t.amount] for t in transactions])
    preds = model.predict(X)

    return [
        transactions[i].dict()
        for i in range(len(preds))
        if preds[i] == -1
    ]