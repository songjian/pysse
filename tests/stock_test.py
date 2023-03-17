import unittest
from sse.stock import overview,profile

class StockTestCase(unittest.TestCase):
    def test_overview(self):
        date = '20220323'
        self.assertEqual(overview(date), 4)