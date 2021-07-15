import datetime
import json

import MySQLdb
import pandas as pd
from sqlalchemy import create_engine


def get_pair_ids(df_path):
    df_currencies = pd.read_csv(df_path)
    list_ids = list(df_currencies[df_currencies['Currency Pair'].str.contains('^BTC_')]['Id'])
    return list_ids, df_currencies


def get_pair_name(dict_currency, currency_id):
    return dict_currency[dict_currency['Id'] == currency_id].iloc[0]['Currency Pair']


def upload_table(engine, data, table, log_path, table_types={}, use_index=False):
    try:
        data.to_sql(table, con=engine, if_exists="append", index=use_index, dtype=table_types)
        create_log("Added to the {}.".format(table), log_path)
    except Exception as e:
        create_log("Unexpected error: {}.".format(e), log_path)


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


def create_log(msgs, filename):
    f = open(filename, "a")
    f.write("{0} -- {1}\n".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), msgs))
    f.close()


def create_database(database, log_path):
    db = MySQLdb.connect(host=database["host"],  # your host, usually localhost
                         user=database["usr"],  # your username
                         passwd=database["pwd"])  # your password
    cur = db.cursor()
    cur.execute("CREATE DATABASE IF NOT EXISTS {};".format(database["db"]))
    db.commit()
    create_log("Create DataBase {}.".format(database["db"]), log_path)
