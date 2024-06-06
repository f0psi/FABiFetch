import requests,csv 
from datetime import datetime
from bs4 import BeautifulSoup 
from selenium import webdriver
from selenium.webdriver import FirefoxOptions

def log(text, level):
    dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    if level == 0:
        print( dt_string + " | DEBUG | " + text)
    if level == 1: 
        print(dt_string + " | INFO  | " + text)

def startBrowser():
    opts = FirefoxOptions()
    opts.add_argument("--headless")
    browser = webdriver.Firefox(options=opts)
    return browser

def getPrice(cardName, browser):
    log("will check price for [" + cardName + "]",1)
    browser.get("https://www.cardmarket.com/en/FleshAndBlood/Products/Singles/Heavy-Hitters/" + cardName)
    soup = BeautifulSoup(browser.page_source, 'html.parser') 
    for dt in soup.find_all('dt'): 
        if "30-days average price" in str(dt):
            return(dt.find_next("span").get_text())   

def stopBrowser(browser):
    browser.quit()


browser = startBrowser()
data = []

with open ("test.csv", "r") as f:
    for row in csv.reader(f):
        cardName = row[1]
        newPrice = getPrice(cardName, browser)
        data.append([row[0], row[1], newPrice])
        log(newPrice, 0)

with open('test.csv', mode='w') as wf:
    w = csv.writer(wf, delimiter=',')
    w.writerows(data)
