# imports here

from selenium import webdriver
import time
import wget
import requests

# SESSIONID = "2223792612%3A0FcbQOoG8rgg88%3A8"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/79.0.3945.74 Safari/537.36 Edg/79.0.309.43",
    # "cookie": f'sessionid={SESSIONID};'
}

driver = webdriver.Firefox(executable_path=r"C:\Users\IVAR\Downloads\geckodriver-v0.30.0-win64\geckodriver.exe")
driver.get("https://www.instagram.com/officememesforworkingteens/")
time.sleep(10)
driver.maximize_window()
close = driver.find_element_by_xpath('//span[@aria-label="Close"]').click()
reels2 = driver.find_element_by_xpath('//span[text()="Reels"]').click()
time.sleep(10)
reelLinks = set()
retryLinks = set()
reached_page_end = False
last_height = driver.execute_script("return document.body.scrollHeight")

while not reached_page_end:
    allLinks = driver.find_elements_by_tag_name('a')
    hrefLinks = [a.get_attribute('href') for a in allLinks]
    for a in hrefLinks:
        if str(a).startswith("https://www.instagram.com/tv/"):
            reelLinks.add(a)

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    new_height = driver.execute_script("return document.body.scrollHeight")
    time.sleep(5)
    if last_height == new_height:
        reached_page_end = True
    else:
        last_height = new_height

driver.close()
print('Found ' + str(len(reelLinks)) + ' links for Reels')
numberOfReels = len(reelLinks)
count = 0
try:
    for link in reelLinks:
        link2 = "?__a=1"
        url = link + link2
        response = requests.get(url, headers=headers).json()
        if bool(response):
            time.sleep(5)
            video_location = response["graphql"]["shortcode_media"]["video_url"]
            try:
                wget.download(video_location)
            except Exception as e:
                retryLinks.add(url)
            count = count + 1
            print("Downloaded ", count, " of ", numberOfReels, " Reels of the user")
            time.sleep(5)
        else:
            retryLinks.add(url)
except Exception as e:
    print(e)


if bool(retryLinks):
    for link in retryLinks:
        url = link
        try:
            response = requests.get(url, headers=headers).json()
            time.sleep(2)
        except Exception as e:
            print("unable to response for ---", url)
        if bool(response):
            time.sleep(5)
            video_location = response["graphql"]["shortcode_media"]["video_url"]
            wget.download(video_location)
            count = count + 1
            print("Downloaded ", count, " of ", numberOfReels, " Pending Reels of the user")
            time.sleep(5)
        else:
            print("unable to download this --  ", url)

exit()
