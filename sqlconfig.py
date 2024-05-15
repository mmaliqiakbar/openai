from promptflow import tool
from promptflow.connections import CustomConnection
import pyodbc
import urllib
import pandas as pd
from sqlalchemy import create_engine, text

def get_table_def(table,engine):
    with engine.connect() as conn:        
        query = f"SELECT COLUMN_NAME, DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME ='{table}'"
        return pd.read_sql(query, conn)


def get_random_rows(table,engine, n=10):
    with engine.connect() as conn:
        query = f'SELECT TOP {n} * FROM {table} ORDER BY NEWID()'
        return pd.read_sql(query, conn)

@tool
def my_python_tool(input1: str) -> str:
    server = 'yourserver.database.windows.net'
    database = 'yourdb'
    username = 'adminuser'
    password = 'yourpassword
    driver = 'ODBC Driver 17 for SQL Server'
    odbc_str = 'DRIVER='+driver+';SERVER='+server+';PORT=1433;UID='+username+';DATABASE='+ database + ';PWD='+ password
    connect_str = 'mssql+pyodbc:///?odbc_connect=' + odbc_str
    engine = create_engine(connect_str)
    tables=['SalesLT.Customer', 'SalesLT.Product', 'SalesLT.ProductDescription', 'SalesLT.ProductModel','SalesLT.ProductCategory','SalesLT.ProductModelProductDescription']
    
    markdown = []
    for table in tables:
        markdown.append(f'### {table}')
        markdown.append(get_table_def(table,engine).to_markdown())
        markdown.append(get_random_rows(table,engine).to_markdown())
        markdown.append('\n')
    table_info = '\n'.join(markdown)
    table_info= table_info+ '\n---\nReturn the TSQL Query for:'

    return table_info
