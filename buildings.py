# -*- coding:  utf-8 -*-
import math
from selenium.webdriver.support.ui import WebDriverWait

TIME_TO_REPAID = 90
ACCELERATION = 2


def FastPow(t, k):
    """ Быстрое возведение числа t в степень k"""
    res = 1
    while k:
        if (k & 1):
            res *= t
        k = k >> 1
        if k == 0:
            break
        t *= t

    return res


class Building:
    TYPES = {
        'Metal_mine': '1',
        'Crystal_mine': '2',
        'Deuterium_mine': '3',
        'Solar_plant': '4',
        'Thermonuclear_plant': '5',
        'Solar_satellite': '6',
        'Metal_storage': '7',
        'Crystal_storage': '8',
        'Deuterium_storage': '9'
    }
    can_build_at = None

    def __init__(self, t, driver, planet_info=None):
        if not Building.TYPES.get(t, None):
            raise ValueError("I don't know this building")

        self.type = t
        self.driver = driver
        if planet_info:
            self.avg_t = planet_info.avg_t

    @property
    def web_obj(self):
        return self.driver.find_element_by_id('button' + Building.TYPES.get(self.type))

    @property
    def level(self):
        return int(self.web_obj.find_element_by_css_selector(".level").text)

    def build(self, res):
        cost = self.cost()
        if cost[0] >= res.metal or cost[1] >= res.crystal or cost[2] >= res.deuterium:
            raise ValueError("No enough resources")
        if self.need_energy() > 0 and self.need_energy() > res.energy:
            raise ValueError("No energy")
        self.web_obj.find_element_by_css_selector(".fastBuild.tooltip").click()
        WebDriverWait(self.driver, 3, 0.5).until(
            lambda x: self.web_obj.find_element_by_id("b_supply" + Building.TYPES.get(self.type)))

    def need_energy(self):
        if self.type in ["Metal_mine", "Crystal_mine"]:
            return math.ceil(10 * (FastPow(1.1, self.level + 1) - FastPow(1.1, self.level)))
        if self.type == "Deuterium_mine":
            return math.ceil(20 * (FastPow(1.1, self.level + 1) - FastPow(1.1, self.level)))
        return 0

    def repaid_coefficient(self, additional_cost=0):
        """
        Mines only
        calculating in metal
        """
        diff_per_hour = math.ceil((self.produce(self.level + 1) - self.produce(self.level)))

        if self.type == "Metal_mine":
            return diff_per_hour * 1.0 * TIME_TO_REPAID * 24 / (self.cost_in_metal() + additional_cost)
        if self.type == "Crystal_mine":
            return diff_per_hour * 1.5 * TIME_TO_REPAID * 24 / (self.cost_in_metal() + additional_cost)
        if self.type == "Deuterium_mine":
            return diff_per_hour * 1.5 * TIME_TO_REPAID * 24 / (self.cost_in_metal() + additional_cost)

    def cost(self, lvl=None):
        if not lvl:
            lvl = self.level  # next level
        else:
            lvl -= 1
        if self.type == "Metal_mine":
            return [math.ceil(60 * FastPow(1.5, lvl)), math.ceil(15 * FastPow(1.5, lvl)), 0]
        if self.type == "Crystal_mine":
            return [math.ceil(48 * FastPow(1.6, lvl)), math.ceil(24 * FastPow(1.6, lvl)), 0]
        if self.type == "Deuterium_mine":
            return [math.ceil(225 * FastPow(1.5, lvl)), math.ceil(75 * FastPow(1.5, lvl)), 0]
        if self.type == "Solar_plant":
            return [math.ceil(75 * FastPow(1.5, lvl)), math.ceil(30 * FastPow(1.5, lvl)), 0]

    def cost_in_metal(self, arr=None):
        if arr is None:
            arr = self.cost()
        return arr[0] + arr[1] * 1.5 + arr[2] * 2.5

    def produce(self, lvl=None):
        if not lvl:
            lvl = self.level  # for next level
        else:
            lvl -= 1
        if self.type == "Metal_mine":
            return math.ceil(ACCELERATION * 30 * lvl * FastPow(1.1, lvl))  # metal
        if self.type == "Crystal_mine":
            return math.ceil(ACCELERATION * 20 * lvl * FastPow(1.1, lvl))  # crystal
        if self.type == "Deuterium_mine":
            return math.ceil(ACCELERATION * 10 * lvl * FastPow(1.1, lvl) * (-0.002 * self.avg_t + 1.28))  # deuterium
        if self.type == "Solar_plant":
            return math.ceil(20 * lvl * FastPow(1.1, lvl))  # energy
