import unittest

from application.recurrence import newsEveryDay


class TestRecurrence(unittest.TestCase):
    def test_whenGivenGoodTime_SendNews(self):
        self.assertTrue(len(newsEveryDay(10)) != 0)

    def test_whenGivenBadTime_DontSendNews(self):
        self.assertIsNone(newsEveryDay(5))
