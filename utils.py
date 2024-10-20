import os
import logging
from datetime import datetime
from claude_service import call_claude
def save_as_html(content: str, filename: str):
    """
    Saves the given content as an HTML file.

    Args:
        content (str): The HTML content to save.
        filename (str): The name of the file to save the content to.
    """
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)

def get_timestamp() -> str:
    """
    Returns the current timestamp as a string.

    Returns:
        str: The current timestamp in the format 'YYYY-MM-DD HH:MM:SS'.
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def log_transition(from_agent: str, to_agent: str):
    """
    Logs the transition between agents or Claude API calls.

    Args:
        from_agent (str): The name of the agent initiating the transition.
        to_agent (str): The name of the agent or service being transitioned to.
    """
    with open('agent_transitions.log', 'a') as f:
        f.write(f"{from_agent} -> {to_agent}\n")

def call_claude_with_logging(prompt: str, max_tokens: int = 1024):
    """
    Logs the transition to the Claude API.
    """
    log_transition("Agent", "Claude API")
    return call_claude(prompt, max_tokens)
