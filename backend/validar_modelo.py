import os
import json
import pandas as pd
from dotenv import load_dotenv
from supabase import create_client
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score, recall_score, f1_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from imblearn.over_sampling import SMOTE
import joblib
import matplotlib.pyplot as plt

# ----------------------
# 1. CONFIGURAÇÃO / SUPABASE
# ----------------------
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError(
        "❌ SUPABASE_URL ou SUPABASE_KEY não encontradas no .env"
    )

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# ----------------------
# 2. EXTRAIR DATASET
# ----------------------
response = supabase.table("asteroids").select("*").execute()
df = pd.DataFrame(response.data)

if df.empty:
    raise ValueError("A tabela 'asteroids' está vazia ou não existe!")

# ----------------------
# 3. PREPARAR DADOS
# ----------------------
TARGET = "is_potentially_hazardous_asteroid"
DROP_COLS = ["name", "close_approach_date"]
DROP_COLS = [c for c in DROP_COLS if c in df.columns]

X = df.drop(columns=[TARGET] + DROP_COLS)
y = df[TARGET].astype(int)

# ----------------------
# 4. TRAIN-TEST SPLIT
# ----------------------
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# ----------------------
# 5. IMPUTAR VALORES AUSENTES
# ----------------------
imputer = SimpleImputer(strategy="median")
X_train_imp = imputer.fit_transform(X_train)
X_test_imp = imputer.transform(X_test)

# ----------------------
# 6. SMOTE
# ----------------------
print("Antes do SMOTE:", y_train.value_counts().to_dict())
smote = SMOTE(random_state=42)
X_train_res, y_train_res = smote.fit_resample(X_train_imp, y_train)
print("Depois do SMOTE:", y_train_res.value_counts().to_dict())

# ----------------------
# 7. NORMALIZAÇÃO
# ----------------------
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train_res)
X_test_scaled = scaler.transform(X_test_imp)

# Salvar nomes das features
feature_names = list(X.columns)
with open("backend/feature_names.json", "w") as f:
    json.dump(feature_names, f)

# ----------------------
# 8. TREINAR MODELO
# ----------------------
model = RandomForestClassifier(
    n_estimators=500,
    max_depth=None,
    min_samples_split=5,
    min_samples_leaf=2,
    class_weight="balanced",
    random_state=42
)
model.fit(X_train_scaled, y_train_res)

# ----------------------
# 9. MÉTRICAS
# ----------------------
y_pred = model.predict(X_test_scaled)
metrics = {
    "accuracy": round(accuracy_score(y_test, y_pred), 3),
    "precision": round(precision_score(y_test, y_pred, zero_division=0), 3),
    "recall": round(recall_score(y_test, y_pred, zero_division=0), 3),
    "f1": round(f1_score(y_test, y_pred, zero_division=0), 3),
}
print("\nMÉTRICAS DO MODELO:", metrics)

# ----------------------
# 10. GRÁFICO REAL X PREDITO
# ----------------------
img_dir = os.path.join("frontend", "static", "images")
os.makedirs(img_dir, exist_ok=True)

plt.figure(figsize=(10, 5))
plt.plot(y_test.values, label="Real")
plt.plot(y_pred, label="Predito")
plt.legend()
plt.title("Comparação: Real vs Predito")
output_img = os.path.join(img_dir, "grafico_comparacao.png")
plt.savefig(output_img, bbox_inches="tight")
plt.close()
print("✔ Gráfico salvo em", output_img)

# ----------------------
# 11. SALVAR MODELO, SCALER, IMPUTER E MÉTRICAS
# ----------------------
joblib.dump(model, "backend/model.pkl")
joblib.dump(scaler, "backend/scaler.pkl")
joblib.dump(imputer, "backend/imputer.pkl")

with open("backend/metrics.json", "w") as f:
    json.dump(metrics, f, indent=4)

print("\nArquivos gerados em backend/:")
print(" - model.pkl")
print(" - scaler.pkl")
print(" - imputer.pkl")
print(" - metrics.json")
print("\nTreinamento concluído! ✅")
