import datetime
import pandas as pd
import undetected_chromedriver as uc 

from time import sleep
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

current_date = datetime.datetime.now().strftime("%d-%m-%Y")
df = pd.read_csv(f"C:/Users/ADMIN/Desktop/app/data/{current_date}_prodcut.txt")  # only take detail prodcut non duplicated

list_link  = list(df['link'])
df_final = pd.DataFrame()
driver = uc.Chrome() 
for i in range(len(list_link)):
    print('crawl link' , i+1)
    driver.get(list_link[i])
    sleep(20)
    pixels_to_scroll = 3000
    driver.execute_script(f"window.scrollBy(0, {pixels_to_scroll});")
    sleep(3)
    page = 1
    comment = []
    name = []
    date_attend = []
    num_review = []
    num_thanks = []
    time_use = []
    link = []
    while page < 5:
        try:
            print('crawl page ' ,page)
            elems = driver.find_elements(By.CSS_SELECTOR , ".jSHEVq .review-comment__user-name")
            if len(elems) == 0:
                break
            else:
                name = name + [elem.text for elem in elems]
                print('--- done get name---')
                print(len(name))
                print('số trang:',page)

            get_cmt = driver.find_elements(By.CSS_SELECTOR , ".review-comment__content")
            comment = comment + [elem.text for elem in get_cmt]
            print('--done get cmt--')
            print(len(comment))

            get_time_use = driver.find_elements(By.CSS_SELECTOR , ".jSHEVq .review-comment__created-date")
            time_use = time_use + [elem.text for elem in get_time_use]
            get_date = driver.find_elements(By.CSS_SELECTOR , ".jSHEVq .review-comment__user-date")
            date_attend = date_attend + [elem.text for elem in get_date]
            print('--done get date--')
            print(len(date_attend))

            rev_thank = driver.find_elements(By.CSS_SELECTOR , ".jSHEVq .review-comment__user-info")
            for j in range(len(rev_thank)):
                if j % 2 == 0:
                    num_review.append(rev_thank[j].text)
                else:
                    num_thanks.append(rev_thank[j].text)
            print('next page')
            try:
                next_page = driver.find_element("xpath" , "/html/body/div[1]/div[1]/main/div/div[2]/div[1]/div[1]/div[3]/div/div[2]/div/div[10]/ul/li[7]")
                next_page.click()
            except NoSuchElementException:
                try:
                    next_page = driver.find_element("xpath" , "/html/body/div[1]/div[1]/main/div/div[2]/div[1]/div[1]/div[3]/div/div[2]/div/div[10]/ul/li[7]/a")
                    next_page.click()
                except NoSuchElementException:
                    next_page = driver.find_element("xpath" , "/html/body/div[1]/div[1]/main/div/div[2]/div[1]/div[1]/div[3]/div/div[2]/div/div[9]/ul/li[5]/a")
                    next_page.click()
            page += 1
            sleep(5)

        except NoSuchElementException:
            print(page)
            break
    for k in range(len(name)):
        link.append(list_link[i])
    print('i' , i)
    print(list_link[i])
    print('độ dài các chuỗi')
    print(len(link))
    print(link)
    print(len(name))
    print(len(comment))
    print(len(num_review))
    print(len(num_thanks))
    print(len(date_attend))
    print(len(time_use))
    df1 = pd.DataFrame({
    'link': link,
    'name': name,
    'comment': comment,
    'num_review': num_review,
    'num_thanks': num_thanks,
    'date_attend': date_attend,
    'time_use' : time_use
})
    
    df_final = pd.concat([df_final, df1], ignore_index=True)

filename = f"C:/Users/ADMIN/Desktop/app/Rawdata/{current_date}_comment_customer.txt"
df_final.to_csv(filename, sep=',', index=False)

driver.close()
