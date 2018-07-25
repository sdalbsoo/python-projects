import re
from abc import abstractmethod
from bs4 import BeautifulSoup

import requests

import constants


class SubtitleParser():
    def __init__(self):
        self.meaning_words = DictParser()  # meaning_words가 DictParser를 가진다.
        with open(constants.PATH_STOPWORDS, "r") as f:
            self.stopwords = set(f.read().splitlines())

    def remove_tag(self, text, tag):
        regex = f"<{tag}>(.*?)</{tag}>"
        matches = re.finditer(regex, text, re.MULTILINE)
        match = list(matches)[0]
        assert len(match.groups()) == 1
        return match.groups()[0]

    @abstractmethod
    def extract_sentences(self):
        pass

    @abstractmethod
    def extract_word(self):
        pass


class SrtParser(SubtitleParser):
    def __init__(self, srt_path):
        super(SrtParser, self).__init__()
        with open(srt_path, 'r') as f:
            self.lines = f.read().replace(',', '').lower().splitlines()

    def extract_sentences(self):
        sentences = []
        for line in self.lines:
            if line.isdigit():
                continue
            if '-->' in line:
                continue
            if len(line) == 0:
                continue
            line = self.remove_tag(line, 'i')
            sentences.append(line)
        return sentences

    def extract_words(self, sentences):
        words = {}
        for sentence in sentences:
            for word in sentence.split(' '):
                if word not in self.stopwords:
                    words[word] = words.get(word, 0) + 1
        return words


class SmiParser(SubtitleParser):
    def __init__(self):
        pass

    def extract_sentences(self):
        pass

    def extract_words(self):
        pass


class DictParser():
    def searchdict(extractwords):
        meaning_words = []
        for key, value in extractwords.items():
            url = 'http://alldic.daum.net/search.do?q={}'.format(key)
            response = requests.get(url)
            source = response.text
            soup = BeautifulSoup(source, 'lxml')
            parsed = soup.find('span', class_='txt_search')
            meaning_words.append(parsed.string)
        return meaning_words


def main():
    srt_path = "../data/srt/lionking.srt"
    srt = SrtParser(srt_path)
    sentences = srt.extract_sentences()
    extractwords = srt.extract_words(sentences)
    meaning_words = DictParser.searchdict(extractwords)
    print(meaning_words)


if __name__ == '__main__':
    main()
