from operator import index
from nbformat import write
import pandas as pd
import os
from openpyxl import load_workbook

def read_file(filename):

    df = pd.read_excel(filename)
    df = df[['open', 'high', 'low', 'close','Buy Indicator', 'Sell Indicator']]
    return df

def calculate_index(df, column_name):

    # df -> dataframe
    # column_name -> sell or sell indicator
    index_ = []
    for index, row in df.iterrows():
         if row[column_name] > 0:
            index_.append(index) 

    return index_ 

def equalize_indexes(buy_index, sell_index):

    if len(buy_index) > len(sell_index):
        diff = len(buy_index) - len(sell_index)
        buy_index = buy_index[:len(buy_index)-diff]
    
    elif len(sell_index) > len(buy_index):
        diff = len(sell_index) - len(buy_index)
        sell_index = sell_index[:len(sell_index)-diff]

    return buy_index, sell_index

def create_processed_df(columns):

    df_processed = pd.DataFrame(columns=columns)
    return df_processed

def write_to_df(df_raw, df_processed, t1,t2, i, processed_cols):
        # buy
    df_processed.loc[i, processed_cols[0]] =  df_raw.loc[t1, 'Buy Indicator']
    # Sell
    df_processed.loc[i, processed_cols[1]] = df_raw.loc[t2, 'Sell Indicator']
    # Stop loss
    df_processed.loc[i, processed_cols[2]] = df_raw.loc[t1-3, 'open']

    # min
    df_processed.loc[i, processed_cols[3]] = df_raw[['open', 'high', 'low', 'close']].loc[t1:t2].min().min()
    #max
    df_processed.loc[i, processed_cols[4]] = df_raw[['open', 'high', 'low', 'close']].loc[t1:t2].max().max()

def close_df(processed_df, filename):
    path = os.getcwd()
    path = os.path.join(filename)

    book = load_workbook(path)
    writer = pd.ExcelWriter(path, engine = 'openpyxl')
    writer.book = book

    processed_df.to_excel(writer, sheet_name='processed')
    writer.save
    writer.close()

def calc_profit(df_processed):

    for index, row in df_processed.iterrows():
        if (row['stop_loss'] <= row['min']) and (row['sell'] <= row['max']):
            df_processed.loc[index, 'profit'] = 100 * (row['sell'] - row['buy']) / row['buy']
        elif (row['stop_loss'] >= row['min']):
            df_processed.loc[index, 'profit'] = 100 * (row['stop_loss'] - row['buy']) / row['buy']


def process_dfs(df_raw, df_processed, index_buy, index_sell, filename, processed_cols):


    for i in range(len(index_buy)):
        t1 = index_buy[i]
        t2 = index_sell[i]

        write_to_df(df_raw, df_processed, t1,t2, i, processed_cols)

    calc_profit(df_processed)
    close_df(df_processed, filename)










