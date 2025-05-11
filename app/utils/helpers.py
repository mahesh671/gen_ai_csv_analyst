"""
Helper utilities for data loading, processing, and formatting.
"""
import io
import os
from typing import List

import pandas as pd

from app.config.settings import CSV_DIR


class DataFrameHelper:
    """
    Helper class for working with and formatting DataFrames.
    """
    
    def __init__(self, dfs: List[pd.DataFrame]) -> None:
        """
        Initialize with a list of pandas DataFrames.
        
        Args:
            dfs: List of pandas DataFrames
        """
        self.dfs = dfs

    def formated_dataframes(self) -> str:
        """
        Format dataframes information as a string.
        
        Returns:
            String representation of dataframes info
        """
        output = []
        for i, df in enumerate(self.dfs):
            # Capture df.info() output
            buffer = io.StringIO()
            df.info(buf=buffer)
            info_str = buffer.getvalue()
            buffer.close()

            output.append(f"<dataframe>")
            output.append(f"dfs[{i}] info:")
            output.append(info_str.strip())
            output.append(f"</dataframe>")
        
        return '\n'.join(output)


def load_dataframes() -> List[pd.DataFrame]:
    """
    Automatically load all CSV files from the CSV directory.
    
    Returns:
        List of pandas DataFrames
    """
    dataframes = []
    
    # Check if directory exists
    if not os.path.exists(CSV_DIR):
        print(f"Warning: CSV directory '{CSV_DIR}' does not exist.")
        return dataframes
    
    # Get all CSV files in the directory
    csv_files = [f for f in os.listdir(CSV_DIR) if f.lower().endswith('.csv')]
    
    if not csv_files:
        print(f"Warning: No CSV files found in '{CSV_DIR}'.")
        return dataframes
    
    # Load each CSV file into a dataframe
    for csv_file in csv_files:
        file_path = os.path.join(CSV_DIR, csv_file)
        try:
            print(f"Loading CSV file: {csv_file}")
            df = pd.read_csv(file_path)
            dataframes.append(df)
            print(f"Successfully loaded {csv_file} with {len(df)} rows and {len(df.columns)} columns")
        except Exception as e:
            print(f"Error loading {csv_file}: {str(e)}")
    
    return dataframes