import pandas as pd
import undetected_chromedriver as uc 
import datetime

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep

current_date = datetime.datetime.now().strftime("%d-%m-%Y")
df = pd.read_csv(f"C:/Users/ADMIN/Desktop/app/data/{current_date}_prodcut.txt") # only take non duplicated link
list_link = list(df['link'])
sum_info = []
for i in range(len(list_link)):
    information = []
    driver = uc.Chrome() 
    print('--crawl link--',i+1)
    driver.get(list_link[i])
    sleep(10)

    pixels_to_scroll = 2000
    driver.execute_script(f"window.scrollBy(0, {pixels_to_scroll});")
    sleep(10)
    elems = driver.find_elements(By.CSS_SELECTOR , ".eDbeCp span")
    print(elems)
    information = information + [e.text for e in elems]
    print(information)
    information.append(list_link[i])
    sum_info.append(information)
    driver.close()

filename = f"C:/Users/ADMIN/Desktop/app/Rawdata/{current_date}_prodcut_detail.txt"
with open(filename, 'w', encoding='utf-8') as file:
    for sublist in sum_info:
        file.write(', '.join(sublist) + '\n')