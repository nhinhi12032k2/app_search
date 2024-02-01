import pyodbc
import pandas as pd
import datetime

server = 'NGUYENTHITHUYNH' 
database = 'TutorialDB' 

cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=' + server + ';DATABASE=' + database + ';Trusted_Connection=yes;')
cursor = cnxn.cursor()

current_date = datetime.datetime.now().strftime("%d-%m-%Y")
df_prodcut = pd.read_csv(f"C:/Users/ADMIN/Desktop/app/data/{current_date}_product.txt", encoding='utf-8')
df_cmt = pd.read_csv(f"C:/Users/ADMIN/Desktop/app/data/{current_date}_comment.txt", encoding='utf-8')
df_customer = pd.read_csv(f"C:/Users/ADMIN/Desktop/app/data/{current_date}_customer.txt", encoding='utf-8')
df_pro_inf = pd.read_csv(f"C:/Users/ADMIN/Desktop/app/data/{current_date}_product_info.txt", encoding='utf-8')


for index, row in df_prodcut.iterrows():
    cursor.execute("INSERT INTO Products (product_id, title, price, link, discount, saled) VALUES (?, ?, ?, ?, ?, ?)", 
                   row.product_id, row.title, row.price, row.link, row.discount, row.saled if pd.notnull(row.saled) else None)
cnxn.commit()
print('--done save prodcut--')

for index, row in df_cmt.iterrows():
    comment_value = None if pd.isnull(row.comment) else row.comment
    time_use_value = None if pd.isnull(row.time_use) else row.time_use

    cursor.execute("INSERT INTO Comments (cmt_id, product_id, Customer_ID, comment, time_use) VALUES (?,?, ?, ?, ?)", 
                   row.cmt_id ,row.product_id, row.Customer_ID, comment_value, time_use_value)

cnxn.commit()
print('done save comment--')

for index, row in df_customer.iterrows():
    cursor.execute("INSERT INTO Customer (Customer_ID, name, num_review, num_thanks, date_attend) VALUES (?,?, ?, ?, ?)", 
                   row.Customer_ID ,row['name'], row.num_review, row.num_thanks, row.date_attend)

cnxn.commit()
print('--done save customer--')

for index, row in df_pro_inf.iterrows():
    voucher_value = None if pd.isnull(row.voucher) else row.voucher
    brand_value = None if pd.isnull(row.brand) else row.brand
    brand_from_value = None if pd.isnull(row.brand_from) else row.brand_from
    country_from_value = None if pd.isnull(row.country_from) else row.country_from
    date_value = None if pd.isnull(row.date) else row.date
    guarantee_value = None if pd.isnull(row.guarantee) else row.guarantee
    time_guarantee_value = None if pd.isnull(row.time_guarantee) else row.time_guarantee
    cursor.execute("INSERT INTO Pro_info (product_id ,voucher, brand, brand_from, country_from, date,guarantee,time_guarantee) VALUES (?,?,?, ?, ?, ?,?,?)", 
                   row.product_id ,voucher_value,brand_value, brand_from_value, country_from_value, date_value,guarantee_value,time_guarantee_value)

cnxn.commit()
print('done save product_info--')
cursor.close()
