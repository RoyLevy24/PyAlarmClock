from urllib.error import HTTPError
from urllib.request import urlopen

from bs4 import BeautifulSoup

from WordItem import *


class WordOfTheDay():

    def __init__(self, num_words=1):
        self.BASE_URL = "https://www.dictionary.com/e/word-of-the-day/"
        self.num_words = num_words

    def get_soup(self, url):
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

    def get_word_title(self, word_item_head):
        title = word_item_head.find(
            "div", class_="otd-item-headword__word").text
        return title

    def get_word_pronounce(self, word_item_head):
        pronounce_div = word_item_head.find(
            "div", class_="otd-item-headword__pronunciation")
        pronounce_div = pronounce_div.find("div")
        pronounce = pronounce_div.text
        pronounce_audio = pronounce_div.find(
            "a", class_="otd-item-headword__pronunciation-audio")
        pronounce_audio = pronounce_audio["href"]

        return pronounce, pronounce_audio

    def get_word_pos_and_meaning(self, word_item_head):
        pos_div = word_item_head.find("div", class_="otd-item-headword__pos")
        pos_list = pos_div.find_all("p")
        pos = pos_list[0].text
        meaning = pos_list[1].text

        return pos, meaning

    def get_word_from_wrapper(self, word_wrap):
        word_item_head = word_wrap.find("div", class_="otd-item-headword")
        title = self.get_word_title(word_item_head)
        pronounce, pronounce_audio = self.get_word_pronounce(word_item_head)
        pos, meaning = self.get_word_pos_and_meaning(word_item_head)

        return {
            "title": title,
            "pronounce": pronounce,
            "pronounce_audio": pronounce_audio,
            "pos": pos,
            "meaning": meaning
        }

    def create_word_item(self, word_item_dict):
        title = word_item_dict["title"]
        pronounce = word_item_dict["pronounce"]
        pronounce_audio = word_item_dict["pronounce_audio"]
        pos = word_item_dict["pos"]
        meaning = word_item_dict["meaning"]

        return WordItem(title, pronounce, pronounce_audio, pos, meaning)

    def create_word_items(self, word_items_dict):
        return [self.create_word_item(word_dict) for word_dict in word_items_dict]

    def create_words_list(self, soup):
        words_list = []
        word_item_wrappers = soup.find_all("div", class_="otd-item-wrapper")
        words_list = [self.get_word_from_wrapper(
            word_wrap) for word_wrap in word_item_wrappers]
        return words_list