import logging
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from config import Config
from exc import FleetException
__author__ = 'Ruslan'


class FleetControl:
    def __init__(self):
        self.missions = {}
        pass

    def _attack(self, driver, fleet):
        if driver.current_url != Config.base_url + "fleet1":
            driver.get(Config.base_url + "fleet1")

    def new_mission(self):
        pass


class Mission:
    TYPE = {
        'Expedition': '15',
        'Colonization': '7',
        'Harvesting': '8',
        'Transport': '3',
        'Deployment': '4',
        'Espionage': '6',
        'Defence': '5',
        'Attacking': '1',
        'ACS Attack': '2',
        'Destroy': '9'
    }

    def __init__(self, driver, mission, fleet, target, speed=100, res=None):
        """

        :param driver: WebDriver
        :param mission: string
        :param fleet: dict
        :param target: dict {'galaxy': 1, system '001', position '001')
        :param speed: 10, 20, ..., 100
        """

        if speed > 100:
            raise ValueError('More than speed of light?')
        self.mission = Mission.TYPE[mission]
        self.fleet = Fleet(driver, fleet)
        self.target = target
        for k, v in target:
            driver.find_element_by_id(k).send_keys(v)
        driver.find_element_by_id('continue').click()
        if driver.current_url == Config.base_url + "fleet2":
            if __debug__:
                raise FleetException("Uninhabited planet")
        else:
            if driver.find_element_by_id('button' + mission).get_attribute("class") == 'off':
                if __debug__:
                    raise FleetException("Unavailable mission type")
            else:
                driver.find_element_by_id('button' + mission).click()
                for k, v in res:
                    if k != 'energy':
                        driver.find_element_by_id(k).send_keys(v)
                driver.find_element_by_id('start').click()
                WebDriverWait(driver, 5, 0.5).until(
                    lambda x: x.find_elements_by_css_selector(".fleetDetails").is_displayed(), "Can't send fleet")
                self.id = driver.find_element_by_css_selector('.timer.tooltip').get_attribute('id').split('_')[1]

    def stop_mission(self, driver):
        if driver.current_url == Config.base_url + "movement":
            driver.get(Config.base_url + "movement")
        try:
            driver.find_element_by_css_selector('#fleet' + self.id + ' > .reversal').click()
        except NoSuchElementException:
            raise FleetException("Fleet already returns")


class Fleet:
    TYPES = {
        # military ships
            'Light Fighter': "204",
            'Heavy Fighter': "205",
            'Cruiser': '206',
            'Battleship': '207',
            'Destroyer': '211',
            'Bomber': '213',
            'Deathstar': '214',
            'Battlecruiser': '215',
        # civil ships
            'Small Cargo Ship': '202',
            'Large Cargo Ship': '203',
            'Colony Ship': '208',
            'Recycler': '209',
            'Espionage Probe': '210',
    }

    @staticmethod
    def _add_ships(driver, fleet):
        if fleet == 'all':
            driver.find_element_by_css_selector('#sendall').click()
        else:
            for t, num in fleet:
                send = driver.find_element_by_css_selector("#button" + Fleet.TYPES[t] + " > input")
                if send.get_attribute('disabled'):
                    if __debug__:
                        raise FleetException('No such type of ships on planet')
                else:
                    send.send_keys(num)

        driver.find_element_by_id('continue').click()
        return 0

    def __init__(self, driver, fleet):
        if self._add_ships(driver, fleet) != 0:
            if __debug__:
                raise FleetException("Smth wrong")
            else:
                logging.exception("Incorrect result")
        else:
            self.fleet = fleet

    @staticmethod
    def build_ships(driver, fleet):
        if driver.current_url != Config.base_url + 'shipyard':
            driver.get(Config.base_url + 'shipyard')
        else:
            driver.refresh()

        for t, num in fleet:
            driver.find_element_by_css_selector("#details" + Fleet.TYPES[t]).click()
            WebDriverWait(driver, 5, 0.5).until(lambda x: x.find_elements_by_id('shipyard_' + Fleet.TYPES[t]
                                                                                + '_large').is_displayed())
            driver.find_element_by_id('number').send_keys(num)