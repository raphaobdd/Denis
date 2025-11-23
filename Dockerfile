# Imagem base
FROM python:3.12-slim

# Diretório de trabalho
WORKDIR /app

# Copiar requirements e instalar dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo o código
COPY . .

# Expor a porta que Flask vai rodar
EXPOSE 5000

# Comando para rodar a aplicação em produção via Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:5000", "backend.app:app"]
