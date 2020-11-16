from urllib.error import HTTPError
from urllib.request import urlopen
from bs4 import BeautifulSoup

def get_soup(url):
    """
    Parameters:
        url (String): Web-page url
        
    Returns: Web-page content as a BeautifulSoup object of url, None upon failure.
    """
    try:
        html = urlopen(url)
    except HTTPError as e:
        return None
    try:
        return BeautifulSoup(html.read(), "html.parser")
    except AttributeError as e:
        return None


WORDS_URL = "https://www.dictionary.com/e/word-of-the-day/"

soup = get_soup(WORDS_URL)
item_wrappers = soup.find_all("div", class_="otd-item-wrapper")
print("here")