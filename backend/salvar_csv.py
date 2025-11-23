from supabase import create_client
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()

# URL e chave do Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Extrai dados da tabela
res = supabase.table("asteroids").select("*").execute()
data = res.data

# Converte para DataFrame e salva como CSV
df = pd.DataFrame(data)
df.to_csv("asteroids_rows.csv", index=False)

print("Dados salvos em asteroids_rows.csv")
