import requests
from src.util import get_pair_ids, engine_create, upload_table, get_pair_name

from websocket import create_connection
import pandas as pd
import datetime
import json
import schedule


# Abstract class
class DataManager:
    # Class that get data and store
    def __init__(self, environment_variables):
        self.environment_variables = environment_variables
        self.data_candle = {}  # Latest data by currency and opening data
        self.currency_list, self.currency_df = get_pair_ids(environment_variables['CurrencyID_info_path'])
        self.currencies_data = requests.get(environment_variables['currency_info_api']).json()
        self.periods = environment_variables['periods']

        schedule.every(1).minutes.do(lambda: self.update_per_period("1"))
        schedule.every(5).minutes.do(lambda: self.update_per_period("5"))
        schedule.every(10).minutes.do(lambda: self.update_per_period("10"))

    def update_per_period(self, period):
        dict_result = {}
        amt_period = len(self.periods)

        position = self.periods[period][0]
        table_name = self.periods[period][1]
        for currency_id in self.data_candle:
            dict_result.setdefault('Moeda', []).append(self.data_candle[currency_id][amt_period])
            dict_result.setdefault('Periodicidade', []).append(period + ' min')
            dict_result.setdefault('Datetime', []).append(self.data_candle[currency_id][amt_period + 1])
            dict_result.setdefault('Open', []).append(self.data_candle[currency_id][position])
            dict_result.setdefault('Low', []).append(self.data_candle[currency_id][amt_period + 2])
            dict_result.setdefault('High', []).append(self.data_candle[currency_id][amt_period + 3])
            dict_result.setdefault('Close', []).append(self.data_candle[currency_id][amt_period + 4])

            # Update open price
            self.data_candle[currency_id][position] = self.data_candle[currency_id][7]

        conn_engine = engine_create(self.environment_variables['database_destiny'])

        # Populate table
        upload_table(engine=conn_engine,
                     data=pd.DataFrame(dict_result),
                     table=table_name,
                     table_types={},
                     use_index=False
                     )

        # Dispose engine
        conn_engine.dispose()

    def get_currency_name(self, dict_currency, currency_id, currencies_data):
        main_currency = self.environment_variables['main_currency']
        return currencies_data[get_pair_name(dict_currency, currency_id).replace(main_currency + '_', '')]['name']

    def update_currency_candle(self, currency_id, date, data_currency, currency_price):
        amt_period = len(self.periods)
        if currency_id in data_currency.keys():
            data_currency[currency_id][amt_period + 1] = date
            data_currency[currency_id][amt_period + 2] = min(
                [data_currency[currency_id][amt_period + 2], currency_price])
            data_currency[currency_id][amt_period + 3] = max(
                [data_currency[currency_id][amt_period + 3], currency_price])
            data_currency[currency_id][amt_period + 4] = currency_price
        else:
            currency = self.get_currency_name(self.currency_df, currency_id, self.currencies_data)
            data_currency[currency_id] = [currency_price for _ in range(len(self.periods))]
            data_currency[currency_id].extend([currency, date, currency_price, currency_price, currency_price])

    def fetch_new_data(self):
        pass


class DataManagerWebSocket(DataManager):
    def __init__(self, environment_variables):
        super().__init__(environment_variables)
        self.route = '{"command": "subscribe", "channel": 1002}'
        self.web_socket = create_connection(environment_variables['web_socket_url'])
        self.web_socket.send(self.route)
        while 1:
            if len(json.loads(self.web_socket.recv())) > 2:
                break

    def fetch_new_data(self):
        while 1:
            schedule.run_pending()
            result = json.loads(self.web_socket.recv())
            if result[0] == 1010:
                print('Bad Request')
                self.web_socket = create_connection(self.environment_variables['web_socket_url'])
                self.web_socket.send(self.route)
                while 1:
                    if len(json.loads(self.web_socket.recv())) > 2:
                        break
            else:
                currency_id = result[2][0]

                if currency_id in self.currency_list:
                    self.update_currency_candle(currency_id,
                                                datetime.datetime.now(),
                                                self.data_candle,
                                                result[2][1])
        ws.close()


class DataManagerApi(DataManager):
    def __init__(self, environment_variables):
        super().__init__(environment_variables)

    def fetch_new_data(self):
        while 1:
            schedule.run_pending()
            result = requests.get(self.environment_variables['api_url']).json()
            for _, value in result.items():
                currency_id = value['id']

                if currency_id in self.currency_list:
                    self.update_currency_candle(currency_id,
                                                datetime.datetime.now(),
                                                self.data_candle,
                                                value['last'])
