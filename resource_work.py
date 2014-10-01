import string


class Resource:
    """
    This return curent resource status
    """
    def __init__(self, driver):
        self.driver = driver

    @property
    def metal(self):
        return int(string.join(self.driver.find_element_by_id("resources_metal").text.split("."), ""))

    @property
    def crystal(self):
        return int(string.join(self.driver.find_element_by_id("resources_crystal").text.split("."), ""))

    @property
    def deuterium(self):
        return int(string.join(self.driver.find_element_by_id("resources_deuterium").text.split("."), ""))

    @property
    def energy(self):
        return int(string.join(self.driver.find_element_by_id("resources_energy").text.split("."), ""))

    def save_resources(self):
        return self.metal, self.crystal, self.deuterium, self.energy


class SavedResources:
    def __init__(self, res=None, metal=None, crystal=None, deuterium=None, energy=None):
        if res:
            self.metal, self.crystal, self.deuterium, self.energy = res.save_resoures()
        else:
            if metal is None or crystal is None or deuterium is None or energy is None:
                raise Exception("Can't save anyth")
            self.metal = metal
            self.crystal = crystal
            self.deuterium = deuterium
            self.energy = energy