"""
Main entry point for the customer data analysis application.
Contains the main function to call the agent with user queries.
"""
from app.agent.agent import create_agent, remove_think_tag
from app.utils.helpers import load_dataframes, DataFrameHelper

def initialize_app():
    """Initialize the application by loading data and creating agent."""
    # Load dataframes
    dfs = load_dataframes()
    dfs_helper = DataFrameHelper(dfs)
    
    # Create the agent
    agent = create_agent(dfs_helper)
    
    return agent, dfs_helper

def call_agent(session_id: str, query: str) -> str:
    """
    Call the agent with a user query and return the response.
    
    Args:
        session_id: The session identifier
        query: The user's query
    
    Returns:
        The agent's response with thinking tags removed
    """
    agent, dfs_helper = initialize_app()
    
    response = agent.invoke(
        {
            'messages': query,
            'dataframe': dfs_helper.formated_dataframes(),
            'is_last_step': {"max_steps": 10},
            'remaining_steps': 10
        }, 
        config={'configurable': {'thread_id': session_id}}
    )
    
    return remove_think_tag(response['messages'][-1].content)

if __name__ == "__main__":
    # Example usage
    session_id = "test_session"
    query = "Can you analyze customer spending patterns?"
    
    response = call_agent(session_id, query)
    print(response)