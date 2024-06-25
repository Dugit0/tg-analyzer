import datetime
from pathlib import Path
import sys
import unittest
import pytz

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
# import tganalyzer
from tganalyzer.core.creator import start_creator
from tganalyzer.core.analyzer import start_analyses
from pprint import pprint

PATH = str(Path(__file__).resolve().parent / "data.json")
FEATURES = ["symb", "word", "msg", "voice_message", "video_message",
            "video_file", "photo", "day_night"]
CHAT_ID = 1012308965

class CoreTest(unittest.TestCase):
    def setUp(self):
        chats = start_creator(PATH)
        features = {feature: True for feature in FEATURES}
        time_gap = [datetime.datetime(2019, 1, 1, 0, 0, 0, 0, pytz.UTC),
                    datetime.datetime(2025, 1, 1, 0, 0, 0, 0, pytz.UTC)]
        self.stats, _ = start_analyses(chats, time_gap, features)

    def tearDown(self):
        del self.stats

    def __test_counted_feature(self, feature, simple_control_values):
        dates = [tuple(date for date in self.stats[feature][CHAT_ID][name])
                 for name in self.stats[feature][CHAT_ID]]
        example_date = dates[0]
        for i in range(1, len(dates)):
            self.assertEqual(example_date, dates[i])

        control_values_gen = (i for i in simple_control_values)
        control_values = {name: {date: next(control_values_gen) 
                                 for date in example_date}
                          for name in self.stats[feature][CHAT_ID]}

        pprint(self.stats[feature][CHAT_ID])
        pprint(control_values)
        for name in self.stats[feature][CHAT_ID]:
            for date in example_date:
                self.assertEqual(self.stats[feature][CHAT_ID][name][date],
                                 control_values[name][date])
    
    def test_symb(self):
        self.__test_counted_feature("symb", (34, 230, 128, 17))

    def test_word(self):
        self.__test_counted_feature("word", (8, 41, 21, 5))

    def test_msg(self):
        self.__test_counted_feature("msg", (2, 4, 4, 5))
