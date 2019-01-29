import requests
import re
from abc import abstractmethod
from bs4 import BeautifulSoup
from tqdm import tqdm

import constants
from utils import time_manager


class NoMeaningWordException(Exception):
    def __init__(self, value="NoMeaningWordException"):
        self.value = value

    def __repr__(self):
        return str(self)

    def __str__(self):
        return self.value


class SubtitleParser():
    def __init__(self):
        self.dict_parser = DictParser()
        with open(constants.PATH_STOPWORDS, "r") as f:
            self.stopwords = set(f.read().splitlines())

    def remove_tag(self, text):
        cleaner = re.compile("<.*?>")
        clean_text = re.sub(cleaner, " ", text)
        return clean_text

    def extract_meanings(self, words):
        return self.dict_parser.search_dict(words)

    def extract_words(self, sentences):
        words = {}
        for sentence in sentences:
            for word in sentence.split(" "):
                if word not in self.stopwords:
                    words[word] = words.get(word, 0) + 1
        return words

    @abstractmethod
    def extract_sentences(self):
        pass


class SrtParser(SubtitleParser):
    def __init__(self, srt_path, conDB):
        super(SrtParser, self).__init__()
        self.conDB = conDB
        with time_manager("필요없는 문자 지우기"):
            with open(srt_path, "r", encoding="utf-8-sig") as f:
                replace_words = [
                    ",", ".", "!", "?", '"', "(", ")", ":", "'s", "-", "--",
                    "=", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0",
                    "[", "]", "/", "'d", "'ll", "'d", "'ve",
                ]
                content = f.read()
                for replace_word in replace_words:
                    content = content.replace(replace_word, "")
                self.lines = content.lower().splitlines()

    def extract_sentences(self):
        sentences = []
        for line in self.lines:
            if line.isdigit():
                continue
            if "-->" in line:
                continue
            if len(line) == 0:
                continue
            line = self.remove_tag(line)
            if line == " > ":
                continue
            sentences.append(line)
        return sentences

    def extract_meanings(self, words):
        return self.dict_parser.search_dict(words, self.conDB)


class SmiParser(SubtitleParser):
    def __init__(self, srt_path):
        super(SmiParser, self).__init__()
        with open(srt_path, "r") as f:
            replace_words = [
                ",", ".", "!", "?", '"', '-', '#', ":",
                "=", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0",
                "&nbsp", "krcc"
            ]
            content = f.read()
            for replace_word in replace_words:
                content = content.replace(replace_word, "")
            self.lines = content.lower().splitlines()

    def extract_sentences(self):
        sentences = []
        for line in self.lines:
            tag_line = self.remove_tag(line)
            line = self.remove_style(tag_line)
            sentences.append(line)
        return sentences

    def remove_style(self, text):
        cleaner = re.compile("{.*?}")
        clean_text = re.sub(cleaner, "", text)
        return clean_text


class DictParser():
    def __init__(self):
        self.daum_url = "http://alldic.daum.net/search.do?q={}"

    def parse_mdiv(self, url):
        source = requests.get(url).text
        soup = BeautifulSoup(source, "lxml")
        mdiv = soup.find(
            "div",
            attrs={"class": "cleanword_type kuek_type"}
        )
        return mdiv

    def search_dict(self, extracted_words, conDB):
        count = 0
        meaning_words = {}
        with time_manager("Search dictionary!"):
            for word in tqdm(extracted_words):
                if conDB.search_exiting_dict(word) is None:
                    try:
                        url = self.daum_url.format(word)
                        mdiv = self.parse_mdiv(url)
                        if mdiv is None:
                            raise NoMeaningWordException(f"NoMeaningWordException: No meaning for this word: {repr(word)}: {url}")  # noqa
                        meanings = [t.text for t in mdiv.find_all("li")]
                        conDB.insert_words_table(word, meanings)
                        meaning_words[word] = meanings
                    except NoMeaningWordException as e:
                        print(e)
                else:
                    count += 1
                    sql_meaning = (conDB.search_exiting_dict(word)[1])
                    meaning_words[word] = sql_meaning
        conDB.insert_subdata_table((count/len(extracted_words)*100), count)
        return meaning_words
