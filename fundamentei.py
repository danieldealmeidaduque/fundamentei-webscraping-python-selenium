import time
import pandas as pd
from unidecode import unidecode
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By


options = webdriver.ChromeOptions()
# options.add_argument('--ignore-certificate-errors')
# options.add_argument('--incognito')
# options.add_argument('--headless')

driver = webdriver.Chrome(options=options)


def initialize(email, password):
    driver.get("https://fundamentei.com/login")
    driver.find_element(By.NAME, 'email').send_keys(email)
    driver.find_element(By.NAME, 'password').send_keys(password)
    time.sleep(5)
    driver.find_element(By.CLASS_NAME, 'css-1dqkbbj').click()
    time.sleep(5)


def get_company_soup(company):
    driver.get(f'https://www.fundamentei.com/br/{company}')
    html = driver.find_element(By.ID, '__next').get_attribute('innerHTML')
    soup = BeautifulSoup(html, 'html.parser')
    return soup


def soup_table_dataframe(company, soup):
    tabela = soup.find("table")
    # print(tabela)
    df = pd.read_html(str(tabela))[0]
    df.columns = [unidecode(c) for c in df.columns]
    df = df.set_index("Ano")
    # print(df)
    with pd.ExcelWriter('companies.xlsx', engine='openpyxl', mode='a') as writer:
        df.to_excel(writer, sheet_name=company)


if __name__ == '__main__':
    # email = input('Email: ')
    # password = input('Password: ')

    email = 'daniel.dik@hotmail.com'
    password = 'Senha1234'

    initialize(email, password)

    with open('companies.txt', 'r') as f:
        companies = f.read().splitlines()
        for company in companies[:1]:
            try:
                soup = get_company_soup(company)
                cleaned_soup = soup_table_dataframe(company, soup)
            except:
                print(f'NÃO DEU --> {company}')
