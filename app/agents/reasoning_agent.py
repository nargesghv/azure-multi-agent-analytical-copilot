def reasoning_agent(sql_result, rag_result, prediction_result):
    return {
        "analytics": sql_result,
        "evidence": rag_result,
        "predictions": prediction_result,
    }