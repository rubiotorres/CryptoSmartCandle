import json
import pandas as pd
from sqlalchemy import create_engine


# '/media/rubio/Backup/Códigos/CryptoSmartCandle/project/environment/currencypairids.csv'
def get_pair_ids(df_path):
    df_currencies = pd.read_csv(df_path)
    list_ids = list(df_currencies[df_currencies['Currency Pair'].str.contains('^BTC_')]['Id'])
    return list_ids, df_currencies


def get_pair_name(dict_currency, currency_id):
    return dict_currency[dict_currency['Id'] == currency_id].iloc[0]['Currency Pair']


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


def get_environment_variables(path):
    with open(path) as json_file:
        return json.load(json_file)
