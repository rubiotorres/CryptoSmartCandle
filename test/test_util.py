import unittest
import sys
import pandas as pd
sys.path.append("../project")

from src.util import get_environment_variables, get_pair_ids, get_pair_name


class TestUtil(unittest.TestCase):
    """Tools test"""

    def setUp(self):
        print("Taking environment variables ...")

        self.variable = get_environment_variables("../project/environment/env.json")
        self.test_result = get_environment_variables("./assets/env.json")
        self.df_mock_currency = pd.DataFrame({
            'Id': [0, 1, 2, 3, 4, 5],
            'Currency Pair': ['currency_1', 'currency_2', 'currency_3', 'currency_4', 'currency_5', 'currency_6']
        })

    def test_get_pair_ids(self):
        print("Testing get pair ids...")

        path = self.variable["CurrencyID_info_path"].replace("./environment/", "../project/environment/")
        currency_list, currency_df = get_pair_ids(path)

        self.assertListEqual(currency_list, self.test_result['btc_list_id'])
        self.assertEqual(len(currency_df), self.test_result['len_currency_id'])

    def test_get_pair_name(self):
        print("Testing get pair name...")
        for currency_id in range(6):
            self.assertEqual(get_pair_name(self.df_mock_currency, currency_id),
                             self.test_result['mock_currency_pair'][currency_id])


if __name__ == "__main__":
    unittest.main()
