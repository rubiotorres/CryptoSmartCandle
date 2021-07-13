import requests
from src.util import get_pair_ids, get_coin_name, engine_create, upload_table
from sqlalchemy import Float

from websocket import create_connection
import pandas as pd
import datetime
import json
import schedule


class DataManager:
    def __init__(self, environment_variables):
        self.environment_variables = environment_variables
        self.data_candle = {}
        self.coin_list, self.coin_df = get_pair_ids()
        self.coins_data = requests.get(environment_variables['coin_info_api']).json()
        self.periods = environment_variables['periods']

        schedule.every(1).minutes.do(lambda: self.update_per_period("1"))
        schedule.every(5).minutes.do(lambda: self.update_per_period("5"))
        schedule.every(10).minutes.do(lambda: self.update_per_period("10"))

    def update_per_period(self, period):
        dict_result = {}
        amt_period = len(self.periods)

        position = self.periods[period][0]
        table_name = self.periods[period][1]
        for coin_id in self.data_candle:
            dict_result.setdefault('Moeda', []).append(self.data_candle[coin_id][amt_period])
            dict_result.setdefault('Periodicidade', []).append(period + ' min')
            dict_result.setdefault('Datetime', []).append(self.data_candle[coin_id][amt_period + 1])
            dict_result.setdefault('Open', []).append(self.data_candle[coin_id][position])
            dict_result.setdefault('Low', []).append(self.data_candle[coin_id][amt_period + 2])
            dict_result.setdefault('High', []).append(self.data_candle[coin_id][amt_period + 3])
            dict_result.setdefault('Close', []).append(self.data_candle[coin_id][amt_period + 4])

            # Update open price
            self.data_candle[coin_id][position] = self.data_candle[coin_id][7]

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

    def update_coin_candle(self, coin_id, date, data_coin, coin_price):
        amt_period = len(self.periods)
        if coin_id in data_coin.keys():
            data_coin[coin_id][amt_period + 1] = date
            data_coin[coin_id][amt_period + 2] = min([data_coin[coin_id][amt_period + 2], coin_price])
            data_coin[coin_id][amt_period + 3] = max([data_coin[coin_id][amt_period + 3], coin_price])
            data_coin[coin_id][amt_period + 4] = coin_price
        else:
            coin = get_coin_name(self.coin_df, coin_id, self.coins_data)
            data_coin[coin_id] = [coin_price for _ in range(len(self.periods))]
            data_coin[coin_id].extend([coin, date, coin_price, coin_price, coin_price])

    def fetch_new_data(self):
        pass


class DataManagerWebSocket(DataManager):
    def __init__(self, environment_variables):
        super().__init__(environment_variables)
        url = "wss://api2.poloniex.com"
        route = '{"command": "subscribe", "channel": 1002}'
        self.web_socket = create_connection(url)
        self.web_socket.send(route)
        while 1:
            if len(json.loads(self.web_socket.recv())) > 2:
                break

    def fetch_new_data(self):
        while 1:
            schedule.run_pending()
            result = json.loads(self.web_socket.recv())

            coin_id = result[2][0]
            # print(self.data_candle)
            if coin_id in self.coin_list:
                self.update_coin_candle(coin_id,
                                        datetime.datetime.now(),
                                        self.data_candle,
                                        result[2][1])
        ws.close()
