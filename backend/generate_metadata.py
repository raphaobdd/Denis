import pandas as pd
import json
from datetime import date

# ----------------------
# CARREGA DATASET
# ----------------------
df = pd.read_csv("asteroids_rows.csv")

# ----------------------
# CALCULA VOLUME
# ----------------------
linhas = len(df)
colunas = len(df.columns)
tamanho_MB = df.memory_usage(deep=True).sum() / 1024**2
colunas_nomes = list(df.columns)

# ----------------------
# CRIA JSON DE METADADOS
# ----------------------
metadados = {
    "nome_dataset": "asteroids_rows",
    "descricao": (
        "Dados de asteroides: posição, diâmetro, magnitude absoluta, órbita, etc."
    ),
    "fonte": "NASA Planetary Data System (PDS) - Jet Propulsion Laboratory",
    "url_fonte": "https://api.nasa.gov/neo/rest/v1/neo/browse",
    "licenca": "Public Domain / United States Government Work",
    "data_extracao": date.today().isoformat(),
    "volume": {
        "linhas": linhas,
        "colunas": colunas,
        "tamanho_MB": round(tamanho_MB, 2),
        "colunas_nomes": colunas_nomes,
    },
}

# ----------------------
# SALVA EM JSON
# ----------------------
with open("asteroids_metadata.json", "w") as f:
    json.dump(metadados, f, indent=4)

print("✅ Metadados gerados em asteroids_metadata.json")
