from cheese import SubtitleParser
from cheese import SrtParser
from cheese import DictParser


def test_extract_meaning():
    words = SrtParser("../data/srt/lionking.srt")
    sentences = words.extract_sentences()
    words = words.extract_words(sentences)
    meaning_words = DictParser.searchdict(words)
    assert meaning_words == ['날', '도착하다', '행성', '깜박이는', '단계', '태양', '보다']


def test_extract_words():
    words = SrtParser("../data/srt/lionking.srt")
    sentences = words.extract_sentences()
    words = words.extract_words(sentences)
    assert words == {'day': 1, 'arrive': 1,
                     'planet': 1, 'blinking': 1, 'see': 1, 'step': 1, 'sun': 1,
                     }


def test_extract_sentence():
    sentence = SrtParser("../data/srt/lionking.srt")
    sentences = sentence.extract_sentences()
    assert sentences == ["from the day we arrive",
                   "on the planet",
                   "and blinking step into the sun",
                   "there's more to see",]  # noqa


def test_remove_tag():
    sub = SubtitleParser()
    sub_line = sub.remove_tag("<i>There's more to see</i>", "i")
    assert sub_line == "There's more to see"

    sub_line = sub.remove_tag("<i>There's more to see</i>", "i")
    assert sub_line == "There's more to see"

    sub_line = sub.remove_tag("<p>There's more to see</p>", "p")
    assert sub_line == "There's more to see"

    sub_line = sub.remove_tag("<p>>There's more to see</p>", "p")
    assert sub_line == ">There's more to see"
