# Django Built-in modules
from django.utils.text import Truncator

# Third party packages
from bs4 import BeautifulSoup


def make_automatic_description(content):
    soup = BeautifulSoup(content, "html.parser")
    paragraphs = soup.find_all(['p', ])
    if paragraphs:
        for paragraph in paragraphs:
            content = paragraph.get_text()
            if content != '':
                return Truncator(content).words(30)
    content = soup.get_text()
    return Truncator(content).words(30)
