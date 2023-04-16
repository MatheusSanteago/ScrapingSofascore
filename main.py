from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By

url = 'https://www.sofascore.com/tournament/football/brazil/brasileiro-serie-a/325'
teams = []


def makeScraping(url):
    try:
        driver = webdriver.Firefox()
        driver.get(url)
        driver.implicitly_wait(10)

        table = driver.find_element(
            By.XPATH, '//*[@id="__next"]/main/div[1]/div[2]/div[1]/div[7]/div/div[3]/div/table')  # Pega por padrão os melhores jogadores pela nota

        data = table.get_attribute('outerHTML')

        soup = BeautifulSoup(data, 'html.parser')
        table = soup.find(name='table')

        for div in table.find_all('a'):
            for img in div.find_all('img', alt=True):
                teams.append(img['alt'])
    finally:
        driver.close()


makeScraping(url)
