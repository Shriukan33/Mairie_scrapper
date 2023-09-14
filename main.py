from os import environ
import smtplib
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import requests

from dotenv import load_dotenv
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager

load_dotenv()

def send_mail():
    mail_content="Date dispo"
    sender = environ("sender")
    sender_pass = environ("sender_pass")
    receiver = environ("receiver")
    message = MIMEMultipart()
    message["From"] = sender
    message["To"] = receiver
    message["Subject"] = "Date dispo Mairie Cauderan"
    message.attach(MIMEText(mail_content, "plain"))
    session = smtplib.SMTP("smtp.gmail.com", 587)
    session.starttls()
    session.login(sender, sender_pass)
    text = message.as_string()
    session.sendmail(sender, receiver, text)
    session.quit()
    print("mail sent!")

# Monitoring cronjob
requests.get('https://cronitor.link/p/fcab34203ba44d21b999298852e708bc/ipuI4E')

url_mairie = "https://rdv-accueil.bordeaux.fr/"

# initialisation Selenium
options = Options()
# options.add_argument("--headless")
options.add_argument("--disable-extensions")
service = Service(ChromeDriverManager().install())
browser= WebDriver(service=service,
                   options=options)
browser.implicitly_wait(5)

# Browsing
found = False
browser.get(url_mairie)
browser.find_element("xpath", '//*[@id="nextButtonId"]').click()
Select(
    browser.find_element(
        "xpath",
        # Quantité "Rendez-vous Carte Nationale d'Identité (CNI)"
        '/html/body/div[4]/div/div/div/main/div/div[3]/div/div/form/div/div[2]/div/div[1]/div[3]/div[3]/select')
    ).select_by_visible_text('1')

browser.find_element("xpath", '//*[@id="nextButtonId"]').click()
Select(browser.find_element("xpath", '//select[@id="ISiteBeanKeySelect"]')).select_by_visible_text('MAIRIE DE CAUDERAN')
try:
    found = EC.presence_of_all_elements_located(browser.find_element(By.CSS_SELECTOR, 'a.ui-state-default'))
except NoSuchElementException:
    browser.find_element(By.CLASS_NAME,'ui-icon-circle-triangle-e').click()
    time.sleep(1)
    try:
        found = EC.presence_of_all_elements_located(browser.find_element(By.CSS_SELECTOR, 'a.ui-state-default'))
    except NoSuchElementException:
        print("No date found")

if found:
    print("Date found")
    found = True
    send_mail()

browser.quit()
