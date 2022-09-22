from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
import json
import time
import random

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


def routine(iteration=-1):
    ################
    # LOADING PAGE #
    ################
    
    while driver.find_element(By.XPATH, '//*[@id="invia-btn"]').is_displayed():                 # Till the button "reload" is present: reload
        driver.find_element(By.XPATH, '//*[@id="invia-btn"]').click() 
    
    
    #############
    # MAIN PAGE #
    #############
    timeout = random.randint(5, 25)                                                             # Timeout to pretend to have human-like results
    time.sleep(timeout)

    select = Select(driver.find_element(By.XPATH, '//*[@id="giorno-odierno"]'))                 # 1sr drop-down menu: DAY
    select.select_by_value('dright')

    select = Select(driver.find_element(By.XPATH, '//*[@id="mese-odierno"]'))                   # 2nd drop-down menu: MONTH
    select.select_by_value('mright')
    
    select = Select(driver.find_element(By.XPATH, '//*[@id="anno-odierno"]'))                   # 3rd drop-down menu: YEAR
    select.select_by_value('yright')
    
    select = Select(driver.find_element(By.XPATH, '//*[@id="data-momento5"]'))                  # 4th drop-down menu: MOMENTO 5
    select.select_by_value('12/12/2022')
    
    select = Select(driver.find_element(By.XPATH, '//*[@id="nome-utente"]'))                    # 5th drop-down menu: PARTECIPANTE
    select.select_by_value('MarioRossi')
    
    select = Select(driver.find_element(By.XPATH, '//*[@id="caratteri-bando"]'))                # 6th drop-down menu: BNDS
    option = select.options
    for index in range(1, len(option)):
        if option[index].get_attribute("value") != "wrong":
            select.select_by_index(index)
            break

    select = Select(driver.find_element(By.XPATH, '//*[@id="caratteri-token"]'))                # 7th drop-down menu: CHECK
    select.select_by_value('rightToken')

    driver.find_element(By.XPATH, '//*[@id="presa-visione-check"]').click()                     # 1st tick
    driver.find_element(By.XPATH, '//*[@id="no-robot-cb"]').click()                             # 2nd tick

    driver.execute_script('document.getElementById("botDetector").value="not-detected"')        # Set bot-detector to false before sending the form

    driver.find_element(By.XPATH, '//*[@id="avanti-btn"]').click()                              # continue

    
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
    print("Iteration " + str(iteration) + " - Time employed: " + str(result) + " - employing a timeout of seconds: " + str(timeout))
    time.sleep(3)
    
    driver.find_element(By.XPATH, '//*[@id="invia-btn"]').click()                               # New simulation


iteration_n = 0
while True:
    iteration_n += 1
    
    try:
        routine(iteration_n)
    except:
        print("Error in the page. Probably you found a not considered case... Will try again with another simulation!")
        iteration_n -= 1
        driver.find_element(By.XPATH, '//*[@id="logout-btn"]').click()
        driver.get(secret_data['simulator_page'])
        
