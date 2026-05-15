import mlflow.pyfunc

model = mlflow.pyfunc.load_model("models:/churn-risk-model/Production")


def predict(features):
    return model.predict(features)