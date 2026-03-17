import os
import re
from urllib.parse import urlparse
from loguru import logger
from rich.console import Console

console = Console()

def is_valid_url(url):
    """
    Check if the provided URL is well-formed.
    Returns True if valid, False otherwise.
    """
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception as e:
        logger.error(f"Error validating URL '{url}': {e}")
        return False

def extract_links_from_markdown(content):
    """
    Extract links from markdown content.
    Returns a list of links found in the content.
    """
    # Regex to match markdown links: [link text](url)
    link_pattern = r'\[.*?\]\((.*?)\)'
    links = re.findall(link_pattern, content)
    return links

def read_markdown_file(filepath):
    """
    Read a markdown file and return its content.
    Raises an error if the file cannot be read.
    """
    if not os.path.isfile(filepath):
        raise FileNotFoundError(f"File '{filepath}' does not exist.")
    
    with open(filepath, 'r', encoding='utf-8') as file:
        return file.read()

def validate_url_format(links):
    """
    Validate a list of links for proper URL format and return a list of malformed links.
    """
    broken_links = []
    for link in links:
        if not is_valid_url(link):
            broken_links.append(link)
    return broken_links

def main(filepath):
    """
    Main function to validate links in a markdown file.
    """
    try:
        content = read_markdown_file(filepath)
        links = extract_links_from_markdown(content)
        broken_links = validate_url_format(links)

        if broken_links:
            console.print("[red]Broken links found:[/red]")
            for link in broken_links:
                console.print(f"[red]- {link}[/red]")
        else:
            console.print("[green]All links are valid![/green]")

    except Exception as e:
        logger.error(f"An error occurred: {e}")

# TODO: Add functionality to check the existence of links over the network.
# TODO: Implement a way to handle relative links based on the markdown file location.
