from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
import re
import json
import time
import datetime

f = open("secret.json")
secret_data = json.load(f)

driver = webdriver.Chrome()
driver.get(secret_data['login_page'])
# Login
driver.find_element(By.ID, 'insert_login').send_keys(secret_data['user'])
driver.find_element(By.ID, 'insert_pwd').send_keys(secret_data['psw'])
driver.find_element(By.XPATH, '/html/body/div/div/form/div[3]/input').click()
driver.get(secret_data['simulator_page'])


def routine(iteration=-1):
    # Till the button "reload" is present: reload
    while driver.find_element(By.XPATH, '//*[@id="invia-btn"]').is_displayed():
        driver.find_element(By.XPATH, '//*[@id="invia-btn"]').click()

    # First drop-down menu
    select = Select(driver.find_element(By.XPATH, '//*[@id="tipo-bando"]'))
    select.select_by_value('ISI2020')

    # ID code
    text = driver.find_element(By.XPATH, '//*[@id="input-token-fe"]/label').text
    code = driver.find_element(By.XPATH, '//*[@id="my-token-fe"]/input').get_property("value")

    n = int(driver.find_element(By.XPATH, '//*[@id="input-token"]').get_attribute("maxlength"))
    groups = 1

    if re.search("numer", text):
        base_re = "[a-z]*([0-9]*)[a-z]*"
    else:
        base_re = "[0-9]*([a-z]*)[0-9]*"

    last = False

    if re.search("^\* Inserire gli ultimi [a-z]+ caratteri", text):
        starting = 64 - n
        regex = "^\+[\w]{" + str(starting) + "}([\w]{" + str(n) + "})"
    # Ultime cifre oppure ultime lettere
    elif re.search("^\* Inserire .+ ultim", text):
        regex = "^\+[0-9a-z]{30}" + base_re * 30
        groups = 30
        last = True
    # Prime cifre oppure prime lettere
    elif re.search("^\* Inserire .+ prim", text):
        regex = "^\+" + base_re * n
        groups = n
    # Numero tra parentesi
    elif re.search("^\* Inserire il numero tra parentesi", text):
        regex = "tra parentesi \(([0-9]+)\)"
    # Prime cifre o lettere
    else:
        # START REGEX
        regex = "^\+([\w]{" + str(n) + "})"

    trial = re.search(regex, code)
    while not trial:
        trial = re.search(regex, code)
        print("WTF!")
    try:
        requested_code = ""
        for i in range(groups):
            requested_code += re.match(regex, code).group(i+1)
    except AttributeError:
        print("Oh noo...")
        print(text)
        print("||" + code + "||")
        print(regex)
        print("Is match?")
        print(re.match(regex, code).group())
        print("has it been match?")
        requested_code = "REINITIALISED-"
        for i in range(groups):
            requested_code += re.match(regex, code).group(i+1)
        print(requested_code)
    if last:
        requested_code = requested_code[-n:]
    driver.find_element(By.XPATH, '//*[@id="input-token"]').send_keys(requested_code[0:n])

    # Date
    text = driver.find_element(By.XPATH, '//*[@id="data-odierna-fe"]/label').text
    data = datetime.date.today()
    if re.search("^\* Data di domani", text):
        data += datetime.timedelta(days=1)
    elif re.search("^\* Data di ieri", text):
        data -= datetime.timedelta(days=1)
    data = data.strftime("%d/%m/%Y")
    driver.find_element(By.XPATH, '//*[@id="data-odierna"]').send_keys(data)

    # Operation
    try:
        operation_result = driver.find_element(By.XPATH, '//*[@id="trueResult"]').get_attribute("value")
        driver.find_element(By.XPATH, '//*[@id="operazione"]').send_keys(operation_result)
    except NoSuchElementException:
        print("No operation needed")

    # Second drop-down menu
    driver.find_element(By.XPATH, '//*[@id="data-momento3"]/option[4]').click()

    # tick
    driver.find_element(By.XPATH, '//*[@id="presa-visione-check"]').click()
    driver.find_element(By.XPATH, '//*[@id="no-robot-cb"]').click()

    # Set bot-detector to false before sending the form
    driver.execute_script('document.getElementById("botDetector").value="not-detected"')

    # continue
    driver.find_element(By.XPATH, '//*[@id="avanti-btn"]').click()

    # ticks
    driver.find_element(By.XPATH, '//*[@id="consenso-verifica-cb-fe"]/div/label').click()
    # Set bot-detector to false before sending the form
    driver.execute_script('document.getElementById("botDetector").value="not-detected"')

    driver.find_element(By.XPATH, '//*[@id="invia-btn"]').click()

    # result
    result = driver.find_element(By.XPATH, '/html/body/div/div[2]/p[2]/strong').text
    print("Iteration " + str(iteration) + " - Time employed: " + str(result))
    time.sleep(4)
    # New simulation
    driver.find_element(By.XPATH, '//*[@id="invia-btn"]').click()


iteration_n = 0
while True:
    iteration_n += 1
    routine(iteration_n)
