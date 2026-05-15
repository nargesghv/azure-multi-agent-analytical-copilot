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