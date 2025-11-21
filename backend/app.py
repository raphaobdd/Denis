from flask import Flask, render_template, request, jsonify
from supabase import create_client
from dotenv import load_dotenv
import pandas as pd
import joblib
import json
import os
import matplotlib.pyplot as plt


load_dotenv()

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# ----------------------
# CONFIGURAÇÃO FLASK
# ----------------------

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "frontend", "templates"),
    static_folder=os.path.join(BASE_DIR, "frontend", "static")
)

# ----------------------
# CONEXÃO SUPABASE
# ----------------------
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# ----------------------
# CARREGAR MODELO
# ----------------------
try:
    model = joblib.load("model.pkl")
    print("✔ Modelo carregado com sucesso.")
except:
    model = None
    print("❌ ERRO: modelo não encontrado. Treine novamente com train_model.py")

# ----------------------
# ROTAS PRINCIPAIS
# ----------------------
@app.route("/")
def index():
    return render_template("index.html")


# ----------------------
# MÉTRICAS
# ----------------------
@app.route("/metrics")
def metrics():
    """Exibe métricas do modelo carregadas via JSON."""
    try:
        with open("metrics.json", "r") as f:
            metrics = json.load(f)
    except:
        metrics = {"erro": "Métricas não encontradas. Rode o treinamento novamente."}

    return render_template("metrics.html", metrics=metrics)


# ----------------------
# PÁGINA PARA TESTE DO MODELO
# ----------------------
@app.route("/test-model")
def test_model_page():
    return render_template("test_model.html")


# ----------------------
# API QUE FAZ A PREDIÇÃO
# ----------------------
@app.route("/predict", methods=["POST"])
def predict():
    if not model:
        return jsonify({"erro": "Modelo não carregado"}), 500

    try:
        data = request.form

        # Coletar campos enviados pelo formulário
        absolute_magnitude = float(data.get("absolute_magnitude"))

        df = pd.DataFrame([{
            "absolute_magnitude": absolute_magnitude
        }])

        prediction = model.predict(df)[0]

        return render_template(
            "test_model.html",
            result="Perigoso" if prediction == 1 else "Não perigoso",
            magnitude=absolute_magnitude
        )

    except Exception as e:
        return jsonify({"erro": str(e)}), 400


# ----------------------
# API PARA EXPORTAR OS DADOS ATUAIS DO SUPABASE
# ----------------------
@app.route("/dados")
def dados():
    """Retorna os dados da tabela asteroids do Supabase."""
    res = supabase.table("asteroids").select("*").execute()
    return jsonify(res.data)


# ----------------------
# RODAR SERVIDOR
# ----------------------
if __name__ == "__main__":
    app.run(debug=True)
