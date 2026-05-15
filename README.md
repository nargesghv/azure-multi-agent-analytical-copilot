# Azure Multi-Agent Analytical Copilot

Production-grade Azure AI platform combining:

* structured analytics
* unstructured enterprise knowledge
* AI-enriched analytical features
* predictive ML models
* multi-agent orchestration
* MLOps + LLMOps + AgentOps
* AKS deployment
* Azure AI Foundry / Azure OpenAI
* Azure ML
* Databricks + Delta Lake + Unity Catalog

---

# Repository Structure

```text
azure-multi-agent-analytical-copilot/
│
├── README.md
├── docs/
├── infra/
├── data/
├── notebooks/
├── pipelines/
├── src/
├── app/
├── deploy/
├── tests/
├── .github/
├── requirements.txt
├── pyproject.toml
└── Makefile
```

---

# README.md

```md
# Azure Multi-Agent Analytical Copilot

This project implements a production-style enterprise AI analytical copilot on Azure.

The system combines:
- structured business analytics
- unstructured document intelligence
- Azure AI Search RAG
- Azure OpenAI / Azure AI Foundry
- Azure Machine Learning
- LangGraph multi-agent orchestration
- Databricks + Delta Lake + Unity Catalog
- MLOps + LLMOps + AgentOps

## Core Idea

Instead of using unstructured documents only for chatbot retrieval, the system extracts structured business signals from documents and materializes them into Delta tables.

Those extracted signals become ML-ready analytical features used for:
- churn prediction
- operational risk analysis
- anomaly detection
- forecasting

## Architecture

Structured Data + Unstructured Documents
        ↓
ADLS Gen2
        ↓
Databricks + Delta Lake
        ↓
Azure AI Search + Azure OpenAI Extraction
        ↓
Feature Tables
        ↓
Azure ML Training + Inference
        ↓
LangGraph Multi-Agent Copilot
        ↓
Grounded Conversational Analytics

## Main Technologies

- Azure Databricks
- Delta Lake
- Unity Catalog
- Azure AI Search
- Azure OpenAI
- Azure AI Foundry
- Azure ML
- AKS
- LangGraph
- MLflow
- FastAPI
- Terraform
- Kubernetes
```

---

# docs/architecture.md

```md
# Architecture

## Main Components

### Storage
- ADLS Gen2
- Delta Lake

### Processing
- Azure Databricks
- Spark ETL pipelines

### Retrieval
- Azure AI Search

### LLM Layer
- Azure OpenAI
- Azure AI Foundry

### ML Platform
- Azure ML
- MLflow

### Orchestration
- LangGraph
- FastAPI
- AKS

### Governance
- Unity Catalog
- Key Vault
- Private Endpoints
```

---

# infra/terraform/main.tf

```hcl
terraform {
  required_version = ">= 1.5.0"

  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.100"
    }
  }
}

provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "main" {
  name     = var.resource_group_name
  location = var.location
}
```

---

# infra/terraform/networking.tf

```hcl
resource "azurerm_virtual_network" "main" {
  name                = "copilot-vnet"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  address_space       = ["10.0.0.0/16"]
}

resource "azurerm_subnet" "aks" {
  name                 = "aks-subnet"
  resource_group_name  = azurerm_resource_group.main.name
  virtual_network_name = azurerm_virtual_network.main.name
  address_prefixes     = ["10.0.1.0/24"]
}
```

---

# infra/terraform/storage.tf

```hcl
resource "azurerm_storage_account" "lake" {
  name                     = "copilotlakehouse"
  resource_group_name      = azurerm_resource_group.main.name
  location                 = azurerm_resource_group.main.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
  is_hns_enabled           = true
}
```

---

# infra/terraform/aks.tf

```hcl
resource "azurerm_kubernetes_cluster" "aks" {
  name                = "copilot-aks"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  dns_prefix          = "copilotaks"

  default_node_pool {
    name       = "default"
    node_count = 2
    vm_size    = "Standard_D4s_v3"
  }

  identity {
    type = "SystemAssigned"
  }
}
```

