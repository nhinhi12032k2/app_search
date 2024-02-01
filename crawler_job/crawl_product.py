import random
import pandas as pd
import undetected_chromedriver as uc 
import datetime

from split_price_discount import split_price_discount
from time import sleep
from selenium.webdriver.common.by import By

driver = uc.Chrome()  
driver.get("https://tiki.vn/cham-soc-da-mat/c1582?sort=newest&page=1")

sleep(15)
page = 1
title = []
links = []
price_list = []
discount_list = []
saled = []
len_title = []
while page < 2:
    print('crawl page ' ,page)
    elems = driver.find_elements(By.CSS_SELECTOR , ".name")
    title = title + [elem.text for elem in elems]
    print('--- done get title---')
    print(len(title))
    len_title.append(len(title))

    get_links = driver.find_elements(By.CSS_SELECTOR , ".jXFjHV .product-item")
    links = links + [elem.get_attribute('href') for elem in get_links]
    print('--done get link--')
    print(len(links))

    get_saled = driver.find_elements(By.CSS_SELECTOR , ".dTMgfN span")
    saled = saled + [elem.text for elem in get_saled]
    print('--done get saled--')
    print(len(saled))


    price_discount = driver.find_elements(By.CSS_SELECTOR , ".lkhWwf .price-discount")
    price = [elem.text for elem in price_discount]
    price = split_price_discount(price)
    price_list = price_list + price[0]
    discount_list = discount_list + price[1]
    print('--done get discount--')
    print(len(discount_list))
    print('--done get price--')
    print(len(price_list))
    print('next page')
    page += 1
    driver.get("https://tiki.vn/cham-soc-da-mat/c1582?sort=newest&page="+str(page))
    sleep(20)
    if page >2:
        if len_title[-1] == len_title[-2]:
            break
    else:
        continue

df1 = pd.DataFrame(list(zip(title,price_list,links,discount_list,saled)), columns=['title' , 'price' ,'link' ,'discount','saled'])
current_date = datetime.datetime.now().strftime("%d-%m-%Y")
filename = f"C:/Users/ADMIN/Desktop/app/Rawdata/{current_date}_product.txt"
df1.to_csv(filename, sep=',', index=False)
driver.close()
