import anthropic
from config import Config
import logging

client = anthropic.Anthropic()

def call_claude(prompt: str, max_tokens: int = 1024) -> str:
    """
    Calls the Claude API with the given prompt and returns the response.

    Args:
        prompt (str): The prompt to send to Claude.
        max_tokens (int): The maximum number of tokens in the response. Default is 1024.

    Returns:
        str: Claude's response to the prompt.
    """

    logging.info(f"Calling Claude")

    message = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=max_tokens,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return message.content[0].text
