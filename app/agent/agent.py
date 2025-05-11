"""
Agent creation and configuration module.
"""
import re
from typing import Annotated, Sequence, TypedDict

from langgraph.prebuilt import create_react_agent
from langgraph.managed.is_last_step import IsLastStep, RemainingSteps
from langgraph.graph import add_messages
from langgraph.checkpoint.memory import InMemorySaver
from langchain_groq import ChatGroq
from langchain_core.messages import BaseMessage

from app.agent.prompt import get_system_prompt
from app.tools.data_tools import verify_entity
from app.tools.python_tools import create_python_repl_tool
from app.utils.helpers import DataFrameHelper
from app.config.settings import LLM_MODEL,LLM_TEMPERATURE,LLM_TOP_P

class AgentState(TypedDict):
    """Type definition for the agent state."""
    messages: Annotated[Sequence[BaseMessage], add_messages]
    is_last_step: IsLastStep
    dataframe: str
    remaining_steps: RemainingSteps


def remove_think_tag(text: str) -> str:
    """
    Remove <think> tags and their content from the response text.
    
    Args:
        text: The raw response text
    
    Returns:
        Text with thinking tags removed
    """
    cleaned = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL)
    return cleaned


def create_agent(dfs_helper: DataFrameHelper):
    """
    Create and configure the ReAct agent.
    
    Args:
        dfs_helper: DataFrameHelper object containing the dataframes
    
    Returns:
        Configured ReAct agent
    """
    # Create memory saver for the agent
    memory = InMemorySaver()
    
    # Create the tools
    repl_tool = create_python_repl_tool(dfs_helper.dfs)
    
    # Create the LLM
    llm = ChatGroq(
        model=LLM_MODEL,
        temperature=LLM_TEMPERATURE,
        model_kwargs={'top_p':LLM_TOP_P}
    )
    
    # Create the system prompt
    system_prompt = get_system_prompt()
    
    # Create the agent
    agent = create_react_agent(
        model=llm,
        tools=[repl_tool, verify_entity],
        prompt=system_prompt,
        checkpointer=memory,
        state_schema=AgentState
    )
    
    return agent