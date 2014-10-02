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


def get_time_building(string_to_time=None):
    seconds = 3
    try:
        if not string_to_time:
            time_string = Config.driver.find_element_by_css_selector("#test.time").text
        else:
            time_string = string_to_time
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


# noinspection PyUnresolvedReferences
def defence_circle(**kwargs):
    if Config.driver.current_url == Config.base_url + 'galaxy':
        Config.driver.get(Config.base_url + "resources")
    else:
        Config.driver.refresh()
    fleets = Config.driver.find_elements_by_css_selector('.eventFleet')
    for fleet in fleets:
        try:
            fleet.find_element_by_css_selector('.hostile')
            if not fleet.get_attribute('id').split('-')[1] in defence_circle.missions.keys():
                coords = fleet.find_element_by_css_selectot('.destFleet').text
                arrival_time = fleet.find_element_by_css_selectot('.arrivalTime').text.split(' ')[0].split(':')

                defence_circle.missions[fleet.get_attribute('id').split('-')[1]] = \
                    {
                        'dest': {'galaxy': coords.split[0][2],
                                 'system': coords.split(':')[1],
                                 'position': coords.split(':')[1][:-1]},
                        'arrival_time': {'hour': arrival_time[0],
                                         'minutes': arrival_time[1],
                                         'second': arrival_time[2]}
                    }

        except NoSuchElementException:
            continue
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
            list_activities.append({'time': time.time() + event['function'](**event['kwargs']), 'callback':
                                   {'function': event['function'], 'kwargs': event['kwargs']}})
        else:
            time.sleep(1)


if __name__ == '__main__':
    Config()
    while 1:
        try:
            main_circle()
        except NoSuchElementException:
            if Config.driver.current_url == "http://ru.ogame.gameforge.com/":
                Config.driver.quit()
                Config()
                continue
        finally:
            Config.driver.save_screenshot("./screenshot.jpg")
            Config.driver.quit()