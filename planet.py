# -*- coding:  utf-8 -*-
from selenium.common.exceptions import TimeoutException
import time
from config import Config

__author__ = 'Ruslan'
from selenium.webdriver.support.wait import WebDriverWait


class Empire:
    def __init__(self):
        self.planets = {}
        ids = []
        for planet in Config.driver.find_elements_by_css_selector('.smallplanet'):
            ids.append(planet.get_attribute('id').split('-')[1])
        for planet_id in ids:
            if not Config.driver.find_elements_by_css_selector('#planet-' + planet_id + '> .active'):
                Config.driver.find_element_by_id('planet-' + planet_id).click()
            self.planets[planet_id] = PlanetInfo(Config.driver)
            time.sleep(1)


class PlanetInfo:
    def __init__(self, driver):
        if not "http://s122-ru.ogame.gameforge.com/game/index.php?page=overview" in driver.current_url :
            driver.get("http://s122-ru.ogame.gameforge.com/game/index.php?page=overview")
        count = 0
        while count < 3:
            try:
                WebDriverWait(driver, 5, 0.5).until(
                    lambda x: len(x.find_element_by_id("honorContentField").text) > 0)
                break
            except TimeoutException:
                driver.save_screenshot("./screen.jpg")
                count += 1
                driver.refresh()
                continue
        arr = driver.find_element_by_id("temperatureContentField").text.split(" ")
        print arr
        self.avg_t = (int(arr[3].split(u"\xb0")[0]) - int(arr[1].split(u"\xb0")[0])) / 2
        coords = driver.find_element_by_id('positionContentField').text
        self.coords = {'galaxy': coords.split[0][2],
                       'system': coords.split(':')[1],
                       'position': coords.split(':')[1][:-1]}