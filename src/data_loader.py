import sqlite3
import pandas as pd
import numpy as np

def load_data(data):
    df = pd.read_csv(data)

    conn = sqlite3.connect("Telco_Customer_Churn.db")

    df.to_sql(
        "customer_table",
        conn,
        if_exists="replace",
        index=False
    )

    Query = "SELECT * FROM customer_table"

    final_df = pd.read_sql_query(Query,conn)

    conn.close()

    return final_df
