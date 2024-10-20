import logging
from config import Config
from web_scraper import scrape_google_and_links, get_image_urls
from content_analyzer import analyze_and_answer
from html_formatter import format_as_html
from utils import save_as_html, get_timestamp, log_transition, call_claude_with_logging
from swarm import Swarm, Agent
from claude_service import call_claude
from flask import Flask, render_template, request, jsonify
import os

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Disable HTTP request logs
logging.getLogger('urllib3').setLevel(logging.WARNING)
logging.getLogger('playwright').setLevel(logging.WARNING)
logging.getLogger('swarm').setLevel(logging.WARNING)
logging.getLogger('anthropic').setLevel(logging.WARNING)

def web_search(query: str) -> str:
    """
    Performs a web search for the given query and analyzes the results.

    Args:
        query (str): The search query.

    Returns:
        str: An answer based on the web search results.
    """
    logging.info(f"Starting web search for query: {query}")
    scraped_contents = scrape_google_and_links(query, Config.MAX_LINKS)
    answer = analyze_and_answer(query, scraped_contents)
    logging.info("Search complete.")
    return answer

def transform_to_html_agent():
    """
    Transforms the current agent to the HTML Formatter agent.

    Returns:
        Agent: The HTML Formatter agent.
    """
    logging.info("Handing off to HTML Formatter agent")
    log_transition("Main Agent", "Formatter Agent")
    return html_agent

def transform_to_web_search_agent():
    """
    Transforms the current agent to the Web Search agent.

    Returns:
        Agent: The Web Search agent.
    """
    logging.info("Handing off to Web Search agent")
    log_transition("Main Agent", "Web Search Agent")
    return web_search_agent

def transform_to_main_agent():
    """
    Transforms the current agent to the Main Agent.

    Returns:
        Agent: The Main Agent.
    """
    logging.info("Handing off to Main Agent")
    log_transition("Web Search Agent", "Main Agent")
    return main_agent

# Create the Swarm client and run the agents
client = Swarm()

html_agent = Agent(
    name="HTML Formatter",
    instructions=Config.HTML_AGENT_INSTRUCTIONS,
    functions=[get_image_urls, call_claude_with_logging],
    model=Config.HTML_MODEL
)

web_search_agent = Agent(
    name="Web Search",
    instructions=Config.WEB_SEARCH_INSTRUCTIONS,
    functions=[web_search, get_timestamp, transform_to_main_agent],
    model=Config.WEB_SEARCH_MODEL
)

main_agent = Agent(
    name="Main Agent",
    instructions=Config.MAIN_AGENT_INSTRUCTIONS,
    functions=[transform_to_web_search_agent, get_timestamp, transform_to_html_agent, call_claude_with_logging],
    model=Config.MAIN_MODEL
)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form['query']
    Config.SEARCH_QUERY = query
    
    response = client.run(
        agent=main_agent,
        messages=[{"role": "user", "content": Config.SEARCH_QUERY}],
        context_variables={
            "Main_Agent_Instructions": Config.MAIN_AGENT_INSTRUCTIONS,
            "HTML_Agent_Instructions": Config.HTML_AGENT_INSTRUCTIONS,
            "Web_Search_Instructions": Config.WEB_SEARCH_INSTRUCTIONS
        }
    )

    answer = response.messages[-1]["content"]
    agent = response.agent.name
    save_as_html(answer, Config.OUTPUT_FILE)
    logging.info(f"Answer saved as {Config.OUTPUT_FILE}")
    logging.info(f"Final agent: {agent}")
    
    with open(Config.OUTPUT_FILE, 'r') as f:
        result_html = f.read()
    
    return jsonify({'result': result_html})

if __name__ == "__main__":
    app.run(debug=True)
