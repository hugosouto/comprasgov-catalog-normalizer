"""
This script reads data from a postgres database, encodes categorical columns to numeric values,
and writes the resulting dataframe to a postgres database.

The script is intended to encode the Materials Catalog of the Federal Government of Brazil for
machine learning. The Materials Catalog is a hierarchical catalogue of materials used by the
Federal Government of Brazil to standardize the procurement process. The catalogue is available
at https://www.gov.br/compras/pt-br/acesso-a-informacao/consulta-detalhada/consulta-detalhada and
downloaded at https://www.gov.br/compras/pt-br/acesso-a-informacao/consulta-detalhada/planilha-
catmat-catser/catmat.xlsx.
"""

# Import libraries
import pandas as pd
import warnings
from sqlalchemy import create_engine
from sql.postgres_connection import (dbname, password, host, port, database)
from sql.sql_queries import (sql_query)
from sklearn.preprocessing import OrdinalEncoder

# Ignore future warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

# Define functions
def read_data_from_postgres(query):
    """
    Read data from postgres database and return a pandas dataframe.

    Args:
        query (str): SQL query to execute.

    Returns:
        pandas.DataFrame: Dataframe with the results of the query.
    """
    try:
        engine = create_engine(f'postgresql://{dbname}:{password}@{host}:{port}/{database}')
        df = pd.read_sql_query(query, engine)
        
    except Exception as e:
        print("An error occurred:", e)
    
    return df

def encode_categorical(df):
    """
    Encode categorical columns to numeric values.

    Args:
        df (pandas.DataFrame): Dataframe to encode.

    Returns:
        pandas.DataFrame: Encoded dataframe.
    """

    # Encode categorical columns to allow ordering by catalogue hierarchy
    df['codigo_grupo_norm'] = df['codigo_grupo'].copy()
    df['codigo_classe_norm'] = df['codigo_grupo'].astype(str) + df['codigo_classe'].astype(str).str.pad(width=4, side='left', fillchar='0')
    df['codigo_pdm_norm'] = df['codigo_classe_norm'].astype(str) + df['codigo_pdm'].astype(str).str.pad(width=5, side='left', fillchar='0')
    df['codigo_item_norm'] = df['codigo_pdm_norm'].astype(str) + df['codigo_item'].astype(str).str.pad(width=6, side='left', fillchar='0')

    # Encode categorical columns to numeric values
    df['codigo_grupo_norm'] = OrdinalEncoder().fit_transform(df[['codigo_grupo_norm']])
    df['codigo_classe_norm'] = OrdinalEncoder().fit_transform(df[['codigo_classe_norm']])
    df['codigo_pdm_norm'] = OrdinalEncoder().fit_transform(df[['codigo_pdm_norm']])
    df['codigo_item_norm'] = OrdinalEncoder().fit_transform(df[['codigo_item_norm']])

    return df

def write_data_to_postgres(df, schema, table_name):
    """
    Write data to postgres database.

    Args:
        df (pandas.DataFrame): Dataframe to write to the database.
        schema (str): Name of the schema to write to.
        table_name (str): Name of the table to write to.
    """
    try:
        engine = create_engine(f'postgresql://{dbname}:{password}@{host}:{port}/{database}')
        df.to_sql(table_name, engine, schema=schema, index=False, if_exists='replace')
        
    except Exception as e:
        print("An error occurred:", e)


# Main function
if __name__ == "__main__":
    """
    Main function that reads data from a postgres database, encodes categorical columns to numeric values,
    and writes the resulting dataframe to a postgres database.
    """
    
    df_original = read_data_from_postgres(sql_query)
    df_norm = encode_categorical(df_original)
    write_data_to_postgres(df_norm, 'catalogo', 'item_material_norm')