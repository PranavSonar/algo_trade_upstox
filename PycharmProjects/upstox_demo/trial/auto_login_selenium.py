import time
import urlparse
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

def login_to_upstox(url):
    driver = webdriver.Chrome()
    driver.get(url)
    assert "Upstox Login" in driver.title
    name = driver.find_element_by_id("name")
    name.clear()
    name.send_keys("100781")

    time.sleep(0.2)

    passwordField = driver.find_element_by_id("password")
    passwordField.clear()
    passwordField.send_keys("feb@12")

    time.sleep(0.2)

    twoFA = driver.find_element_by_id("password2fa")
    twoFA.clear()
    twoFA.send_keys("1989")
    twoFA.send_keys(Keys.RETURN)

    WebDriverWait(driver, 10).until(
        expected_conditions.visibility_of(driver.find_element_by_id("allow"))
    )

    driver.find_element_by_id("allow").submit()

    parsed = urlparse.urlparse(driver.current_url)
    print urlparse.parse_qs(parsed.query)['code']
    driver.close()
    return urlparse.parse_qs(parsed.query)['code']

    # assert "No results found." not in driver.page_source
