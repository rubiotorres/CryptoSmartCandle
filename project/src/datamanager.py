import requests
from src.util import get_pair_ids, get_coin_name, engine_create, createTables, upload_table

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
        self.coins_data = requests.get("https://poloniex.com/public?command=returnCurrencies").json()

        schedule.every(1).minutes.do(lambda: self.update_per_period(1))
        schedule.every(5).minutes.do(lambda: self.update_per_period(5))
        schedule.every(10).minutes.do(lambda: self.update_per_period(10))

    def update_per_period(self, period):
        dict_result = {
            "Moeda": [],
            "Periodicidade": [],
            "Datetime": [],
            "Open": [],
            "Low": [],
            "High": [],
            "Close": []
        }
        if period == 1:
            position = 0
        elif period == 5:
            position = 1
        elif period == 10:
            position = 2
        for coin_id in self.data_candle:
            dict_result['Moeda'].append(self.data_candle[coin_id][3])
            dict_result['Periodicidade'].append(str(period) + ' min')
            dict_result['Datetime'].append(self.data_candle[coin_id][4])
            dict_result['Open'].append(self.data_candle[coin_id][position])
            dict_result['Low'].append(self.data_candle[coin_id][5])
            dict_result['High'].append(self.data_candle[coin_id][6])
            dict_result['Close'].append(self.data_candle[coin_id][7])
            self.data_candle[coin_id][position] = self.data_candle[coin_id][7]

        #conn_engine = engine_create(self.environment_variables['database_destiny'])

        df_result = pd.DataFrame(dict_result)
        # Populate table
        #upload_table(conn_engine, df_result, self.environment_variables['table_destiny'], False)

        # Dispose engine
        # conn_engine.dispose()
        df_result.to_csv('my_csv.csv', mode='a', header=False)

    def update_coin_candle(self, coin_id, date, data_coin, coin_price):
        if coin_id in data_coin.keys():
            data_coin[coin_id][4] = date
            data_coin[coin_id][5] = min([data_coin[coin_id][5], coin_price])
            data_coin[coin_id][6] = max([data_coin[coin_id][6], coin_price])
            data_coin[coin_id][7] = coin_price
        else:
            coin = get_coin_name(self.coin_df, coin_id, self.coins_data)
            data_coin[coin_id] = [coin_price, coin_price, coin_price, coin, date, coin_price, coin_price, coin_price]

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