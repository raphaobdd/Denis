import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.ensemble import RandomForestClassifier
import joblib
import json

# 1. Carregar dataset
df = pd.read_csv("asteroids_rows.csv")

# 2. Definir target
target = "is_potentially_hazardous_asteroid"
X = df.drop(columns=[target, "name", "close_approach_date"])
y = df[target].astype(int)

# 3. Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y
)

# 4. Normalizar
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# 5. Modelo
model = RandomForestClassifier(
    n_estimators=400,
    max_depth=5,
    random_state=42
)
model.fit(X_train_scaled, y_train)

# 6. Predições
y_pred = model.predict(X_test_scaled)

# 7. Métricas
metrics = {
    "accuracy": accuracy_score(y_test, y_pred),
    "precision": precision_score(y_test, y_pred, zero_division=0),
    "recall": recall_score(y_test, y_pred, zero_division=0),
    "f1": f1_score(y_test, y_pred, zero_division=0)
}

# 8. Salvar modelo e scaler
joblib.dump(model, "model.pkl")
joblib.dump(scaler, "scaler.pkl")

# 9. Exportar métricas para JSON (para seu Flask)
with open("metrics.json", "w") as f:
    json.dump(metrics, f, indent=4)

print("Treinamento finalizado!")
print(metrics)