---

# infra/terraform/openai.tf

```hcl
resource "azurerm_cognitive_account" "openai" {
  name                = "copilot-openai"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  kind                = "OpenAI"
  sku_name            = "S0"
}
```

---

# infra/terraform/ai_search.tf

```hcl
resource "azurerm_search_service" "search" {
  name                = "copilot-search"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  sku                 = "standard"
}
```

---

# infra/terraform/keyvault.tf

```hcl
resource "azurerm_key_vault" "kv" {
  name                        = "copilot-keyvault"
  location                    = azurerm_resource_group.main.location
  resource_group_name         = azurerm_resource_group.main.name
  tenant_id                   = data.azurerm_client_config.current.tenant_id
  sku_name                    = "standard"
  purge_protection_enabled    = true
  soft_delete_retention_days  = 7
}
```

---

# data/sample_structured/customers.csv

```csv
customer_id,region,segment,monthly_spend,usage_drop_30d
C1029,Ontario,Enterprise,4200,0.31
C2381,Ontario,Enterprise,5100,0.24
```

---

# data/sample_unstructured/transcript_001.txt

```text
Customer repeatedly complained about billing errors and mentioned considering a competitor before renewal.
```

---

# pipelines/databricks/document_chunking.py

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder.getOrCreate()


def chunk_text(text, chunk_size=500, overlap=50):
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap

    return chunks
```

---

# pipelines/databricks/ai_signal_extraction.py

```python
from openai import AzureOpenAI
import json

client = AzureOpenAI(
    api_key="YOUR_KEY",
    api_version="2024-02-15-preview",
    azure_endpoint="YOUR_ENDPOINT"
)


