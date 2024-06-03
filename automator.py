from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from datetime import date, timedelta
import json
import time
import random
import re

f = open("secret.json")
secret_data = json.load(f)

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(options=options)

#########
# LOGIN #
#########
driver.get(secret_data['login_page'])
driver.find_element(By.ID, 'insert_login').send_keys(secret_data['user'])
driver.find_element(By.ID, 'insert_pwd').send_keys(secret_data['psw'])
driver.find_element(By.XPATH, '/html/body/div/div/form/div[3]/input').click()
driver.get(secret_data['simulator_page'])

versione_bando = -1

def routine(iteration=-1):
    ################
    # LOADING PAGE #
    ################
    
    while driver.find_element(By.XPATH, '//*[@id="invia-btn"]').is_displayed():                 # Till the button "reload" is present: reload
        driver.find_element(By.XPATH, '//*[@id="invia-btn"]').click()
        time.sleep(1)
    
    
    #############
    # MAIN PAGE #
    #############

    versione_bando = 0
    attempt_again = False
    try:
        versione_bando = 1
        select = Select(driver.find_element(By.XPATH, '//*[@id="tipo-bando"]'))                     # 1sr drop-down menu: BANDO
        select.select_by_value('ISI2023')
    except NoSuchElementException:
        attempt_again = True
    
    if attempt_again:
        attempt_again = False
        versione_bando = 2
        try:
            driver.find_element(By.XPATH, '//*[@value="2023"]').click()
            driver.find_element(By.XPATH, '//*[@value="-"]').click()
            select = Select(driver.find_element(By.XPATH, '//*[@id="caratteri-token"]'))
            select.select_by_value("rightToken")
            select = Select(driver.find_element(By.XPATH, '//*[@id="nome-inail"]'))
            select.select_by_value("INAIL")
            driver.find_element(By.CSS_SELECTOR, '#label-3-4').click()
            select = Select(driver.find_element(By.XPATH, '//*[@id="minuti-momento"]'))
            select.select_by_value("20")
            driver.find_element(By.XPATH, '//*[@value="right"]').click()
        except NoSuchElementException:
            attempt_again = True

    if attempt_again:
        attempt_again = False
        versione_bando = 3
        try:
            driver.find_element(By.XPATH, '//*[@value="prova@esempio.com"]').click()
        except NoSuchElementException:        
            print("Bando NON versione 3")
        try:
            driver.find_element(By.XPATH, '//*[@value="fbbr"]').click()
        except:
            pass
        try:
            driver.find_element(By.XPATH, '//*[@value="23"]').click()
        except:
            try:
                driver.find_element(By.XPATH, '//*[@value="20"]').click()
            except:
                pass
        try:
            driver.find_element(By.XPATH, '//*[@value="ISI2022"]').click()
        except:
            pass
        try:
            driver.find_element(By.XPATH, '//*[@value="12/09/2023"]').click()
        except:
            pass
        try:
            driver.find_element(By.XPATH, '//*[@id="data-momento1"]').find_element(By.XPATH, '//*[@value="12/09/2023"]').click()
        except:
            pass
        

    
    try:
        # ID code
        text_id_req = driver.find_element(By.XPATH, '//*[@id="input-token-fe"]/label').text               # 2nd box: codice identificativo
        code = driver.find_element(By.XPATH, '//*[@id="my-token-value"]/strong').text

        n = 11
        if re.search("due", text_id_req):
            n = 2
        elif re.search("tre", text_id_req):
            n = 3
        elif re.search("quattro", text_id_req):
            n = 4
        elif re.search("cinque", text_id_req):
            n = 5
        elif re.search("sei", text_id_req):
            n = 6
        elif re.search("sette", text_id_req):
            n = 7
        elif re.search("otto", text_id_req):
            n = 8
        elif re.search("nove", text_id_req):
            n = 9
        elif re.search("dieci", text_id_req):
            n = 10
        if re.search("^\* Inserire .* ultim", text_id_req):
            # END REGEX
            regex = r"([\w]{})$".format('{' + str(n) + '}')
        else:
            # START REGEX
            regex = r"^\+([\w]{" + str(n) + "})"

        if re.search(".* lettere del codice identificativo assegnato:$", text_id_req):
            code = re.sub(r'[0-9]+', '', code)
        elif re.search(".* numeri del codice identificativo assegnato:$", text_id_req):
            code = re.sub(r'[a-z]+', '', code)

        trial = re.search(regex, code)
        while not trial:
            trial = re.search(regex, code)
            print("WTF!")
        try:
            requested_code = re.search(regex, code).group(1)
        except AttributeError:
            print("Oh noo...")
            print(text_id_req)
            print(code)
            print(regex)
            requested_code = re.match(regex, code)
            print(requested_code)
        driver.find_element(By.XPATH, '/html/body/div[2]/div[3]/form/fieldset/div[3]/input').send_keys(requested_code)
    except:
        pass

    try:
        # Data
        data_question = driver.find_element(By.XPATH, '//*[@id="data-odierna-fe"]/label').text
        if re.search("^\* Data di domani \[GG/MM/AAAA]", data_question):
            day = date.today() + timedelta(days=1)                                                   # 3th box: data di domani
        elif re.search("^\* Data odierna \[GG/MM/AAAA]", data_question):
            day = date.today()                                                                       # 3th box: data di ogg
        else:
            day = date.today() - timedelta(days=1)                                                   # 3th box: data di ieri
        driver.find_element(By.XPATH, '//*[@id="data-odierna"]').send_keys(day.strftime("%d/%m/%Y")) # data
    except:
        pass
    
    #numero tra parentesi
    try:
        hidden = driver.find_element(By.CSS_SELECTOR, '#trueResult')                          # 4th box: operazione
        driver.find_element(By.XPATH, '//*[@id="operazione"]').send_keys(hidden.get_property("value"))
    except NoSuchElementException:
        versione_bando = str(versione_bando) + "b"
    
    
    try:
        select = Select(driver.find_element(By.XPATH, '//*[@id="data-momento3"]'))                  # 5th drop-down menu: MOMENTO 3
        select.select_by_value('27/05/2024')
    except:
        pass


    driver.execute_script('document.getElementById("botDetector").value="not-detected"')                # Set bot-detector to false before sending the form

    driver.find_element(By.XPATH, '//*[@id="presa-visione-check"]').click()                             # presa visione regole tecniche check
    driver.find_element(By.XPATH, '//*[@id="no-robot-cb"]').click()                                     # non sono un robot check
    driver.find_element(By.XPATH, '//*[@id="avanti-btn"]').click()                                      # bottone Avanti

    timeout = random.randint(5, 20)                                                                     # Timeout to pretend to have human-like results
    time.sleep(timeout)


    
    #####################
    # CONFIRMATION PAGE #
    #####################
    driver.find_element(By.XPATH, '//*[@id="consenso-verifica-cb-fe"]/div/label').click()       # ticks
    driver.execute_script('document.getElementById("botDetector").value="not-detected"')        # Set bot-detector to false before sending the form

    driver.find_element(By.XPATH, '//*[@id="invia-btn"]').click()

    
    ###############
    # RESULT PAGE #
    ###############
    result = driver.find_element(By.XPATH, '/html/body/div/div[2]/p[2]/strong').text            # result
    print("Iteration " + str(iteration) + " - Time employed: " + str(result) + " - employing a timeout of seconds: " + str(timeout) + " Versione bando: " + str(versione_bando))
    time.sleep(3)
    
    driver.find_element(By.XPATH, '//*[@id="invia-btn"]').click()                               # New simulation


iteration_n = 0
while True:
    iteration_n += 1
    
    try:
        routine(iteration_n)
    except:
        time.sleep(2)
        print("Error in the page. Probably you found a not considered case... Will try again with another simulation! Versione bando:", versione_bando)
        time.sleep(10)
        iteration_n -= 1
        driver.find_element(By.XPATH, '//*[@id="logout-btn"]').click()
        driver.get(secret_data['simulator_page'])
        
