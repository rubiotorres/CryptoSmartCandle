import pandas as pd


def get_pair_ids(df_path='/media/rubio/Backup/Códigos/CryptoSmartCandle/project/environment/currencypairids.csv'):
    df_coins = pd.read_csv(df_path)
    list_ids = list(df_coins[df_coins['Currency Pair'].str.contains('^BTC_')]['Id'])
    return list_ids, df_coins


def get_coin_name(dict_coin, id):
    return dict_coin[dict_coin['Id'] == id]['Currency Pair'].reset_index().iloc[0]['Currency Pair']
