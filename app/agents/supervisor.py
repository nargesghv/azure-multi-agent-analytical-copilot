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