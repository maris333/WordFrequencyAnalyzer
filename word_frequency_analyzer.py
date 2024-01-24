import requests
import re
from typing import List, Tuple

from bs4 import BeautifulSoup
from requests import RequestException


def open_url(url: str) -> str:
    """
    Open the page with the given URL.

    Parameters:
    - url (str): The URL of the web page.

    Returns:
    str: The HTML content of the web page.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except RequestException as e:
        print(f"Error opening URL: {e}")
        return ""


def extract_text(html_content: str) -> str:
    """
    Extract human-readable text from HTML content.

    Parameters:
    - html_content (str): The HTML content of the web page.

    Returns:
    str: Text containing human-readable content without HTML tags.
    """
    cleaned_text = re.sub(r'<(style|script)[^>]*>.*?</\1>|<[^>]*>', '', html_content, flags=re.DOTALL)
    return cleaned_text


def clean_text(raw_text: str) -> str:
    """
    Clean the text by removing punctuation marks and special characters.

    Parameters:
    - raw_text (str): Raw text containing human-readable content.

    Returns:
    str: Cleaned text without punctuation marks and special characters.
    """
    return re.sub(r'[^\w\s]', '', raw_text)


def analyze_words(text: str) -> List[Tuple[str, int]]:
    """
    Analyze the text by counting the occurrences of each word.

    Parameters:
    - text (str): Text without punctuation marks and special characters.

    Returns:
    list: A list of tuples containing words and their respective counts.
    """
    occs = {}

    for word in text.split():
        if word in occs.keys():
            occs[word] += 1
        else:
            occs[word] = 1

    mapped_words = list(map(lambda items: (items[0], items[1]), occs.items()))
    mapped_words.sort(key=lambda pair: pair[1], reverse=True)

    return mapped_words[:10]


def display_results(most_common_words: List[Tuple[str, int]]) -> None:
    """
    Display the 10 most frequent words with their number of occurrences.

    Parameters:
    - most_common_words (list): A list of tuples containing words and their respective counts.
    """
    for elem, occ in most_common_words[:10]:
        print(f"{elem} : {occ}")


def save_to_file(most_common_words: List[Tuple[str, int]], filename: str = 'results.txt') -> None:
    """
    Save the information to a file.

    Parameters:
    - most_common_words (list): A list of tuples containing words and their respective counts.
    - filename (str): The name of the file to save the information. Default is 'results.txt'.
    """
    with open(filename, 'w') as file:
        for word, count in most_common_words:
            file.write(f'{word}: {count}\n')


def analyze_web_page(url: str) -> None:
    """
    Analyze a web page by opening the URL, extracting text, cleaning HTML, preprocessing text,
    analyzing text, and saving results to a file.

    Parameters:
    - url (str): The URL of the web page.
    """
    html_content = open_url(url)
    extracted_text = extract_text(html_content)
    cleaned_text = clean_text(extracted_text)
    most_common_words = analyze_words(cleaned_text)
    display_results(most_common_words)
    save_to_file(most_common_words)


if __name__ == "__main__":
    url = "https://example.com"
    analyze_web_page(url)
