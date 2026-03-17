import os
import re
import requests
from loguru import logger

class LinkValidator:
    def __init__(self, markdown_file):
        self.markdown_file = markdown_file
        self.links = self.extract_links()
        self.broken_links = []

    def extract_links(self):
        """Extracts markdown links from the file."""
        links = []
        try:
            with open(self.markdown_file, 'r', encoding='utf-8') as file:
                content = file.read()
                # Regex to find markdown links [text](url)
                links = re.findall(r'\[.*?\]\((.*?)\)', content)
        except FileNotFoundError:
            logger.error(f"The file {self.markdown_file} does not exist.")
        except Exception as e:
            logger.error(f"An error occurred while reading the file: {e}")
        return links

    def check_link(self, link):
        """Checks if a given link is valid."""
        try:
            response = requests.get(link, allow_redirects=True, timeout=5)
            # Check if the response status code is not in the range of 200-399 (successful responses)
            if response.status_code < 200 or response.status_code >= 400:
                return False
            return True
        except requests.RequestException as e:
            logger.warning(f"Error checking link {link}: {e}")
            return False

    def validate_links(self):
        """Validates all extracted links."""
        for link in self.links:
            if not self.check_link(link):
                self.broken_links.append(link)

    def report_broken_links(self):
        """Reports broken links to the user."""
        if not self.broken_links:
            logger.info("All links are valid!")
        else:
            logger.warning("Broken links found:")
            for link in self.broken_links:
                logger.warning(f"- {link}")

if __name__ == "__main__":
    # Example usage
    markdown_file = 'example.md'  # Replace with your markdown file path
    validator = LinkValidator(markdown_file)
    validator.validate_links()
    validator.report_broken_links()
