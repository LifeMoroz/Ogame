import logging
from selenium import webdriver
from selenium.webdriver.support.select import Select
import time

__author__ = 'Ruslan'


class Config:
    """
    log_lvl = {
        CRITICAL = 50
        FATAL = CRITICAL
        ERROR = 40
        WARNING = 30
        WARN = WARNING
        INFO = 20
        DEBUG = 10
        NOTSET = 0
    }
    """
    base_url = "http://ogame.ru"
    time_to_repaid = 90
    log_lvl = 20  # INFO
    driver = None

    def __init__(self):
        logging.basicConfig(level=Config.log_lvl)
        Config.driver = webdriver.Firefox()
        Config.driver.get(Config.base_url)
        logging.info("Log in system")
        Config.driver.find_element_by_id("loginBtn").click()
        select = Select(Config.driver.find_element_by_id("serverLogin"))
        select.select_by_visible_text("Vega")
        Config.driver.find_element_by_id("usernameLogin").send_keys("LifeMoroz")
        Config.driver.find_element_by_id("passwordLogin").send_keys("Olenegorsk8")
        Config.driver.find_element_by_id("loginSubmit").click()
        time.sleep(3)
        logging.info("Log in successful")
        Config.base_url = Config.driver.current_url.split("=")[0] + "="
