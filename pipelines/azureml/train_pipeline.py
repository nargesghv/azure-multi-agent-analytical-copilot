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