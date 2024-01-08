import pandas as pd
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from seleniumbase import Driver
from selenium.webdriver.common.keys import Keys
from dotenv import load_dotenv
import os
from time import sleep

load_dotenv()
EMAIL=os.environ.get("EMAIL")
HANDLE=os.environ.get("HANDLE")
PASSWORD=os.environ.get("PASSWORD")
COMPANY=os.environ.get("COMPANY")
POSTS=int(os.environ.get("POSTS"))

browser = Driver(browser="chrome",headless=False,headless2=False,headed=True)
browser.get(r"https://twitter.com/explore")
sleep(5)
username = browser.find_element(By.XPATH,r'//*[@class="r-30o5oe r-1niwhzg r-17gur6a r-1yadl64 r-deolkf r-homxoj r-poiln3 r-7cikom r-1ny4l3l r-t60dpp r-1dz5y72 r-fdjqy7 r-13qz1uu"]')
username.send_keys(EMAIL)
next = browser.find_element(By.XPATH,r'//*[@class="css-18t94o4 css-1dbjc4n r-sdzlij r-1phboty r-rs99b7 r-ywje51 r-usiww2 r-2yi16 r-1qi8awa r-1ny4l3l r-ymttw5 r-o7ynqc r-6416eg r-lrvibr r-13qz1uu"]')
next.click()
sleep(5)
username = browser.find_element(By.XPATH,r'//*[@class="r-30o5oe r-1niwhzg r-17gur6a r-1yadl64 r-deolkf r-homxoj r-poiln3 r-7cikom r-1ny4l3l r-t60dpp r-1dz5y72 r-fdjqy7 r-13qz1uu"]')
username.send_keys(HANDLE)
next = browser.find_elements(By.XPATH,r'//*[@role="button"]')[-1]
next.click()
sleep(5)
password = browser.find_element(By.XPATH,r'//*[@class="r-30o5oe r-1niwhzg r-17gur6a r-1yadl64 r-deolkf r-homxoj r-poiln3 r-7cikom r-1ny4l3l r-t60dpp r-1dz5y72 r-fdjqy7 r-13qz1uu"]')
password.send_keys(PASSWORD)
next = browser.find_elements(By.XPATH,r'//*[@role="button"]')[-2]
next.click()
sleep(5)
search = browser.find_element(By.XPATH,r'//*[@class="r-30o5oe r-1niwhzg r-17gur6a r-1yadl64 r-deolkf r-homxoj r-poiln3 r-7cikom r-1ny4l3l r-xyw6el r-13rk5gd r-1dz5y72 r-fdjqy7 r-13qz1uu"]')
search.send_keys(COMPANY)
search.send_keys(Keys.ENTER)

data = set()
nodes = set()
sleep(5)
scroll = 2160
while len(data)<POSTS:
    tweets = browser.find_elements(By.XPATH,r'.//*[@class="css-1dbjc4n r-1iusvr4 r-16y2uox r-1777fci r-kzbkwu"]')
    added = False
    sleep(5)
    for tweet in tweets:
        if tweet in nodes:
            continue
        added=True
        try:
            date = tweet.find_element(By.TAG_NAME,"time").get_attribute("datetime")
            content = tweet.find_element(By.XPATH,r".//*[@class='css-901oao css-cens5h r-1nao33i r-37j5jr r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-bnwqim r-qvutc0']").text
            comments,retweets,likes,views = tweet.find_element(By.XPATH,r".//*[@class='css-1dbjc4n r-1kbdv8c r-18u37iz r-1wtj0ep r-1s2bzr4 r-1ye8kvj']").text.split()
            
            nodes.add(tweet)
            data.add((content,date,comments,retweets,likes,views))
        except Exception:
            continue
    df = pd.DataFrame(data,columns=["content","date","comments","retweets","likes","views"])
    df.to_csv(f"{COMPANY}.csv")
    browser.execute_script(f"window.scrollTo(0, {scroll})")
    scroll+=2160
    if not added:
        break