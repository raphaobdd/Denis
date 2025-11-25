# Relatório Técnico — Projeto Final

**Sistema de Análise de Asteroides Perigosos**

-----

**Disciplina:** Computação em Nuvem
**Semestre/ANO:** 6° semestre de 2025
**Equipe:**

  * Raphael Bento von Zuben — 23002292
  * Arturo Bento Duran - 23003201

-----

## 1\. Introdução

O projeto visa desenvolver um **Sistema de Análise de Asteroides Perigosos** (Near-Earth Objects - NEOs), com o objetivo primário de prever o risco potencial de impacto de asteroides próximos à Terra.

**Problema e Contexto:** A identificação e classificação de asteroides é crucial para a segurança planetária. O desafio é processar grandes volumes de dados orbitais e físicos fornecidos pela NASA e aplicar um modelo de Machine Learning (ML) para classificar o risco de forma rápida e precisa.

**Motivação e Objetivos:** O principal objetivo é criar uma Prova de Conceito (POC) que demonstre a integração entre um banco de dados relacional em nuvem (**Supabase/PostgreSQL**), um backend robusto (**Flask**) e um modelo de ML (**Random Forest**) treinado para previsão de risco. A arquitetura deve ser modular e escalável, facilitando o deploy e a manutenção.

-----

## 2\. Conjunto de Dados

**Fonte e Descrição:**
Os dados são provenientes do **NASA NEO Dataset** (Near-Earth Object), acessado através da **CAD API** (Close-Approach Data) e armazenados na base de dados **Supabase DB**. O volume de dados esperado abrange **milhares de registros** de asteroides. A licença é a **NASA Open Data License**, garantindo o uso público.

**Esquema e Atributos Chave:**
Os registros incluem atributos físicos e orbitais essenciais para a predição de risco, tais como:

  * **Magnitude Absoluta (H)**
  * **Diâmetro Estimado**
  * **Velocidade de Aproximação (V\_inf)**
  * **Distância de Aproximação (Nominal Distance)**
  * **Risco Potencial (Potentially Hazardous Asteroid - PHA)** (Target/Label)

**Transformações Necessárias:**
Para otimizar a performance do modelo de ML, são aplicadas as seguintes transformações:

1.  **Normalização/Escalonamento:** Utilização do **`StandardScaler`** para normalizar as *features* numéricas, garantindo que todas contribuam de forma equivalente para o modelo. O `scaler.pkl` é salvo e carregado para garantir a consistência entre treino e predição.
2.  **Tratamento de Desbalanceamento:** Aplicação do método **SMOTE** (*Synthetic Minority Over-sampling Technique*) durante o treinamento para lidar com o desequilíbrio natural da classe de asteroides "perigosos" (minoritária), melhorando a capacidade preditiva do modelo para esta classe crítica.
3.  **Imputação:** Uso de um **`Imputer`** (`imputer.pkl`) treinado para preencher valores ausentes no *dataset*.

-----

## 3\. Arquitetura da Solução

### Desenho Detalhado da Arquitetura Final

A solução adota uma arquitetura de três camadas, integrando serviços de nuvem e ferramentas de Machine Learning.

\`\`mermaid
graph TD
A[Frontend Web (HTML/CSS/JS)] --\>|1. Envia dados do asteroide| B[Backend: Flask API]
B --\>|2. Consulta/Atualiza Registros| C[Supabase DB (PostgreSQL)]
B --\>|3. Carrega e usa o modelo| D[Random Forest Model (model.pkl)]
D --\>|4. Retorna Predição de Risco| B
E[Storage/Arquivos Locais] --\>|model.pkl, scaler.pkl| D
B --\>|5. Retorna Resultado e UI| A
subgraph Servidor de Aplicação
B
end
subgraph Camada de Dados
C
E
end

```

**Componente por Componente:**

* **Frontend Web:** Interface interativa para o usuário, permitindo a inserção de novos atributos de asteroides e a visualização dos resultados da predição e das métricas históricas.
* **Backend (Flask API):** O coração da lógica de negócios.
    * **Função:** Controla a lógica de predição, as métricas, e o acesso ao banco de dados.
    * **Endpoints Chave:** `/predict` (para nova predição) e `/dados` (para exportação ou consulta histórica).
