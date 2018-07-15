from cheese import SubtitleParser
from cheese import SrtParser


def test_extract_words():
    words = SrtParser("../data/srt/lionking.srt")
    temps = words.extract_sentence()
    out = words.extract_words(temps)
    assert out == {'day': 1, 'arrive': 1,
                   'planet': 1, 'blinking,': 1, 'step': 1, 'sun': 1, 'see': 1}

def test_extract_sentence():
    sentence = SrtParser("../data/srt/lionking.srt")
    out = sentence.extract_sentence()
    assert out == ["From the day we arrive",
                   "On the planet",
                   "And, blinking, step into the sun",
                   "There's more to see",]  # noqa

def test_remove_tag():
    sub = SubtitleParser()
    out = sub.remove_tag("<i>There's more to see</i>", "i")
    assert out == "There's more to see"

    out = sub.remove_tag("<i>There's more to see</i>", "i")
    assert out == "There's more to see"

    out = sub.remove_tag("<p>There's more to see</p>", "p")
    assert out == "There's more to see"

    out = sub.remove_tag("<p>>There's more to see</p>", "p")
    assert out == ">There's more to see"
