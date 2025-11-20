import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

try:
    DB_URL = os.getenv("DATABASE_URL")

    if not DB_URL:
        raise ValueError("Variável SUPABASE_DB_URL não encontrada no .env")

    connection = psycopg2.connect(DB_URL, sslmode="require")
    print("Conexão bem-sucedida!")

except Exception as e:
    print("Erro ao conectar ao banco:", e)
