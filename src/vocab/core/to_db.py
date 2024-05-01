#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 20 22:50:50 2024

@author: jp
"""

# Standard library imports:
from datetime import date
from mysql.connector import connect, Error

# Package imports:
from vocab.core.config import mysql_user, mysql_password

# Add entry to database:
def to_db(vocable, phase=0, date=None):
    """Create new table in db if not present for this atom number and
    write entry for new data to db."""
    if not date:
        vocable_date = date.today().isoformat()
    else:
        vocable_date = date
    
    native_lang = vocable.native_lang
    foreign_lang = vocable.foreign_lang
    native_vocable = vocable.native_vocable
    foreign_vocable = vocable.foreign_vocable
    phase = vocable.phase
    
    # Connect to database:
    try:
        with connect(
            host='localhost',
            user=mysql_user,
            password=mysql_password,
            database='vocab'
        ) as connection:
            with connection.cursor() as cursor:
                
                # Create table for dataset ID's if not present:
                check_table_query = """SHOW TABLES;"""
                cursor.execute(check_table_query)
                tables_result = cursor.fetchall()
                if ('Vocable_IDs', ) not in tables_result:
                    create_table_query = """create table \
                        Vocable_IDs (ID INT AUTO_INCREMENT PRIMARY KEY,\
                                        Language VARCHAR(255));"""
                    cursor.execute(create_table_query)
                    connection.commit()
                    
                # Add entry to dataset_ids table:
                insert_data_query = f"""INSERT INTO Vocable_IDs \
                    (Language) VALUES ('{foreign_lang}')"""
                cursor.execute(insert_data_query)
                connection.commit()
                
                # Retain dataset_id for insertion into atom_nb table:
                cursor.execute('SELECT LAST_INSERT_ID();')
                vocable_id = cursor.fetchall()[0][0]
                
                # Create table if not present for this atom number:
                if (foreign_lang,) not in tables_result:
                    create_table_query = f"""create table \
                        {foreign_lang} (ID INT PRIMARY KEY,\
                                        {native_lang} VARCHAR(255),\
                                        {foreign_lang} VARCHAR(255),\
                                        Phase INT(1),\
                                        Date DATE);"""
                    cursor.execute(create_table_query)
                    connection.commit()
                    
                # Check for duplicates:
                    
                # Insert entry for new data:
                insert_data_query = f"""INSERT INTO {foreign_lang} \
                    (ID, {native_lang}, {foreign_lang}, phase, date) VALUES \
                        ({vocable_id}, '{native_vocable}', '{foreign_vocable}', {phase}, '{vocable_date}');"""
                cursor.execute(insert_data_query)
                connection.commit()
    except Error as e:
        print(e)
        
#%%

# from vocable import Vocable

# voc = Vocable('English', 'Auszeichnung', 'accolade')

# to_db(voc)