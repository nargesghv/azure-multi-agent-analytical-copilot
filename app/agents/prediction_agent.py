from app.tools.azureml_tool import call_prediction_endpoint


def prediction_agent(question: str):
    return call_prediction_endpoint(question)