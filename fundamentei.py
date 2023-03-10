import time
import pandas as pd
from bs4 import BeautifulSoup
from openpyxl import Workbook
from selenium import webdriver
from selenium.webdriver.common.by import By

# Define selenium webdriver options
options = webdriver.ChromeOptions()

# Create selenium webdriver instance
driver = webdriver.Chrome(options=options)


def login_website(email, password):
    ''' Function to login in the website '''

    # go to the website
    driver.get("https://fundamentei.com/login")

    # give email and password to the browser and click to login
    driver.find_element(By.NAME, 'email').send_keys(email)
    time.sleep(.5)
    driver.find_element(By.NAME, 'password').send_keys(password)
    time.sleep(.5)
    driver.find_element(By.CLASS_NAME, 'css-1dqkbbj').click()
    time.sleep(.5)


def get_company_soup(company):
    ''' Get raw html from a company '''

    # access the company website
    driver.get(f'https://www.fundamentei.com/br/{company}')

    # get inner html from company
    html = driver.find_element(By.ID, '__next').get_attribute('innerHTML')

    # transform html into soup
    soup = BeautifulSoup(html, 'html.parser')

    return soup


def soup_to_dataframe(soup):
    ''' Transform soup into dataframe '''

    # find table inside the soup
    table = soup.find("table")

    # transform table into dataframe
    df = pd.read_html(str(table))[0]

    # set 'Ano' column as index of the dataframe
    df = df.set_index("Ano")

    return df


if __name__ == '__main__':
    # account to login
    email = input('Email: ')
    password = input('Password: ')

    # start timer
    start = time.time()

    # login with given email and password
    login_website(email, password)

    # read file with companies codes to get company information
    with open('companies.txt', 'r') as f:
        companies = f.read().splitlines()

        wb = Workbook()
        wb.save('companies_data.xlsx')

        # create excel writer to write company information into sheets
        with pd.ExcelWriter('companies_data.xlsx', engine='openpyxl', mode='a') as writer:

            # get company information and create excel sheet
            for company in companies:
                try:
                    # get html soup
                    soup = get_company_soup(company)
                    # transform soup into dataframe
                    df = soup_to_dataframe(soup)
                    # write dataframe to excel sheet named as the company name
                    df.to_excel(writer, sheet_name=company)
                except:
                    # if we not get the information... just skip it
                    print(f'Could not get {company} information')

        # close driver
        driver.quit()
        # end timer
        end = time.time()

    print(f'Brasilian companies information got in {int(end-start)} s')
