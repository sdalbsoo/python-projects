import re


class SubtitleParser():
    def __init__(self):
        with open("../data/srt/stopwords.txt", "r") as f:
            self.stopwords = set(f.read().split('\n'))

    def remove_tag(self, text, tag):
        regex = f"<{tag}>(.*?)</{tag}>"
        matches = re.finditer(regex, text, re.MULTILINE)
        match = list(matches)[0]
        assert len(match.groups()) == 1
        return match.groups()[0]


class SrtParser(SubtitleParser):
    def __init__(self, srt_path):
        super(SrtParser, self).__init__()
        with open(srt_path, 'r') as f:
            self.lines = f.read().splitlines()

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


class SmiParser():
    def __init__(self):
        pass


def main():
    srt_path = "../data/srt/lionking.srt"
    srt = SrtParser(srt_path)
    sentences = srt.extract_sentences()
    srt.extract_words(sentences)


if __name__ == '__main__':
    main()
