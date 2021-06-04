from datetime import date
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import re
import json

f = open("secret.json")
secret_data = json.load(f)

driver = webdriver.Chrome()
driver.get(secret_data['login_page'])
# Login
driver.find_element_by_id('insert_login').send_keys(secret_data['user'])
driver.find_element_by_id('insert_pwd').send_keys(secret_data['psw'])
driver.find_element_by_xpath('/html/body/div/div/form/div[3]/input').click()
driver.get(secret_data['simulator_page'])


def routine(iteration=-1):
    # Till the button "reload" is present: reload
    while driver.find_element_by_xpath('//*[@id="invia-btn"]').is_displayed():
        driver.find_element_by_xpath('//*[@id="invia-btn"]').click()

    today = date.today()

    # First drop-down menu
    select = Select(driver.find_element_by_xpath('//*[@id="tipo-bando"]'))
    select.select_by_value('ISI2020')
    # ID code
    text = driver.find_element_by_xpath('//*[@id="input-token-fe"]/label').text
    code = driver.find_element_by_xpath('//*[@id="my-token-value"]/strong').text

    n = 11
    if re.search("due", text):
        n = 2
    elif re.search("tre", text):
        n = 3
    elif re.search("quattro", text):
        n = 4
    elif re.search("cinque", text):
        n = 5
    elif re.search("sei", text):
        n = 6
    elif re.search("sette", text):
        n = 7
    elif re.search("otto", text):
        n = 8
    elif re.search("nove", text):
        n = 9
    elif re.search("dieci", text):
        n = 10
    if re.search("^\* Inserire gli ultimi", text):
        # END REGEX
        starting = 64 - n
        regex = "^\+[\w]{" + str(starting) + "}([\w]{" + str(n) + "})"
    else:
        # START REGEX
        regex = "^\+([\w]{" + str(n) + "})"

    trial = re.search(regex, code)
    while not trial:
        trial = re.search(regex, code)
        print("WTF!")
    try:
        requested_code = re.match(regex, code).group(1)
    except AttributeError:
        print("Oh noo...")
        print(text)
        print(code)
        print(regex)
        requested_code = re.match(regex, code)
        print(requested_code)
    driver.find_element_by_xpath('//*[@id="input-token"]').send_keys(requested_code)

    # Date
    driver.find_element_by_xpath('//*[@id="data-odierna"]').send_keys(today.strftime("%d/%m/%Y"))
    # Second drop-down menu
    driver.find_element_by_xpath('//*[@id="data-momento3"]/option[4]').click()
    # tick
    driver.find_element_by_xpath('//*[@id="presa-visione-check"]').click()
    driver.find_element_by_xpath('//*[@id="no-robot-cb"]').click()
    # continue
    driver.find_element_by_xpath('//*[@id="avanti-btn"]').click()
    # ticks
    driver.find_element_by_xpath('//*[@id="consenso-verifica-cb-fe"]/div/label').click()
    driver.find_element_by_xpath('//*[@id="invia-btn"]').click()

    # result
    result = driver.find_element_by_xpath('/html/body/div/div[2]/p[2]/strong').text
    print("Iteration " + str(iteration) + " - Time employed: " + str(result))
    # New simulation
    driver.find_element_by_xpath('//*[@id="invia-btn"]').click()


iteration_n = 0
while True:
    iteration_n += 1
    routine(iteration_n)
