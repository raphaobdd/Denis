import os
import json
import pandas as pd
from dotenv import load_dotenv
from supabase import create_client
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.ensemble import RandomForestClassifier
import joblib

# ----------------------------------------------------------------
# 1. Configurações / Supabase
# ----------------------------------------------------------------
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# ----------------------------------------------------------------
# 2. Buscar Dataset da Tabela do Supabase
# ----------------------------------------------------------------
response = supabase.table("asteroids").select("*").execute()
df = pd.DataFrame(response.data)

if df.empty:
    raise Exception("A tabela 'asteroids' está vazia ou não existe!")

# ----------------------------------------------------------------
# 3. Preparar dados
# ----------------------------------------------------------------
TARGET = "is_potentially_hazardous_asteroid"

# Remover colunas não usadas
drop_cols = ["name", "close_approach_date"]
drop_cols = [c for c in drop_cols if c in df.columns]

X = df.drop(columns=[TARGET] + drop_cols)
y = df[TARGET].astype(int)

# ----------------------------------------------------------------
# 4. Train-Test split
# ----------------------------------------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y
)

# ----------------------------------------------------------------
# 5. Normalização
# ----------------------------------------------------------------
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# ----------------------------------------------------------------
# 6. Modelo
# ----------------------------------------------------------------
model = RandomForestClassifier(
    n_estimators=400,
    max_depth=5,
    class_weight='balanced',
    random_state=42
)

model.fit(X_train_scaled, y_train)

# ----------------------------------------------------------------
# 7. Métricas
# ----------------------------------------------------------------
y_pred = model.predict(X_test_scaled)

metrics = {
    "accuracy": accuracy_score(y_test, y_pred),
    "precision": precision_score(y_test, y_pred, zero_division=0),
    "recall": recall_score(y_test, y_pred, zero_division=0),
    "f1": f1_score(y_test, y_pred, zero_division=0)
}

print("\nMÉTRICAS DO MODELO:")
print(metrics)

# ----------------------------------------------------------------
# 8. Exportar modelo, scaler e métricas
# ----------------------------------------------------------------
joblib.dump(model, "model.pkl")
joblib.dump(scaler, "scaler.pkl")

with open("metrics.json", "w") as f:
    json.dump(metrics, f, indent=4)

print("\nArquivos gerados:")
print(" - model.pkl")
print(" - scaler.pkl")
print(" - metrics.json")
print("\nTreinamento concluído!")
