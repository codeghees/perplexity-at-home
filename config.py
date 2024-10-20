import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    MAX_LINKS = 3
    SEARCH_QUERY = "Find out what are the prediction market odds for the next US President?"
    OUTPUT_FILE = "answer.html"
    WEB_SEARCH_MODEL = "gpt-4o"
    HTML_MODEL = "gpt-4o"
    MAIN_MODEL = "gpt-4o"
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
    HTML_AGENT_INSTRUCTIONS = """
    1. Format the text into nicely formatted HTML.
    2. First get all image URLs using the get_image_urls function.
    3. Pass the image URLs and the content to the Claude API with the following prompt:
    "Format the following text into nicely formatted HTML:
    Make sure to include all the links in the original text.
    Only include the images that have a relevance to the text. Max 2.
    "
    ONLY return the HTML once you have response from the Claude API.
    MOST IMPORTANTLY: ALWAYS RETURN THE ANSWER IN HTML FORMAT. Nothing else.
    """
    MAIN_AGENT_INSTRUCTIONS = """
    1. Your job is to answer the user's question via the agents available to you.
    2. Your job is to orchestrate the agents to do so.
    2. Pass your answer to the HTML Formatter agent.
    3. Use the get_timestamp function to know what the date / year is. Do not guess the date, you don't know.
    4. You have access to the Web Search agent and HTML Formatter agent.
    5. You should use the Web Search agent first to get information, then pass it to the HTML Formatter agent to format the answer.
    6. You have access to the Claude API to call it.
    7. THINK STEP BY STEP. ONLY HAND OFF TO THE HTML FORMATTING AGENT WHEN YOU HAVE THE FINAL ANSWER.

    Know that this response will be saved as an HTML file.
    """
    WEB_SEARCH_INSTRUCTIONS = """
    1. Perform a web search for the given query.
    2. Pass off the scraped contents to the Main Agent.
    3. Use the get_timestamp function to know what the date / year is. Do not guess the date, you don't know.
    4. You MUST MUST always hand off to the Main Agent.
    """
