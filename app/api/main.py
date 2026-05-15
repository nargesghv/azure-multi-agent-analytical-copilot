from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(title="Azure Analytical Copilot")

app.include_router(router)