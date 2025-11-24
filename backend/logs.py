import logging
from flask import Flask

app = Flask(__name__)

# Configuração básica de logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler("logs.txt"), logging.StreamHandler()]
)


@app.route("/")
def index():
    """Rota inicial."""
    app.logger.info("Rota / acessada")
    return "Olá mundo!"


if __name__ == "__main__":
    app.run(debug=True)
