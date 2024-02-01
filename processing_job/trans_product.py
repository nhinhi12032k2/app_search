import pandas as pd
import datetime

yesterday_formatted = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%d-%m-%Y")
yesterday_file = f"C:/Users/ADMIN/Desktop/app/data/{yesterday_formatted}_product.txt"
df_yesterday = pd.read_csv(yesterday_file)

max_product_id_yesterday = df_yesterday['product_id'].max()

current_date = datetime.datetime.now().strftime("%d-%m-%Y")
filename_input = f"C:/Users/ADMIN/Desktop/app/Rawdata/{current_date}_product.txt"
item_new = pd.read_csv(filename_input)

item_new.loc[item_new['discount'] == '%', 'discount'] = '0%'
item_new['price'] = item_new['price'].str.replace('.', '').str.replace('₫', '')

links_in_yesterday = df_yesterday['link']
item_new = item_new[~item_new['link'].isin(links_in_yesterday)]

item_new = item_new.reset_index(drop=True)
item_new['product_id'] = range(max_product_id_yesterday + 1, max_product_id_yesterday + 1 + len(item_new))

filename_output = f"C:/Users/ADMIN/Desktop/app/data/{current_date}_product.txt"
item_new.to_csv(filename_output, sep=',', index=False)