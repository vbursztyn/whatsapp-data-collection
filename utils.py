from time import sleep
from random import randint

from yaml import load

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait


# random_sleep() -- Sleeps with some added randomness in order to mitigate the chances of being black-listed.
def random_sleep(floor, ceil):
    sleep_time = randint(floor, ceil)
    sleep(sleep_time)


# init_selenium() -- Initializes Selenium, fetches WhatsApp's web client and gives it some time to load.
def init_selenium():
    driver.set_page_load_timeout(config['DRIVER_TIMEOUT'])
    WebDriverWait(driver, config['DRIVER_TIMEOUT'])

    driver.get("https://web.whatsapp.com")
    random_sleep(config['WEB_CLIENT_LOAD_TIME'][0], config['WEB_CLIENT_LOAD_TIME'][1])


config = None

with open('config.yaml', 'r') as config_f:
    config = load(config_f.read())

driver = webdriver.Chrome(config['DRIVER_PATH'])

init_selenium()

