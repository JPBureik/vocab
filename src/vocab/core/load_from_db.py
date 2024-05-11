#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 21 22:33:02 2024

@author: jp
"""

# Standard library imports:
import pandas as pd
from sqlalchemy import create_engine

# Package imports:
from vocab.core.config import mysql_user, mysql_password

def load_from_db(foreign_lang):
    r"""
    Returns a pandas.dataframe containing the database table for foreign_lang.

    Parameters
    ----------
    foreign_lang: str
        Foreign language vocable set to load from database.
    
    Returns
    -------
    table_df: pandas.dataframe
        Contents of the database table.
    """
    
    # Create SQL engine:
    engine = create_engine(f"mysql+mysqlconnector://{mysql_user}"
                           + f":{mysql_password}@localhost/vocab")
    
    # Create SQL query:
    import_query = f"""SELECT * FROM {foreign_lang};"""
    
    # Load table from database:
    table_df = pd.read_sql(import_query, con=engine)
    
    # Use ID column as index:
    table_df.set_index('ID', inplace=True)
    
    return table_df

def save_to_db(foreign_lang, table_df):
    r"""
    Returns a pandas.dataframe containing the database table for foreign_lang.

    Parameters
    ----------
    foreign_lang: str
        Foreign language vocable set to load from database.
    
    Returns
    -------
    table_df: pandas.dataframe
        Contents of the database table.
    """
    
    # Create SQL engine:
    engine = create_engine(f"mysql+mysqlconnector://{mysql_user}"
                           + f":{mysql_password}@localhost/vocab")
    
    # Load table from database:
    table_df.to_sql(foreign_lang, con=engine, if_exists='replace')
