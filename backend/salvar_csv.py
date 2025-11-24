import os
from supabase import create_client
import pandas as pd
from dotenv import load_dotenv

# ----------------------
# CARREGA VARIÁVEIS DE AMBIENTE
# ----------------------
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("❌ SUPABASE_URL ou SUPABASE_KEY não encontradas no .env")

# ----------------------
# CONEXÃO COM SUPABASE
# ----------------------
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# ----------------------
# EXTRAI DADOS DA TABELA
# ----------------------
res = supabase.table("asteroids").select("*").execute()
data = res.data

# ----------------------
# CONVERTE PARA DATAFRAME E SALVA COMO CSV
# ----------------------
df = pd.DataFrame(data)
csv_path = "backend/asteroids_rows.csv"
df.to_csv(csv_path, index=False)

print(f"✅ Dados salvos em {csv_path}")
