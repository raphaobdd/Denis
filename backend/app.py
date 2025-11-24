from flask import Flask, render_template, request, jsonify
from supabase import create_client
from dotenv import load_dotenv
import pandas as pd
import joblib
import json
import os

# ----------------------
# CONFIGURAÇÃO E AMBIENTE
# ----------------------
load_dotenv()

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "frontend", "templates"),
    static_folder=os.path.join(BASE_DIR, "frontend", "static"),
)

# ----------------------
# CONEXÃO SUPABASE
# ----------------------
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# ----------------------
# CARREGAR MODELO E PREPROCESSADORES
# ----------------------
try:
    model = joblib.load("model.pkl")
    scaler = joblib.load("scaler.pkl")
    imputer = joblib.load("imputer.pkl")
    print("✔ Modelos e preprocessadores carregados com sucesso.")
except Exception as e:
    model = None
    scaler = None
    imputer = None
    print("❌ ERRO ao carregar modelo/preprocessadores:", e)


# ----------------------
# CARREGAR NOMES DAS FEATURES
# ----------------------
try:
    with open("feature_names.json", "r") as f:
        feature_names = json.load(f)
except Exception as e:
    feature_names = []
    print("❌ ERRO: feature_names.json não encontrado.", e)


# ----------------------
# ROTAS
# ----------------------
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/metrics")
def metrics():
    """Exibe métricas do modelo carregadas via JSON."""
    try:
        with open("metrics.json", "r") as f:
            metrics = json.load(f)
    except Exception as e:
        metrics = {
            "erro": (
                "Métricas não encontradas. "
                "Rode o treinamento novamente."
            )
        }
        print("❌ ERRO ao ler metrics.json:", e)

    return render_template("metrics.html", metrics=metrics)


@app.route("/dados")
def dados():
    """Retorna os dados da tabela asteroids do Supabase."""
    res = supabase.table("asteroids").select("*").execute()
    return jsonify(res.data)


@app.route("/test-model")
def test_model_page():
    """Renderiza a página do formulário para teste do modelo."""
    return render_template("test_model.html", feature_names=feature_names)


@app.route("/predict", methods=["POST"])
def predict():
    """Recebe dados do formulário, aplica preprocessamento e faz predição"""
    if not model or not scaler or not imputer:
        return jsonify({"erro": "Modelo ou preprocess não carregados"}), 500

    try:
        # Receber dados do formulário
        data = {col: float(request.form.get(col)) for col in feature_names}

        # Criar DataFrame
        df_user = pd.DataFrame([data])

        # Aplicar imputer e scaler
        df_imp = imputer.transform(df_user)
        df_scaled = scaler.transform(df_imp)  # type: ignore

        # Predição
        pred = model.predict(df_scaled)[0]
        result = "Perigoso" if pred == 1 else "Não perigoso"

        return render_template(
            "test_model.html",
            result=result,
            feature_names=feature_names
        )

    except Exception as e:
        return jsonify({"erro": str(e)}), 400


# ----------------------
# RODAR SERVIDOR
# ----------------------
if __name__ == "__main__":
    app.run(debug=True)
