import bs4
import sys
import time
from playsound import playsound
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager

import config

# Twilio configuration
# toNumber = 'your_phonenumber'
# fromNumber = 'twilio_phonenumber'
# accountSid = 'ssid'
# authToken = 'authtoken'
# client = Client(accountSid, authToken)

# Product Page (By default, This URL will scan all RTX 3080's at one time.)
def timeSleep(x, driver):
    for i in range(x, -1, -1):
        sys.stdout.write('\r')
        sys.stdout.write('{:2d} seconds'.format(i))
        sys.stdout.flush()
        time.sleep(1)
    driver.refresh()
    sys.stdout.write('\r')
    sys.stdout.write('Page refreshed\n')
    sys.stdout.flush()


def createDriver():
    """Creating driver."""
    options = Options()
    options.headless = False  # Change To False if you want to see Firefox Browser Again.
    profile = webdriver.FirefoxProfile(config.profile)
    driver = webdriver.Firefox(profile, options=options, executable_path=GeckoDriverManager().install())
    return driver


def driverWait(driver, findType, selector):
    """Driver Wait Settings."""
    while True:
        if findType == 'css':
            try:
                driver.find_element_by_css_selector(selector).click()
                break
            except NoSuchElementException:
                driver.implicitly_wait(0.2)
        elif findType == 'name':
            try:
                driver.find_element_by_name(selector).click()
                break
            except NoSuchElementException:
                driver.implicitly_wait(0.2)


def findingCards(driver):
    """Scanning all cards."""
    driver.get(config.url)
    while True:
        html = driver.page_source
        soup = bs4.BeautifulSoup(html, 'html.parser')
        wait = WebDriverWait(driver, 15)
        wait2 = WebDriverWait(driver, 2)
        try:
            findAllCards = soup.find('button', {'class': 'btn btn-primary btn-sm btn-block btn-leading-ficon add-to-cart-button'})
            if findAllCards:
                print(f'Button Found!: {findAllCards.get_text()}')

                # Clicking Add to Cart.
                time.sleep(.3)
                driverWait(driver, 'css', '.add-to-cart-button')
                playsound(config.sound)
                time.sleep(2)
                return
            else:
                pass

        except NoSuchElementException:
            pass
        timeSleep(5, driver)


if __name__ == '__main__':
    driver = createDriver()
    findingCards(driver)
