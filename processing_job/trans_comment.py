import pandas as pd
import datetime

current_date = datetime.datetime.now().strftime("%d-%m-%Y")
filename_open = f"C:/Users/ADMIN/Desktop/app/data/{current_date}_product.txt"
item = pd.read_csv(filename_open)

yesterday_formatted = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%d-%m-%Y")
yesterday_file = f"C:/Users/ADMIN/Desktop/app/data/{yesterday_formatted}_comment.txt"
df_yesterday = pd.read_csv(yesterday_file)

max_customer_yesterday = df_yesterday['Customer_ID'].max()
max_comment_id_yesterday = df_yesterday['cmt_id'].max()


filename_input = f"C:/Users/ADMIN/Desktop/app/Rawdata/{current_date}_comment_customer.txt"
cmt = pd.read_csv(filename_input)
link_to_product_id = pd.Series(item.product_id.values, index=item.link).to_dict()
cmt['product_id'] = cmt['link'].map(link_to_product_id)

# cmt['Customer_ID'] = cmt['name'] + "_" + cmt['date_attend']
# unique_ids = cmt['Customer_ID'].unique()
# id_mapping = {id_: i for i, id_ in enumerate(unique_ids, start=1)}
# cmt['Customer_ID'] = cmt['Customer_ID'].map(id_mapping)
# cmt['cmt_id'] = range(1, len(cmt) + 1)

cmt['Customer_ID'] = range(max_customer_yesterday + 1, max_customer_yesterday + 1 + len(cmt))
cmt['cmt_id'] = range(max_comment_id_yesterday + 1, max_comment_id_yesterday + 1 + len(cmt))

cmt = cmt.drop('link', axis=1)

cmt['num_review'] = cmt['num_review'].str.replace('\n', ' ', regex=False)
cmt['num_thanks'] = cmt['num_thanks'].str.replace('\n', ' ', regex=False)
cmt['time_use'] = cmt['time_use'].str.replace('trướcĐã', 'trước Đã', regex=False)

df_comment = cmt[['Customer_ID', 'product_id', 'comment', 'time_use','cmt_id']]
filename = f"C:/Users/ADMIN/Desktop/app/data/{current_date}_comment.txt"
df_comment.to_csv(filename, sep=',', index=False)

df_customer = cmt[['Customer_ID', 'name', 'num_review', 'num_thanks', 'date_attend']]
df_customer_unique = df_customer.drop_duplicates(subset='Customer_ID')
filename1 = f"C:/Users/ADMIN/Desktop/app/data/{current_date}_customer.txt"
df_customer_unique.to_csv(filename1, sep=',', index=False)