def extract_signals(text: str):
    prompt = f"""
    Extract analytical business signals.

    Return valid JSON.

    Text:
    {text}
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You extract structured business features."},
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )

    return response.choices[0].message.content
```

---

# pipelines/databricks/gold_feature_build.py

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder.getOrCreate()

customers = spark.table("silver.customers_clean")
features = spark.table("silver.extracted_signals")

joined = customers.join(features, on="customer_id", how="left")

joined.write.format("delta").mode("overwrite").saveAsTable(
    "gold.customer_360_features"
)
```

---

# pipelines/azureml/train_pipeline.py

```python
import mlflow
import pandas as pd

from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score


df = pd.read_parquet("data/churn_training_set.parquet")

X = df.drop(columns=["customer_id", "label"])
y = df["label"]

X_train, X_test, y_train, y_test = train_test_split(X, y)

with mlflow.start_run():
    model = XGBClassifier()
    model.fit(X_train, y_train)

    preds = model.predict_proba(X_test)[:, 1]

    auc = roc_auc_score(y_test, preds)

    mlflow.log_metric("auc", auc)
    mlflow.sklearn.log_model(model, "model")
```

---

# src/models/inference.py

```python
import mlflow.pyfunc

model = mlflow.pyfunc.load_model("models:/churn-risk-model/Production")


def predict(features):
    return model.predict(features)
```

---

# app/api/main.py

```python
from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(title="Azure Analytical Copilot")

app.include_router(router)
```

---

# app/api/routes.py

```python
from fastapi import APIRouter
from pydantic import BaseModel

from app.agents.supervisor import run_workflow

router = APIRouter()


class QueryRequest(BaseModel):
    question: str
    user_id: str


@router.post("/ask")
async def ask(request: QueryRequest):
    result = await run_workflow(request.question, request.user_id)
    return result
```

---

# app/agents/supervisor.py

```python
from app.agents.analytics_agent import analytics_agent
from app.agents.rag_agent import rag_agent
from app.agents.prediction_agent import prediction_agent
from app.agents.reasoning_agent import reasoning_agent
from app.agents.summary_agent import summary_agent


async def run_workflow(question: str, user_id: str):
    sql_result = analytics_agent(question)
    rag_result = rag_agent(question)
    prediction_result = prediction_agent(question)

    reasoning = reasoning_agent(
        sql_result,
        rag_result,
        prediction_result,
    )

    final_answer = summary_agent(reasoning)

    return {
        "answer": final_answer,
        "reasoning": reasoning,
    }
```

---

# app/agents/analytics_agent.py

```python
from app.tools.databricks_sql_tool import run_sql


def analytics_agent(question: str):
    sql = "SELECT * FROM gold.customer_360_features LIMIT 5"
    return run_sql(sql)
```

---

# app/agents/rag_agent.py

```python
from app.tools.azure_ai_search_tool import retrieve_chunks


def rag_agent(question: str):
    return retrieve_chunks(question)
```

---

# app/agents/prediction_agent.py

```python
from app.tools.azureml_tool import call_prediction_endpoint


def prediction_agent(question: str):
    return call_prediction_endpoint(question)
```

---

# app/agents/reasoning_agent.py

```python

def reasoning_agent(sql_result, rag_result, prediction_result):
    return {
        "analytics": sql_result,
        "evidence": rag_result,
        "predictions": prediction_result,
    }
```

---

# app/agents/summary_agent.py

```python
from app.tools.openai_tool import summarize


def summary_agent(reasoning):
    return summarize(reasoning)
```

---

# app/tools/openai_tool.py

```python
from openai import AzureOpenAI

client = AzureOpenAI(
    api_key="YOUR_KEY",
    azure_endpoint="YOUR_ENDPOINT",
    api_version="2024-02-15-preview"
)


def summarize(reasoning):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You generate grounded analytical summaries."
            },
            {
                "role": "user",
                "content": str(reasoning)
            }
        ]
    )

    return response.choices[0].message.content
```

---

# app/llmops/guardrails.py

```python
FORBIDDEN_PATTERNS = [
    "DROP TABLE",
    "ignore previous instructions",
]


def validate_prompt(prompt: str):
    for pattern in FORBIDDEN_PATTERNS:
        if pattern.lower() in prompt.lower():
            raise ValueError("Unsafe prompt detected")
```

---

# deploy/docker/Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

# deploy/k8s/deployment.yaml

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: analytical-copilot
spec:
  replicas: 2
  selector:
    matchLabels:
      app: analytical-copilot
  template:
    metadata:
      labels:
        app: analytical-copilot
    spec:
      containers:
        - name: api
          image: acr.azurecr.io/analytical-copilot:latest
          ports:
            - containerPort: 8000
```

---

# deploy/k8s/service.yaml

```yaml
apiVersion: v1
kind: Service
metadata:
  name: analytical-copilot-service
spec:
  selector:
    app: analytical-copilot
  ports:
    - port: 80
      targetPort: 8000
```

---

# .github/workflows/ci.yml

```yaml
name: CI

on:
  push:
    branches:
      - main

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install -r requirements.txt

      - name: Run tests
        run: pytest
```

---

# requirements.txt

```text
fastapi
uvicorn
langgraph
langchain
openai
pyspark
mlflow
xgboost
scikit-learn
pandas
azure-search-documents
azure-identity
azure-ai-ml
pytest
```

---

# Makefile

```makefile
install:
	pip install -r requirements.txt

run:
	uvicorn app.api.main:app --reload

test:
	pytest

docker-build:
	docker build -t analytical-copilot .
```

---

# Final Workflow

```text
New structured + unstructured data
        ↓
ADLS Gen2
        ↓
Databricks + Delta Lake
        ↓
Chunking + Azure AI Search indexing
        ↓
Azure OpenAI / Foundry extraction
        ↓
Structured analytical features
        ↓
Delta feature tables
        ↓
Azure ML model training
        ↓
MLflow + Model Registry
        ↓
Azure ML endpoint deployment
        ↓
User asks analytical question
        ↓
FastAPI + LangGraph on AKS
        ↓
Supervisor routes request
        ↓
Analytics Agent + RAG Agent + Prediction Agent
        ↓
Reasoning Agent
        ↓
Azure OpenAI grounded summary
        ↓
Final analytical response
```
