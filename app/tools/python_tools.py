"""
Python-related tools including the Python REPL tool.
"""
import pandas as pd
import numpy as np
from typing import List
from langchain_experimental.tools import PythonAstREPLTool


def create_python_repl_tool(dataframes: List[pd.DataFrame]) -> PythonAstREPLTool:
    """
    Create a Python REPL tool with dataframes included in the locals.
    
    Args:
        dataframes: List of pandas DataFrames to include in the REPL
    
    Returns:
        Configured PythonAstREPLTool
    """
    # Create the REPL tool with dataframes in locals
    repl_tool = PythonAstREPLTool(
        locals={
            'dfs': dataframes,
            'pd': pd,
            'np':np,
            'numpy': __import__('numpy'),
        }
    )
    
    return repl_tool