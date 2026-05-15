from app.tools.databricks_sql_tool import run_sql


def analytics_agent(question: str):
    sql = "SELECT * FROM gold.customer_360_features LIMIT 5"
    return run_sql(sql)