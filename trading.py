import pandas as pd
import common
import argparse
import yaml


ap = argparse.ArgumentParser()
ap.add_argument('Filename')

args = ap.parse_args()
filename = args.Filename

with open('params.yaml') as file:
    params = yaml.safe_load(file)

buy_column = params['buy_column']
sell_column = params['sell_column']

processed_cols = params['processed_df_cols']

def run():

    df_raw =  common.read_file(filename)

    indexes_buy = common.calculate_index(df_raw, buy_column)
    indexes_sell = common.calculate_index(df_raw, sell_column)

    indexes_buy, indexes_sell = common.equalize_indexes(indexes_buy, indexes_sell)
    
    processed_df = common.create_processed_df(processed_cols)
    
    common.process_dfs(df_raw, processed_df, indexes_buy, indexes_sell, filename, processed_cols)

   
if __name__ == "__main__":
    run()










   