# Perplexity At Home
Everything is Claude generated. Including this README.

This project is an AI-powered search engine that uses web scraping, content analysis, and the Claude API to provide comprehensive answers to user queries.

## Features

- Web scraping of Google search results and linked pages
- Content analysis using the Claude API
- HTML formatting of search results
- User-friendly web interface

## Installation

1. Clone the repository:   ```
   git clone https://github.com/yourusername/ai-search-engine.git
   cd ai-search-engine   ```

2. Create a virtual environment and activate it:   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`   ```

3. Install the required packages:   ```
   pip install -r requirements.txt   ```

4. Set up your Anthropic API key:
   - Create a file named `.env` in the project root
   - Add your API key to the file:     ```
     ANTHROPIC_API_KEY=your_api_key_here     ```

## Usage

1. Run the Flask application:   ```
   python main.py   ```

2. Open a web browser and navigate to `http://localhost:5000`

3. Enter your search query and click "Search" or press Enter

## Configuration

You can modify the `config.py` file to adjust various settings, such as:

- Maximum number of links to scrape
- Output file name
- AI model selection
- Agent instructions

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
