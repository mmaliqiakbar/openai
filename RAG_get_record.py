from promptflow import tool
from promptflow.connections import CustomConnection
import urllib
import pandas as pd
from sqlalchemy import create_engine, text

def run_query(query,engine):
    with engine.connect() as conn:
        result =  pd.read_sql(query, conn).to_markdown()
    return result

@tool
def Get_Record(query: str) -> str:
    server = 'yourserver.database.windows.net'
    database = 'yourdb'
    username = 'adminuser'
    password = 'yourpassword'
    driver = 'ODBC Driver 17 for SQL Server'
    odbc_str = 'DRIVER='+driver+';SERVER='+server+';PORT=1433;UID='+username+';DATABASE='+ database + ';PWD='+ password
    connect_str = 'mssql+pyodbc:///?odbc_connect=' + odbc_str
    engine = create_engine(connect_str)
    sql_output=run_query(query,engine)

    return sql_output