* **Supabase DB (PostgreSQL):** Base de dados relacional em nuvem.
    * **Função:** Armazenar todos os registros históricos de asteroides, permitindo consultas diretas via API REST ou *client* Python pelo Flask.
* **Random Forest Model (`model.pkl`):** O modelo de Machine Learning.
    * **Função:** Receber *features* pré-processadas do Flask e retornar a classificação binária de risco potencial (Perigoso/Não Perigoso).
* **Arquivos Locais/Storage:** Armazenam artefatos do ML (`model.pkl`, `scaler.pkl`, `imputer.pkl`, `metrics.json`).

### Justificativa das Decisões

| Componente | Motivação | Benefício |
| :--- | :--- | :--- |
| **Supabase (PostgreSQL)** | Banco relacional em nuvem, fácil integração (API REST/Python Client), gratuito para POCs. | Armazenamento escalável e estruturado de registros históricos. |
| **Flask** | Backend Python minimalista e ágil. | Controla a lógica do sistema, integração nativa com bibliotecas ML (scikit-learn). |
| **Random Forest** | Robusto a *outliers*, bom desempenho em *datasets* desequilibrados (com SMOTE), fácil de serializar (`joblib`). | Alto poder preditivo com boa interpretabilidade. |
| **Modelo Treinado Separado** | O modelo é salvo como `model.pkl` e carregado pelo Flask. | Separação entre o ciclo de Treino e o de Predição, permitindo *deploy* leve e re-treino sem indisponibilidade do serviço. |

### Segurança e Compliance

1.  **Proteção de Credenciais:** Todas as chaves e tokens (Supabase URL/KEY) são isoladas em um arquivo **`.env`** e **não são versionados** no Git, conforme o princípio de segurança.
2.  **Políticas de Acesso (Supabase):** Utilização de *roles* e *policies* no Supabase para limitar o acesso a dados sensíveis. O acesso ao banco é sempre intermediado pelo backend Flask, e nunca de forma direta pelo *frontend* do usuário.
3.  **Sanitização de Entrada:** Validação e sanitização rigorosa de todas as entradas de dados do usuário no *frontend* antes de serem processadas pelo modelo ou inseridas no banco, prevenindo ataques como *SQL Injection*.
4.  **Deploy Seguro:** Recomenda-se o *deploy* em produção via **HTTPS** e configuração adequada de um servidor de aplicação (*e.g.*, Gunicorn com Nginx) para segurança de tráfego.

***

## 4. Implementação

### Scripts e APIs Desenvolvidas

O backend Flask é implementado em `backend/app.py`, contendo a lógica para:

1.  **Carregamento de Artefatos:** No *startup* do Flask, os arquivos `model.pkl`, `scaler.pkl`, e `imputer.pkl` são carregados (`joblib`), minimizando a latência em chamadas de predição.
2.  **API de Predição (`/predict`):** Recebe os atributos de um asteroide via requisição POST, aplica as transformações (`imputer.pkl` e `scaler.pkl`), e passa o vetor resultante para o `model.pkl` para obter a classificação de risco.

### Docker e Orquestração

* **`Dockerfile`:** Define o ambiente Python, instala as dependências (`requirements.txt`), e define o ponto de entrada para a aplicação Flask.
* **`docker-compose.yml`:** Usado para orquestrar o ambiente local. Permite subir o container da aplicação (`asteroid-app`) em uma porta específica (5000) e injetar as variáveis de ambiente a partir do `.env`.
* **`start.sh`:** Script facilitador para a construção (`docker build`) e inicialização (`docker-compose up`) do ambiente containerizado, simplificando o processo de *setup* local.

### Estrutura de Diretórios do Repositório

A estrutura é modular e organizada:

