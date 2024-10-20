from typing import List
from web_scraper import get_image_urls

def format_as_html(content: str) -> str:
    """
    Formats the given content as HTML, including images.

    Args:
        content (str): The content to format.

    Returns:
        str: The formatted HTML content.
    """
    image_urls = get_image_urls()
    
    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Search Results</title>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; padding: 20px; }}
            img {{ max-width: 100%; height: auto; margin: 10px 0; }}
        </style>
    </head>
    <body>
        <h1>Search Results</h1>
        <div>{content}</div>
        <h2>Related Images</h2>
        {''.join(f'<img src="{url}" alt="Related image">' for url in image_urls[:5])}
    </body>
    </html>
    """
    return html
