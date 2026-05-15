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
