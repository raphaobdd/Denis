import os
import json
import pandas as pd
from dotenv import load_dotenv
from supabase import create_client
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from imblearn.over_sampling import SMOTE
import joblib
import matplotlib.pyplot as plt

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

drop_cols = ["name", "close_approach_date"]
drop_cols = [c for c in drop_cols if c in df.columns]

X = df.drop(columns=[TARGET] + drop_cols)
y = df[TARGET].astype(int)

# ----------------------------------------------------------------
# 4. Train-Test split
# ----------------------------------------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# ----------------------------------------------------------------
# 5. Imputar valores ausentes (resolver NaNs)
# ----------------------------------------------------------------
imputer = SimpleImputer(strategy="median")
X_train_imp = imputer.fit_transform(X_train)
X_test_imp = imputer.transform(X_test)

# ----------------------------------------------------------------
# 6. Aplicar SMOTE no TREINO
# ----------------------------------------------------------------
print("Antes do SMOTE:", y_train.value_counts().to_dict())

sm = SMOTE(random_state=42)
X_train_res, y_train_res = sm.fit_resample(X_train_imp, y_train)

print("Depois do SMOTE:", y_train_res.value_counts().to_dict())

# ----------------------------------------------------------------
# 7. Normalização
# ----------------------------------------------------------------
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train_res)
X_test_scaled = scaler.transform(X_test_imp)

# ----------------------------------------------------------------
# 8. Modelo
# ----------------------------------------------------------------
model = RandomForestClassifier(
    n_estimators=500,
    max_depth=None,
    min_samples_split=5,
    min_samples_leaf=2,
    class_weight="balanced",
    random_state=42
)

model.fit(X_train_scaled, y_train_res)

# ----------------------------------------------------------------
# 9. Métricas
# ----------------------------------------------------------------
y_pred = model.predict(X_test_scaled)

metrics = {
    "accuracy": round(accuracy_score(y_test, y_pred), 3),
    "precision": round(precision_score(y_test, y_pred, zero_division=0), 3),
    "recall": round(recall_score(y_test, y_pred, zero_division=0), 3),
    "f1": round(f1_score(y_test, y_pred, zero_division=0), 3)
}


print("\nMÉTRICAS DO MODELO:")
print(metrics)

# ----------------------------------------------------------------
# 10. Gráfico
# ----------------------------------------------------------------
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

print("✔ gráfico salvo em", output_img)

# ----------------------------------------------------------------
# 11. Exportar modelo, scaler e métricas
# ----------------------------------------------------------------
joblib.dump(model, "model.pkl")
joblib.dump(scaler, "scaler.pkl")
joblib.dump(imputer, "imputer.pkl")  # IMPORTANTE para usar na predição depois

with open("metrics.json", "w") as f:
    json.dump(metrics, f, indent=4)

print("\nArquivos gerados:")
print(" - model.pkl")
print(" - scaler.pkl")
print(" - imputer.pkl")
print(" - metrics.json")
print("\nTreinamento concluído!")
