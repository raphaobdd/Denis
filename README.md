# Sistema de Análise de Asteroides Perigosos

## Equipe
- Raphael Bento von Zuben — 23002292 — raphael.bvz@puccampinas.edu.br
- Arturo Bento Duran - 23003201 - arturo.bd@puccampinas.edu.br

## Descrição Geral
Este projeto consiste em um sistema de análise de asteroides próximos à Terra, com objetivo de identificar se eles são potencialmente perigosos.  
O sistema utiliza dados de asteroides disponibilizados pela NASA e permite a previsão de risco com base em atributos físicos e orbitais, fornecendo uma interface web interativa para inserção de novos dados e visualização dos resultados.  

---

## Dataset
- **Fonte**: [NASA NEO Dataset](https://ssd-api.jpl.nasa.gov/doc/cad.html) (armazenado e acessado via Supabase)  
- **Volume de dados esperado**: milhares de registros de asteroides, incluindo informações como magnitude absoluta, diâmetro estimado, velocidade e risco potencial.  
- **Licença**: Dados públicos da NASA, disponíveis sob [NASA Open Data License](https://www.nasa.gov/open/data)  

---


## Motivações
- **1. Supabase como banco de dados**: 
    [Motivo]

        Supabase oferece banco relacional (PostgreSQL) em nuvem com integração fácil via API REST ou client Python.

        Gratuito para projetos pequenos, ideal para protótipos ou POCs.

    [Benefícios]

        Permite armazenar todos os registros históricos de asteroides.

        Facilita a consulta de dados diretamente do backend Flask.

        Escalabilidade: ao crescer, é possível aumentar plano ou migrar para PostgreSQL tradicional sem mudanças na arquitetura.

- **2. Flask como backend**: 
    [Motivo]
        Supabase oferece banco relacional (PostgreSQL) em nuvem com integração fácil via API REST ou client Python.

        Possui autenticação, storage e tempo de setup muito rápido.

        Gratuito para projetos pequenos, ideal para protótipos ou POCs.
    [Benefícios]
        Controla toda a lógica do sistema: predição, métricas e acesso a dados.

        Permite integração com armazenamento de modelos e gráficos.

- **3. Random Forest como modelo de ML**:
    [Motivo]
        É robusto a outliers, suporta features numéricas variadas e não requer normalização complexa (apesar de usarmos scaler).

        Bom desempenho mesmo com datasets desequilibrados (somado ao uso do SMOTE).

        Fácil de interpretar e salvar com joblib.

- **4. Escalabilidade e manutenção**:
    [Motivo]
        Backend escalável: Flask pode ser colocado em serviços como Railway, Heroku ou Docker/Kubernetes.

        Banco escalável: Supabase (PostgreSQL) pode crescer sem mudar código.
    
        Modelo treinado separado:

            O modelo é salvo (model.pkl) e carregado pelo Flask, permitindo separar treino de predição.

            Novos dados podem ser adicionados e o modelo re-treinado sem afetar o frontend.

---

## Segurança

- **Proteção de chaves e credenciais**:
  - Todas as chaves e tokens (Supabase URL e KEY, OpenAI API, etc.) são armazenados em `.env` e não versionados no Git.
  - O arquivo `.env`.

- **Políticas de acesso**:
  - Supabase utiliza roles e policies para limitar acesso a dados sensíveis.
  - Usuários da aplicação web só têm permissão de leitura/escrita através do backend, nunca acesso direto ao banco.

- **Boas práticas adicionais**:
  - Evitar logs de dados sensíveis.
  - Validar e sanitizar todas as entradas do usuário antes de enviar para o modelo ou banco.
  - Deploy seguro usando HTTPS e configuração adequada do servidor Flask em produção.

---


## Arquitetura da Solução

``mermaid
graph TD
    A[Frontend Web] -->|Envia dados do asteroide| B[Flask API]
    B -->|Consulta/Atualiza| C[Supabase DB]
    B -->|Usa modelo treinado| D[Random Forest Model]
    D -->|Retorna predição| B
    B -->|Retorna resultado| A
    E[Arquivos locais / Storage] --> D


Backend: Flask com APIs REST para predição (/predict) e exportação de dados (/dados).

Frontend: Página web para inserção de dados, visualização de resultados e métricas.

ML Model: Random Forest treinado com dados do Supabase, utilizando SMOTE para balanceamento e StandardScaler para normalização.

Armazenamento de modelos e métricas: joblib e JSON.

Capturas de tela:

Vídeo demo: https://youtu.be/GXGgF3xWqFU

NASA NEO API Documentation: https://ssd-api.jpl.nasa.gov/doc/cad.html

Flask Documentation: https://flask.palletsprojects.com/

scikit-learn Random Forest: https://scikit-learn.org/stable/modules/ensemble.html#forest

SMOTE (imbalanced-learn): https://imbalanced-learn.org/stable/references/generated/imblearn.over_sampling.SMOTE.html

--- 

## Como Rodar a Aplicação

**1. Rodando localmente (sem Docker)**
```bash
pip install -r requirements.txt
python backend/app.py

Certifique-se de ter o Docker e Docker Compose instalados.

Dê permissão executável ao script:
chmod +x start.sh
Rode o script para construir e iniciar o container:
./start.sh
Acesse a aplicação no navegador: http://localhost:5000
Para parar os containers:
docker-compose down

Rodando manualmente via Docker (opcional)
docker build -t asteroid-app .
docker run -p 5000:5000 --env-file .env asteroid-app


---

## Estrutura de diretórios

/
├── backend/
│   └── ... (código Flask, modelos e lógica de predição)
│
├── frontend/
│   └── ... (arquivos HTML/CSS/JS do painel web)
│
├── .vscode/
│   └── settings.json (opcional)
│
│── infra/
│   └── main.tf
│
├── .env                 # Variáveis de ambiente (NUNCA subir para Git)
├── .env.example         # Exemplo de configuração
│
├── asteroids_metadata.json   # Metadados do dataset (fonte, volume, licença)
├── asteroids_rows.csv        # Dados originais dos asteroides (NASA)
│
├── Dockerfile           # Build da imagem Docker
├── docker-compose.yml   # Orquestração (App + dependências)
│
├── feature_names.json   # Nomes das features usadas no modelo
├── imputer.pkl          # Imputer treinado
├── scaler.pkl           # Scaler treinado
├── model.pkl            # Modelo Random Forest treinado
├── metrics.json         # Métricas de treino do modelo
│
├── requirements.txt     # Dependências do Python
├── start.sh             # Script para executar o Docker
│
└── README.md            # Documentação principal do projeto



---

## Terraform
O arquivo define a infraestrutura necessária para hospedar a aplicação:

- **Azure App Service** – Hospeda o backend Flask.
- **Azure App Service Plan** – Define o plano de execução.
- **Azure Storage Account** – Armazena modelos (`model.pkl`, `scaler.pkl`) ou logs.
- **Azure PostgreSQL Flexible Server** – Banco relacional equivalente ao Supabase.
- **Resource Group** – Agrupa todos os componentes.

### Como executar (opcional)
```bash
cd infra
terraform init
terraform plan
terraform apply

<img width="1365" height="639" alt="image" src="https://github.com/user-attachments/assets/b870fbe3-59bf-4405-8aac-f4cb2cabc98a" />
<img width="1365" height="635" alt="image" src="https://github.com/user-attachments/assets/3eae897a-7002-438c-a2ad-de5c902f4c6c" />
<img width="1365" height="641" alt="image" src="https://github.com/user-attachments/assets/c6f8f882-3189-4c17-8eff-a92de457f041" />

