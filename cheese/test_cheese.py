from pathlib import Path
import os

from cheese import SubtitleParser
from cheese import SrtParser
from connectDB import ConnectDB
import constants


def test_srt_extract_meaning():
    with ConnectDB("localhost", os.environ["USER"], os.environ["PASSWORD"]) as conDB:  # noqa
        conDB.cursor.execute("USE cheese_project")
        srt_parser = SrtParser(constants.PATH_SRT / Path("lionking.srt"), conDB)  # noqa
        sentences = srt_parser.extract_sentences()
        words = srt_parser.extract_words(sentences)
        words.pop('')
        meanings = srt_parser.dict_parser.search_dict(words, conDB)
        answers = {
            "day": '1.날, 2.하루, 3.낮, 4.데이, 5.시절',
            "arrive": '1.도착하다, 2.오다, 3.가다, 4.도래하다, 5.도달하다',  # noqa
            "planet": '1.행성, 2.혹성, 3.유성',
            "blinking": '1.깜박이는, 2.가물거리는, 3.지독한',
            "step": '1.단계, 2.조치, 3.걸음, 4.계단, 5.스텝',
            "sun": '1.태양, 2.해, 3.햇볕',
            "see": '1.보다, 2.알다, 3.만나다, 4.발견하다, 5.이해하다',  # noqa
        }
        assert meanings == answers


def test_srt_extract_words():
    with ConnectDB("localhost", os.environ["USER"], os.environ["PASSWORD"]) as conDB:  # noqa
        srt_parser = SrtParser(constants.PATH_SRT / Path("lionking.srt"), conDB)  # noqa
        sentences = srt_parser.extract_sentences()
        words = srt_parser.extract_words(sentences)
        words.pop('')
        assert words == {
            "day": 1, "arrive": 1,
            "planet": 1, "blinking": 1,
            "see": 1, "step": 1, "sun": 1,
        }


def test_srt_extract_sentence():
    with ConnectDB("localhost", os.environ["USER"], os.environ["PASSWORD"]) as conDB:  # noqa
        srt_parser = SrtParser(constants.PATH_SRT / Path("lionking.srt"), conDB)  # noqa
        sentences = srt_parser.extract_sentences()
        assert sentences == [
            " from the day we arrive ",
            " on the planet ",
            " and blinking step into the sun ",
            " there more to see ",
        ]


def test_remove_tag():
    sub = SubtitleParser()
    sub_line = sub.remove_tag("<i>There's more to see</i>")
    assert sub_line == " There's more to see "

    sub_line = sub.remove_tag("<i>There's more to see</i>")
    assert sub_line == " There's more to see "

    sub_line = sub.remove_tag("<p>There's more to see</p>")
    assert sub_line == " There's more to see "

    sub_line = sub.remove_tag("<p>There's more to see</p>")
    assert sub_line == " There's more to see "
