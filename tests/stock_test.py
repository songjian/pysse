import unittest
from sse.stock import Stock
import pandas as pd

class TestSSE(unittest.TestCase):
    def setUp(self):
        self.sse = Stock()

    def test_stock_list(self):
        stock_type = '1'
        result = self.sse.stock_list(stock_type)
        self.assertIsInstance(result, pd.DataFrame)
        self.assertTrue(len(result) > 0)
        
    def test_overview(self):
        date = '20220323'
        result = self.sse.overview(date)
        self.assertIsInstance(result, pd.DataFrame)
        self.assertTrue(len(result) > 0)


if __name__ == '__main__':
    unittest.main()