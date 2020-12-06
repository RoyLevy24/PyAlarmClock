import random
from urllib.error import HTTPError
from urllib.request import urlopen

from bs4 import BeautifulSoup

from WordOfTheDay.WordItem import *


class WordOfTheDay():

    def __init__(self, num_words=1):
        self.BASE_URL = "https://www.dictionary.com/e/word-of-the-day/"
        self.WORDS_PER_PAGE = 7
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
            return BeautifulSoup(html.read(), "html.parser", from_encoding="utf-8")
        except AttributeError as e:
            return None
    

    def get_word_title(self, word_item_head):
        title = word_item_head.find(
            "div", class_="otd-item-headword__word").text.strip()
        return title

    def get_word_pronounce(self, word_item_head):
        pronounce_div = word_item_head.find(
            "div", class_="otd-item-headword__pronunciation")
        pronounce_div = pronounce_div.find("div")
        pronounce = pronounce_div.text.strip()
        pronounce_audio = pronounce_div.find(
            "a", class_="otd-item-headword__pronunciation-audio")
        pronounce_audio = pronounce_audio["href"]

        return pronounce, pronounce_audio

    def get_word_pos_and_meaning(self, word_item_head):
        pos_div = word_item_head.find("div", class_="otd-item-headword__pos")
        pos_list = pos_div.find_all("p")
        pos = pos_list[0].text.strip()
        meaning = pos_list[-1].text.strip()

        return pos, meaning

    def get_word_from_wrapper(self, word_wrap):
        word_item_head = word_wrap.find("div", class_="otd-item-headword")
        title = self.get_word_title(word_item_head)
        pronounce, pronounce_audio = self.get_word_pronounce(word_item_head)
        pos, meaning = self.get_word_pos_and_meaning(word_item_head)

        return WordItem(title, pronounce, pronounce_audio, pos, meaning)

    def create_words_list(self, soup):
        words_list = []
        word_item_wrappers = soup.find_all("div", class_="otd-item-wrapper")
        words_list = [self.get_word_from_wrapper(
            word_wrap) for word_wrap in word_item_wrappers]
        return words_list

    def get_words_of_the_day(self):
        soup = self.get_soup(self.BASE_URL)
        words_list = self.create_words_list(soup)
        remaining_words = self.num_words - self.WORDS_PER_PAGE

        while soup != None and remaining_words > 0:
            next_page = soup.find("a", class_="otd-item__load-more")["href"]
            soup = self.get_soup(next_page)
            words_list += self.create_words_list(soup)
            remaining_words -= self.WORDS_PER_PAGE

        words_list = words_list[:self.num_words]
        random.shuffle(words_list)
        return words_list