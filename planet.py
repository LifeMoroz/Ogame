# -*- coding:  utf-8 -*-
__author__ = 'Ruslan'
from selenium.webdriver.support.wait import WebDriverWait


class PlanetInfo:
    def __init__(self, driver):
        url = driver.current_url
        if url != "http://s122-ru.ogame.gameforge.com/game/index.php?page=overview":
            driver.get("http://s122-ru.ogame.gameforge.com/game/index.php?page=overview")
        WebDriverWait(driver, 5, 0.5).until(lambda x: len(x.find_element_by_id("temperatureContentField").text) > 6)
        print driver.find_element_by_id("temperatureContentField").text
        arr = driver.find_element_by_id("temperatureContentField").text.split(" ")  #от 10°C до 50°C
        print arr
        self.avg_t = (int(arr[3].split(u"\xb0")[0]) - int(arr[1].split(u"\xb0")[0])) / 2
        driver.get(url)