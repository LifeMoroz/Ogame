# -*- coding:  utf-8 -*-
import datetime
import time
import logging
from selenium.common.exceptions import NoSuchElementException
from buildings import Building
from config import Config
from fleet_control import Mission
from planet import PlanetInfo, Empire
from resource_work import Resource
from timer import Timer


def get_time_building():
    seconds = 3
    try:
        time_string = Config.driver.find_element_by_css_selector("#test.time").text
        if time_string == u"готов":
            return seconds
        logging.info("Can't build, workers are busy")
        parts = time_string.split(" ")
        for part in parts:
            seconds += {
                u'с': 1,
                u'м': 60,
                u'ч': 3600,
                u'д': 86400
            }[part[-1]] * int(part[:-1])
        return seconds
    except NoSuchElementException:
        return 0


def building_circle(**kwargs):
    Config.driver.find_element_by_id('planet-' + kwargs['planet_id']).click()
    if Config.driver.current_url != Config.base_url + 'resources':
        Config.driver.get(Config.base_url + 'resources')
    seconds = get_time_building()
    if seconds != 0:
        return seconds
    if Building.build_smth(Config.driver, kwargs['planet_info']) != 0:
        return 60  # Wait until has resources
    else:
        logging.warning("Time to build smth")


def defence_circle(**kwargs):
    if Config.driver.current_url == Config.base_url + 'galaxy':
        Config.driver.get(Config.base_url + "resources")
    else:
        Config.driver.refresh()
    if defence_circle.mission:
        logging.warning('attack!')
    if not 'noAttack' in Config.driver.find_element_by_id('attack_alert').get_attribute('class'):
        defence_circle.mission = {0: Mission(Config.driver, fleet='all',
                                             target={'galaxy': 1, 'system': 134, 'position': 10}, speed=10,
                                             mission='Transport', res=Resource(Config.driver))}

    else:
        return 60 * 30


def main_circle():
    defence_circle.mission = {}
    list_activities = []
    empire = Empire()
    for planet_id, planet_info in empire.planets.items():
        list_activities.append({'time': 0, 'callback': {'function': building_circle,
                                                        'kwargs': {'planet_id': planet_id,
                                                                   'planet_info': planet_info}}})
    timer = Timer(list_activities)
    timer.start()
    while 1:
        if timer.activated_events.qsize() > 0:
            event = timer.activated_events.get(timeout=1)
            list_activities.append({'time': time.time() + event['function'](event['kwargs']), 'callback':
                                   {'function': event['function'], 'args': event['kwargs']}})
        else:
            time.sleep(1)


if __name__ == '__main__':
    while 1:
        try:
            Config()
            main_circle()
        except NoSuchElementException:
            if Config.driver.current_url == "http://ru.ogame.gameforge.com/":
                Config.driver.quit()
                continue
        finally:
            Config.driver.save_screenshot("./screenshot.jpg")
            Config.driver.quit()