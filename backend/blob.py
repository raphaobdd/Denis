import os
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv

# ----------------------
# CARREGAR VARIÁVEIS DE AMBIENTE
# ----------------------
load_dotenv()
connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")

if not connection_string:
    raise ValueError(
        "AZURE_STORAGE_CONNECTION_STRING não encontrada no .env"
    )

# ----------------------
# CONFIGURAÇÃO
# ----------------------
container_name = "models"  # Pode escolher outro nome
FILES_TO_UPLOAD = [
    "model.pkl",
    "metrics.json",
]


def main():
    """Conecta ao Azure Blob e envia arquivos definidos em FILES_TO_UPLOAD."""
    # Conecta ao serviço de Blob
    blob_service = BlobServiceClient.from_connection_string(connection_string)

    # Cria o container se ainda não existir
    container_client = blob_service.get_container_client(container_name)
    if not container_client.exists():
        print(f"🔵 Criando container '{container_name}'...")
        container_client.create_container()

    # Enviar arquivos
    for file in FILES_TO_UPLOAD:
        if not os.path.exists(file):
            print(f"⚠️ Arquivo não encontrado: {file}")
            continue

        print(f"⬆️ Fazendo upload de {file}...")
        blob_client = container_client.get_blob_client(file)
        with open(file, "rb") as data:
            blob_client.upload_blob(data, overwrite=True)

    print("✅ Upload concluído!")


# ----------------------
# EXECUÇÃO
# ----------------------
if __name__ == "__main__":
    main()