```

/
├── backend/           \# Lógica do Flask e scripts de ML
├── frontend/          \# UI/UX da aplicação web
├── infra/             \# Código de Infraestrutura como Código (Terraform)
├── .env               \# Variáveis de ambiente
├── model.pkl          \# Modelo Random Forest serializado
├── scaler.pkl         \# Scaler treinado
├── imputer.pkl        \# Imputer treinado
├── requirements.txt   \# Dependências Python
├── Dockerfile         \# Definição da imagem
├── docker-compose.yml \# Orquestração Docker
└── start.sh           \# Script de execução

````

***

## 5. Infraestrutura Azure

A infraestrutura como código (IaC) utiliza **Terraform** para provisionar os recursos na **Azure**, permitindo um *deploy* consistente e repetível.



[Image of Azure services for web application hosting]


### Recursos Provisionados

O arquivo `infra/main.tf` define os seguintes recursos, agrupados no **Resource Group**:

1.  **`azurerm_resource_group`:** Contêiner lógico para todos os recursos da solução.
2.  **`azurerm_app_service_plan`:** Define o plano de execução (tamanho e *tier*), por exemplo, um plano **Standard S1** para balancear custo e desempenho.
3.  **`azurerm_app_service`:** Hospeda o backend Flask containerizado (Docker). Configurado para extrair a imagem do **Azure Container Registry (ACR)** e expor a porta 5000.
4.  **`azurerm_storage_account`:** Armazena artefatos de ML (`model.pkl`) e logs operacionais, garantindo persistência e acesso global.
5.  **`azurerm_postgresql_flexible_server`:** Servidor de banco de dados relacional (equivalente ao Supabase no *deploy* cloud), provisionado com um *tier* adequado, como **Burstable B1ms**, para a POC.

### Trechos de IaC (Terraform) Destacados

A seguir, um trecho de exemplo para o provisionamento do serviço de aplicação, destacando a utilização do Docker:

```terraform
# Provisionamento do Azure App Service para o backend Flask
resource "azurerm_app_service" "app_service" {
  name                = "asteroid-analysis-app"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  app_service_plan_id = azurerm_app_service_plan.app_plan.id

  # Configuração para rodar container Docker
  site_config {
    linux_fx_version = "DOCKER|${azurerm_container_registry.acr.login_server}/asteroid-app:latest"
    always_on        = true
  }

  app_settings = {
    "DOCKER_REGISTRY_SERVER_URL"      = azurerm_container_registry.acr.login_server
    # Variáveis de ambiente para conexão com o banco...
  }
}
````

-----

## 6\. Pipeline CI/CD

Embora não explicitamente detalhado, o *deploy* eficiente de uma aplicação containerizada em Azure requer um *pipeline* de Integração Contínua e Entrega Contínua (CI/CD).

**Descrição Detalhada do Pipeline (Assumido):**

### 1\. Integração Contínua (CI)

  * **Gatilho:** *Push* ou *Pull Request* para o *branch* `main`.
  * **Job 1 (Build):**
      * Instalar dependências.
      * (Opcional: Rodar Testes Unitários).
      * **Build da Imagem Docker:** Criar a imagem `asteroid-app:$(Build.BuildId)` usando o `Dockerfile`.
      * **Push para ACR:** Autenticar no **Azure Container Registry (ACR)** e fazer *push* da nova imagem.

### 2\. Entrega Contínua (CD)

  * **Gatilho:** Imagem recém-construída no ACR.
  * **Job 2 (Deploy):**
      * **Atualização do Azure App Service:** Conectar ao Azure e forçar o *pull* da *tag* `latest` (ou da *tag* específica do *build*) do ACR.
      * **Swap de Slots (Melhor Prática):** Fazer *deploy* inicialmente em um *Staging Slot* no App Service e, após validação, fazer o *swap* para o *Production Slot*, garantindo *zero downtime*.

**Prints dos Jobs e Logs:**

  * (Não disponível, mas seria o *screenshot* do *pipeline* em execução no Azure DevOps ou GitHub Actions, mostrando o sucesso do *build* da imagem e do *deploy* no App Service).

-----

## 7\. Observabilidade e Desempenho

### Logs, Métricas e Dashboards

  * **Logs:** O Flask gera logs que são configurados para serem capturados pelo **Azure Application Insights** ou pelo próprio **Log Stream** do App Service. É crucial configurar a aplicação para *não logar* dados sensíveis ou chaves.
  * **Métricas de Desempenho (Backend):** O Azure App Service fornece automaticamente métricas de utilização de CPU, memória, taxa de requisições e latência da API.
  * **Métricas de ML:** O arquivo `metrics.json` armazena métricas de treino importantes:
      * **Acurácia (Accuracy)**
      * **Precisão (Precision)**
      * **Recall**
      * **F1-Score** (Crucial, dada a aplicação do SMOTE e o desbalanceamento).
  * **Dashboards:** Um *dashboard* no Azure Monitor seria criado para correlacionar o desempenho da aplicação (latência da API) com a saúde da infraestrutura (uso de CPU e latência do PostgreSQL).

### Resultados de Testes

