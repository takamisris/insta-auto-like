# coding:utf-8

# exec -> $ python auto-like-insta.py <user_id>

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

import time
import sys

import datetime

MAIN_URL = "https://www.instagram.com/"
TAG_SEARCH_URL = MAIN_URL + "explore/tags/{}/"
TAG_LIST = ['lol', 'vancouver', 'likeforfollow']

def main():
    try:
        username = sys.argv[1]
        # tag = sys.argv[2]

        option = Options()
        option.add_argument('--headless')
        option.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36")
        driver = webdriver.Chrome('/Users/misris/Program/python/greenteaj/chromedriver', options=option)
        # driver = webdriver.Chrome('/Users/misris/Program/python/greenteaj/chromedriver')
        driver.set_window_size('1200', '1000')
        # driver = webdriver.Chrome('/Users/misris/Program/python/greenteaj/chromedriver')
        driver.get('https://www.instagram.com/accounts/login/?source=auth_switcher')
        print('open instagram...')
        time.sleep(10)

        # login
        id = driver.find_element_by_name("username")
        id.send_keys(username)
        password = driver.find_element_by_name("password")
        password.send_keys("")
        time.sleep(10)
        password.send_keys(Keys.RETURN)
        print('login...')
        time.sleep(10)

        #tag search
        for count in range(1, 12):
            for tag in TAG_LIST:
                tagUrl = TAG_SEARCH_URL.format(tag)
                driver.get(tagUrl)
                print('tag search...')
                time.sleep(10)
                hrefList = []
                for i in range(1, 4):
                    for j in range(1, 4):
                        xpath = '//*[@id="react-root"]/section/main/article/div[2]/div/div[{}]/div[{}]/a'.format(i, j)
                        posts = driver.find_elements_by_xpath(xpath)
                        if len(posts) == 0:
                            continue
                        href = posts[0].get_attribute("href")
                        hrefList.append(href)

                #like
                print('hit like...')
                for href in hrefList:
                    driver.get(href)
                    time.sleep(5)
                    labels = driver.find_elements_by_xpath('//main//section//button/div/span/*[name()="svg"][1]')
                    if len(labels) == 0:
                        continue
                    label = labels[0].get_attribute('aria-label')
                    if label == "Like":
                        driver.find_element_by_xpath('//main//section//button').click()
                        print('hit like! ' + href)

                #done
                f = open('/Users/misris/Program/python/greenteaj/cron.log', 'a')
                f.write('success: ' + tag + ' ' + datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S") + '\n')
                f.close()
            print('wait for 15min...')
            time.sleep(900)

        print('done')
        driver.close()
    except:
        f = open('/Users/misris/Program/python/greenteaj/cron.log', 'a')
        f.write('fail: ' + tag + ' ' + datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + '\n')
        f.close()
        driver.close()

if __name__ == '__main__':
    main()
