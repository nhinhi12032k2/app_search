import pandas as pd
import datetime

current_date = datetime.datetime.now().strftime("%d-%m-%Y")
filename_open = f"C:/Users/ADMIN/Desktop/app/data/{current_date}_product.txt"
item = pd.read_csv(filename_open)

file_name = f"C:/Users/ADMIN/Desktop/app/Rawdata/{current_date}_prodcut_detail.txt"
lines = []
with open(file_name, 'r', encoding='utf-8') as file:
    for line in file:
        if 'http' in line:
            lines.append(line)

keywords = ['Mã Giảm Giá','Thương hiệu', 'Xuất xứ thương hiệu', 'Xuất xứ', 'Hạn sử dụng', 'được bảo hành không','Thời gian bảo hành','link']
df = pd.DataFrame(columns=keywords)
for line in lines:
    parts = [part.strip() for part in line.split(',') if part.strip()]
    product_info = {key: None for key in keywords}
    for i, part in enumerate(parts):
        if 'http' in part:
            product_info['link'] = part
        if 'Mã Giảm Giá' in part:
            product_info['Mã Giảm Giá'] = part[0]
        else:
            for key in keywords:
                if key in part and key != 'link' and key != 'Mã Giảm Giá':
                    try:
                        product_info[key] = parts[i + 1]
                    except IndexError:
                        product_info[key] = None

    df.loc[len(df)] = product_info

df.fillna(value=pd.NA, inplace=True)

link_to_product_id = pd.Series(item.product_id.values, index=item.link).to_dict()
df['product_id'] = df['link'].map(link_to_product_id)
df = df.drop('link', axis=1)

df = df.rename(columns={
    'Mã Giảm Giá': 'voucher',
    'Thương hiệu': 'brand',
    'Xuất xứ thương hiệu': 'brand_from',
    'Xuất xứ': 'country_from',
    'Hạn sử dụng': 'date',
    'được bảo hành không': 'guarantee',
    'Thời gian bảo hành': 'time_guarantee'
})
df_unique = df.drop_duplicates(subset='product_id')
filename1 = f"C:/Users/ADMIN/Desktop/app/data/{current_date}_product_info.txt"
df_unique.to_csv(filename1, sep=',', index=False)