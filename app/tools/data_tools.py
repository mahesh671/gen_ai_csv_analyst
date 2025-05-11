"""
Tools for data analysis and entity verification.
"""
import re
from typing import Annotated, Dict, Any, List

import pandas as pd
from langchain.tools import tool
from langgraph.prebuilt import InjectedState

from app.utils.helpers import DataFrameHelper
from app.utils.helpers import load_dataframes, DataFrameHelper
dfs = load_dataframes()
dfs_helper = DataFrameHelper(dfs)

@tool
def verify_entity(df: str, entity_name: str, column_name: str, primary_key_column: str, 
                  state: Annotated[dict, InjectedState]) -> Dict[str, Any]:
    """
    Verify if an entity exists in the specified column of the dataframe. 
    
    Args:
        df: String representation of DataFrame (e.g., "dfs[0]")
        entity_name: The entity name to search for
        column_name: The column name to search in
        primary_key_column: The column name containing the primary key
        state: Injected state containing application state
    
    Returns:
        dict with keys:
        - 'found': bool, whether any matches were found
        - 'exact_match': bool, whether an exact match was found
        - 'matches': list of dicts with matched values and their primary keys
        - 'message': str, message to display to the user
    """
    print(df, entity_name, column_name, primary_key_column)
    
    # Get the DataFrameHelper from injected state or elsewhere
    if not dfs_helper:
        from app.utils.helpers import load_dataframes, DataFrameHelper
        dfs = load_dataframes()
        dfs_helper = DataFrameHelper(dfs)
    
    # Extract dataframe index from the string
    df_index = get_list_index(df)
    if df_index is None:
        return {
            'found': False,
            'exact_match': False,
            'matches': [],
            'message': f"Invalid dataframe reference: {df}. Please use format 'dfs[i]' where i is an integer."
        }
    
    # Get the actual dataframe
    df_actual = dfs_helper.dfs[df_index]
    
    # Convert inputs to lowercase for case-insensitive comparison
    entity_lower = entity_name.lower()
    
    # Step 1: Try exact match (case-insensitive)
    exact_match_rows = df_actual[df_actual[column_name].str.lower() == entity_lower]
    
    # If we find exact matches, return them
    if len(exact_match_rows) > 0:
        exact_matches = format_matches(exact_match_rows, column_name, primary_key_column)
        
        if len(exact_matches) == 1:
            match = exact_matches[0]
            return {
                'found': True,
                'exact_match': True,
                'matches': exact_matches,
                'message': f"Found exact match: {match['entity']} (ID: {match['primary_key']})"
            }
        else:
            match_list = ", ".join([f"{m['entity']} (ID: {m['primary_key']})" for m in exact_matches])
            return {
                'found': True,
                'exact_match': True,
                'matches': exact_matches,
                'message': f"Found multiple exact matches: {match_list}. Please specify which one you mean."
            }
    
    # Step 2: Try partial match (case-insensitive)
    partial_match_rows = df_actual[df_actual[column_name].str.lower().str.contains(entity_lower)]
    
    if len(partial_match_rows) > 0:
        partial_matches = format_matches(partial_match_rows, column_name, primary_key_column)
        match_list = ", ".join([f"{m['entity']} (ID: {m['primary_key']})" for m in partial_matches])
        return {
            'found': True,
            'exact_match': False,
            'matches': partial_matches,
            'message': f"Found similar matches: {match_list}. Please specify which one you mean."
        }
    
    # No matches found
    return {
        'found': False,
        'exact_match': False,
        'matches': [],
        'message': f"No entity matching '{entity_name}' found in {column_name}. Would you like to search for other names or terms?"
    }


def get_list_index(text: str) -> int:
    """
    Extract the index from a string in the format 'dfs[i]'.
    
    Args:
        text: The string containing the index
    
    Returns:
        The index as an integer or None if not found
    """
    match = re.search(r"\[(\d+)\]", text)
    if match:
        return int(match.group(1))
    return None


def format_matches(matched_rows: pd.DataFrame, column_name: str, primary_key_column: str) -> List[Dict[str, Any]]:
    """
    Format matched rows as a list of dictionaries with entity and primary key.
    
    Args:
        matched_rows: DataFrame containing the matched rows
        column_name: The column name containing the entity
        primary_key_column: The column name containing the primary key
    
    Returns:
        List of dictionaries with entity and primary key
    """
    return [
        {
            'entity': row[column_name],
            'primary_key': row[primary_key_column]
        }
        for _, row in matched_rows.iterrows()
    ]