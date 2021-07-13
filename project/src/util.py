import json
import pandas as pd
from sqlalchemy import create_engine


# '/media/rubio/Backup/Códigos/CryptoSmartCandle/project/environment/currencypairids.csv'
def get_pair_ids(df_path='./environment/currencypairids.csv'):
    df_coins = pd.read_csv(df_path)
    list_ids = list(df_coins[df_coins['Currency Pair'].str.contains('^BTC_')]['Id'])
    return list_ids, df_coins


def get_coin_name(dict_coin, coin_id, coins_data):
    return coins_data[dict_coin[dict_coin['Id'] == coin_id]['Currency Pair'].reset_index().iloc[0]['Currency Pair']
        .replace('BTC_', '')]['name']


def upload_table(engine, data, table, table_types={}, use_index=False):
    try:
        data.to_sql(table, con=engine, if_exists="append", index=use_index, dtype=table_types)
        print("Added to the {}.".format(table))
    except Exception as e:
        print("Unexpected error:", e)


def engine_create(database):
    url = "mysql://{user}:{pw}@{host}/{db}".format(
        host=database["host"],
        user=database["usr"],
        pw=database["pwd"],
        db=database["db"],
    )
    return create_engine(url)


def get_environment_variables():
    try:
        with open("./environment/env.json") as json_file:
            return json.load(json_file)
    except Exception as e:
        print("Unexpected error:", e)
        with open("./environment/env.json") as json_file:
            return json.load(json_file)
