from app.tools.azure_ai_search_tool import retrieve_chunks


def rag_agent(question: str):
    return retrieve_chunks(question)