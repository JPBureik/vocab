#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 12:32:15 2024

@author: jp
"""
# Standard library imports:
import datetime

# Package imports:
from vocab.core.config import session_volume, phase_intervals

def select_for_practice(table_df):
    r"""
    Returns a subsample of table_df containing a random selection of vocable
    items eligible for practice.

    Parameters
    ----------
    table_df: pandas.dataframe
        Contents of the database table.
    
    Returns
    -------
    pract_df: pandas.dataframe
        Subsample of table_df containing selection for practice.
    """

    # Determine days since last practice
    days_since_last_practice = (datetime.date.today()
                                - table_df['Date']).apply(lambda x: x.days)
    
    # Determine items eligible for practice:
    eligible_items = table_df[days_since_last_practice
                              >= table_df.apply(
                                  lambda x: phase_intervals[x['Phase']], axis=1
                                  )
                              ]
    
    # Randomly select from eligible items:
    pract_df = eligible_items.sample(session_volume)
    
    return pract_df
