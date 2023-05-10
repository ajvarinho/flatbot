import requests
import time
from random import randint
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait            
from selenium.webdriver.support import expected_conditions as EC

import smtplib
from email.message import EmailMessage
import stash
from selenium.webdriver.common.action_chains import ActionChains


url = 'https://www.wbm.de/wohnungen-berlin/angebote/'
request_time = randint(190, 340)

gmail_password = stash.googlePw
email_address = stash.emailAddress
input_address = stash.adresa
input_phone = stash.telefon
input_name = stash.prezime

def send_email_gmail(subject, message, destination):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login('hbtuju@gmail.com', gmail_password)

    msg = EmailMessage()

    message = f'{message}\n'
    msg.set_content(message)
    msg['Subject'] = subject
    msg['From'] = 'hbtuju@gmail.com'
    msg['To'] = destination
    server.send_message(msg)

def main():

    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(5)
    #to accept cookies
    #button = driver.find_element(By.CLASS_NAME, "cookie-settings-submitall")
    #button.click()
    time.sleep(2)
    
    try:
        #
        listing = driver.find_element(By.CLASS_NAME, "immo-element")
        if listing.is_displayed():
            time.sleep(2)
            description = driver.find_element(By.CLASS_NAME, "textWrap")
            findArea = driver.find_element(By.CLASS_NAME, 'area')
            whereIs = findArea.text
            lowercase = whereIs.lower()
            numberOfRooms = driver.find_element(By.CLASS_NAME, 'main-property-rooms')
            roomNum = numberOfRooms.text
            if roomNum == '3':  
                time.sleep(2)
                print('helou')
                hrefLink = 'www.wbm.de/wohnungen-berlin/angebote/details/3-zimmer-wohnung-in-' + lowercase
                anchorEl = driver.find_element(By.LINK_TEXT, 'ANSEHEN')
                anchorEl.click()
                time.sleep(3)
                # FORM HANDLING
                WebDriverWait(driver, 5).until(EC.element_to_be_clickable(((By.ID, 'powermail_field_name')))).send_keys(input_name)
                name = driver.find_element(By.ID, 'powermail_field_name')
                vorname = driver.find_element(By.ID, 'powermail_field_vorname').send_keys("Maja")
                strasse = driver.find_element(By.ID, 'powermail_field_strasse').send_keys(input_address)
                time.sleep(2)
                ort = driver.find_element(By.ID, 'powermail_field_ort').send_keys("Berlin")
                PLZ = driver.find_element(By.ID, 'powermail_field_plz').send_keys("10 243")
                email = driver.find_element(By.ID, 'powermail_field_e_mail').send_keys(email_address)
                telefon = driver.find_element(By.ID, 'powermail_field_telefon').send_keys(input_phone)
                time.sleep(2)
                datenschutz = driver.find_element(By.ID, 'powermail_field_datenschutzhinweis_1').send_keys(Keys.SPACE)
                time.sleep(2)
                absenden = driver.find_element(By.XPATH, '//button[text()="Anfrage absenden"]')
                absenden.click()
                time.sleep(2)
                currentUrl = driver.current_url
                send_email_gmail('Prijava', currentUrl, email_address)
                time.sleep(5)
                driver.quit()
    #      
    except NoSuchElementException:
        time.sleep(5)
        print('ma bjaaazi')
        driver.quit()

    time.sleep(request_time)

i = 0
while i < 250:
    i+=1
    print(i)
    main()

if __name__ == "__main__":
    main()