O modelo **Random Forest**, combinado com o **SMOTE**, é escolhido por sua capacidade de manter um **alto Recall** para a classe minoritária (Perigoso), minimizando Falsos Negativos, que seriam o erro mais crítico neste contexto.

**Tempo de Predição:** Devido ao modelo ser carregado na memória do Flask (`model.pkl`) e ser um modelo de árvore leve, a latência de predição em novas entradas é **muito baixa** (sub-segundo), garantindo uma experiência de usuário rápida.

-----

## 8\. Resultados e Demonstração

### Interface Analítica e Demonstração

A aplicação é demonstrada via *screenshots* (links fornecidos na documentação) e um vídeo demo: [https://youtu.be/GXGgF3xWqFU](https://youtu.be/GXGgF3xWqFU).

  * **Print 1 (Página Inicial):** Visualização geral do sistema e interface para inserção de novos dados. 
  <img width="1362" height="635" alt="image" src="https://github.com/user-attachments/assets/ebb47dcc-72c5-449f-80cb-25b4832b9c76" />

  * **Print 2 (Predição):** Exibe o resultado da predição (Perigoso/Não Perigoso) após a submissão dos atributos do asteroide.
  <img width="1365" height="636" alt="image" src="https://github.com/user-attachments/assets/aeeed488-c09f-4e68-a820-f65a3311ea38" />
  
  * **Print 3 (Métricas):** Painel ou seção mostrando as métricas históricas de *performance* do modelo (Acurácia, F1-Score). 
  <img width="1365" height="651" alt="image" src="https://github.com/user-attachments/assets/c20ded9d-513b-4fc0-b341-db975d7c7334" />


### Métricas Obtidas

A métrica chave é o **F1-Score** e o **Recall** para a classe 'Perigoso'. O uso do **Random Forest** (robusto) e do **SMOTE** (balanceamento) é esperado para garantir um F1-Score competitivo, mesmo em cenários de desbalanceamento de classes, resultando em uma classificação de risco mais confiável.

### Limitações da Solução

1.  **Atualização de Dados:** O sistema depende da frequência de extração do NASA NEO Dataset (via API ou arquivo), não sendo uma solução de *streaming* em tempo real.
2.  **Modelo Fixo:** O modelo `model.pkl` é estático. Requer re-treino manual ou via *pipeline* dedicado para incorporar novos dados históricos e garantir que o modelo não sofra *drift* ao longo do tempo.
3.  **Ambiente POC:** O uso do Supabase/Azure Flexible Server em *tier* básico é dimensionado para uma POC, podendo exigir *upgrade* de *tier* para sustentar milhões de requisições ou um volume massivo de dados.

-----

## 9\. Conclusão e Trabalhos Futuros

### Principais Aprendizados

O projeto demonstrou com sucesso a integração de uma arquitetura *data-intensive* baseada em Machine Learning com infraestrutura em nuvem (Azure/Terraform) e serviços *cloud-native* (Supabase). O principal aprendizado foi o uso eficiente de ferramentas de MLOps (serialização de modelos, `joblib`) para separar o ciclo de treino e *deploy*, resultando em um backend Flask leve e otimizado para predição.

### Melhorias Possíveis e Escalabilidade

1.  **MLOps Completo e Re-treino Automático:** Implementar um *pipeline* CI/CD/CT (Continuous Training) completo que use um *trigger* (ex: novos dados no Supabase) para re-treinar o modelo, avaliar as métricas e fazer o *deploy* da nova versão de `model.pkl` automaticamente para o Azure Storage.
2.  **Arquitetura Serverless:** Migrar o backend Flask para **Azure Functions** ou **Azure Container Apps** (*serverless*), escalando automaticamente de forma mais granular e otimizando custos em períodos de baixo tráfego.
3.  **Modelos Mais Complexos:** Explorar modelos de *Deep Learning* (Redes Neurais) para classificação, potencialmente melhorando a acurácia, especialmente se o volume de dados aumentar significativamente.
4.  **Visualização Avançada:** Integrar um serviço de *dashboard* dedicado (ex: Power BI ou Grafana) para uma visualização mais rica e analítica dos asteroides e métricas.


Link do repositório: https://github.com/raphaobdd/Denis
Link da aplicação: https://asteroide-app-dqe5edbqapbta6ce.brazilsouth-01.azurewebsites.net/
