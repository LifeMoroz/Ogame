# -*- coding:  utf-8 -*-
import datetime
from selenium import webdriver
import time
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from buildings import Building
from selenium.webdriver.support.ui import Select
from planet import PlanetInfo
from resource_work import Resource
import logging

baseURL = "http://ogame.ru"
TIME_TO_REPAID = 90
logging.basicConfig(level=logging.INFO)
driver = None


def what_build_now(has_energy, one_energy_cost=0):
    """
    Calculating based on the speed of payback
    """
    repaid_coef = 1
    what_build = ''
    mines = {}
    for build_t in ['Metal_mine', 'Crystal_mine', 'Deuterium_mine']:
        mines[build_t] = Building(build_t, driver, pl)
        if mines[build_t].need_energy() > has_energy:
            repaid_coef_cur = mines[build_t].repaid_coefficient()
        else:
            repaid_coef_cur = mines[build_t].repaid_coefficient(one_energy_cost *
                                                                (mines[build_t].need_energy() - has_energy))
        if not repaid_coef_cur:
            raise Exception("Smth wrong")
        logging.info(build_t + " w'll produce: " + str(mines[build_t].produce()))
        logging.info(build_t + " w'll cost: " + str(mines[build_t].cost()))
        if repaid_coef <= repaid_coef_cur:
            repaid_coef = repaid_coef_cur
            what_build = build_t

    return mines[what_build]


def build_smth():
    solar_plant_next_lvl = Building('Solar_plant', driver)
    res = Resource(driver)
    building = what_build_now(Resource(driver).energy,
                              solar_plant_next_lvl.cost_in_metal() / solar_plant_next_lvl.produce())
    logging.info("Want to build: " + building.type)
    if not building:
        return 404
    if building.cost()[0] >= res.metal or building.cost()[1] >= res.crystal or building.cost()[2] >= res.deuterium:
        logging.info("Resources: Not enough resources")
        return 1
    logging.info("Resources: OK")
    if building.need_energy() > Resource(driver).energy:
        logging.info("Energy: Not enough energy, now: " + building.need_energy() + ". Try to build solar_plant")
        if solar_plant_next_lvl.cost()[0] >= res.metal or solar_plant_next_lvl.cost()[1] >= res.crystal or \
                        solar_plant_next_lvl.cost()[2] >= res.deuterium:
            logging.info("Resources: Not enough resources")
            return 1
        logging.info("Resources for solar plant: OK")
        solar_plant_next_lvl.build(Resource(driver))
    else:
        logging.info("Energy: OK")
        building.build(Resource(driver))


def connect():
    global driver, baseURL
    driver = webdriver.Firefox()
    driver.get(baseURL)
    logging.info("Log in system")
    driver.find_element_by_id("loginBtn").click()
    select = Select(driver.find_element_by_id("serverLogin"))
    select.select_by_visible_text("Vega")
    driver.find_element_by_id("usernameLogin").send_keys("LifeMoroz")
    driver.find_element_by_id("passwordLogin").send_keys("Olenegorsk8")
    driver.find_element_by_id("loginSubmit").click()
    time.sleep(3)
    logging.info("Log in successful")
    baseURL = driver.current_url.split("=")[0] + "="


connect()
pl = PlanetInfo(driver)
driver.get(baseURL + "resources")
try:
    while 1:
        try:
            time_string = driver.find_element_by_css_selector("#test.time").text
            if time_string == u"готов":
                time.sleep(2)
                continue
            logging.info("Can't build, workers are busy")
            parts = time_string.split(" ")
            seconds = 3
            for part in parts:
                seconds += {
                    u'с': 1,
                    u'м': 60,
                    u'ч': 3600,
                    u'д': 86400
                }[part[-1]] * int(part[:-1])
            logging.info("Going to sleep until the building is finish: " + datetime.timedelta(seconds=seconds))
            time.sleep(seconds)
        except NoSuchElementException:
            if build_smth() == 1:
                time.sleep(60)
                driver.refresh()
            else:
                logging.warning("Time to build smth")
finally:
    driver.quit()
