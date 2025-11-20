from requests_api import get_all_data
from repository import salvar_dados_api
from os import getenv
from dotenv import load_dotenv
import os

load_dotenv()

def main():
    # 1. Puxar dados da API
    url = os.getenv("API_URL")
    dados = get_all_data(url)

    # 2. Salvar no Postgres
    salvar_dados_api(dados)

    print("Dados importados para o Postgres")

if __name__ == "__main__":
    main()
