import re


class Subtitle():
    def __init__(self):
        with open("../data/srt/stopwords.txt", "r") as f:
            self.stopwords = set(f.read().split('\n'))

    def remove_tag(self, text, tag):
        regex = f"<{tag}>(.*?)</{tag}>"
        matches = re.finditer(regex, text, re.MULTILINE)
        match = list(matches)[0]
        assert len(match.groups()) == 1
        return match.groups()[0]


class Srt(Subtitle):
    def __init__(self, srt_path):
        super(Srt, self).__init__()
        with open(srt_path, 'r') as f:
            self.lines = f.read().splitlines()

    def extract_sentence(self):
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
        temp_list = []
        for sentence in sentences:
            for word in sentence.split(' '):
                if word not in self.stopwords:
                    words[word] = words.get(word, 0) + 1
        print(type(self.stopwords))
        print(self.stopwords)
        print(type(word))
        print(words)
        return words

    def __str__(self):
        return ()

class Smi():
    def __init__(self):
        pass


def main():
    srt_path = "../data/srt/lionking.srt"
    srt = Srt(srt_path)
    sentences = srt.extract_sentence()
    srt.extract_words(sentences)


if __name__ == '__main__':
    main()
