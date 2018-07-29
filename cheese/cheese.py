import re
from abc import abstractmethod
from bs4 import BeautifulSoup

import requests

import constants


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
        clean_text = re.sub(cleaner, "", text)
        return clean_text

    def extract_meanings(self, words):
        return self.dict_parser.searchdict(words)

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
    def __init__(self, srt_path):
        super(SrtParser, self).__init__()
        with open(srt_path, "r") as f:
            replace_words = [
                ",", ".", "!", "?", '"',
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
            sentences.append(line)
        return sentences


class SmiParser(SubtitleParser):
    def __init__(self):
        pass

    def extract_sentences(self):
        pass


class DictParser():
    def __init__(self):
        self.daum_url = "http://alldic.daum.net/search.do?q={}"

    def searchdict(self, extracted_words):
        meaning_words = {}
        for i, word in enumerate(extracted_words):
            try:
                url = self.daum_url.format(word)
                source = requests.get(url).text
                soup = BeautifulSoup(source, "lxml")
                mdiv = soup.find(
                    "div",
                    attrs={"class": "cleanword_type kuek_type"}
                )
                if mdiv is None:
                    raise NoMeaningWordException(f"NoMeaningWordException: No meaning for this word: {repr(word)}: {url}")  # noqa
                meanings = [t.text for t in mdiv.find_all("li")]
                meaning_words[word] = meanings
                print(word, meanings)
            except NoMeaningWordException as e:
                print(e)
        return meaning_words

    def remove_tag(self, text):
        cleaner = re.compile("<.*?>")
        clean_text = re.sub(cleaner, "", text)
        return clean_text


def main():
    srt_path = "../data/srt/ironman.srt"
    srt = SrtParser(srt_path)
    sentences = srt.extract_sentences()
    extracted_words = srt.extract_words(sentences)
    meanings = srt.dict_parser.searchdict(extracted_words)
    print(meanings)


if __name__ == "__main__":
    main()
