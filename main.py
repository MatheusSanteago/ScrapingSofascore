from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options as ChromeOptions

url = 'https://www.sofascore.com/pt/torneio/futebol/brazil/brasileiro-serie-a/325'
teams = []

chrome_options = ChromeOptions()
chrome_options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=chrome_options)


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

        df = dataAjust(table)  # Ajuste no DataFrame
    finally:
        driver.close()


def dataAjust(html):
    df_full = pd.read_html(str(html))[0].head(10)
    df_teams = pd.DataFrame(teams).head(10)
    df_full['Time'] = df_teams.replace(df_teams)
    df_full.drop(columns=['#', 'Dribles realizados'])
    df = df_full.rename(
        columns={'Nota Sofascore': 'Nota', 'Gols esperados (xG)': 'xG'})
    df = df[['Time', 'Nome', 'Gols', 'Assistências',
             'Acerto no passe %', 'xG', 'Nota']]
    return df


makeScraping(url)
