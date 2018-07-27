from cheese import SubtitleParser
from cheese import SrtParser
from cheese import DictParser


def test_srt_extract_meaning():
    srt_file = SrtParser("../data/srt/lionking.srt")
    sentences = srt_file.extract_sentences()
    parser = srt_file.extract_words(sentences)
    meanings = DictParser.searchdict(parser)
    assert meanings == {'day': ['날'], 'arrive': ['도착하다'],
                        'planet': ['행성'], 'blinking': ['가물거리는'],
                        'see': ['보다'], 'step': ['단계'], 'sun': ['태양'],
                        }


def test_srt_extract_words():
    srt_file = SrtParser("../data/srt/lionking.srt")
    sentences = srt_file.extract_sentences()
    words = srt_file.extract_words(sentences)
    assert words == {'day': 1, 'arrive': 1,
                     'planet': 1, 'blinking': 1, 'see': 1, 'step': 1, 'sun': 1,
                     }


def test_srt_extract_sentence():
    srt_file = SrtParser("../data/srt/lionking.srt")
    sentences = srt_file.extract_sentences()
    assert sentences == ["from the day we arrive",
                         "on the planet",
                         "and blinking step into the sun",
                         "there's more to see",
                         ]


def test_remove_tag():
    sub = SubtitleParser()
    sub_line = sub.remove_tag("<i>There's more to see</i>")
    assert sub_line == "There's more to see"

    sub_line = sub.remove_tag("<i>There's more to see</i>")
    assert sub_line == "There's more to see"

    sub_line = sub.remove_tag("<p>There's more to see</p>")
    assert sub_line == "There's more to see"

    sub_line = sub.remove_tag("<p>>There's more to see</p>")
    assert sub_line == ">There's more to see"
