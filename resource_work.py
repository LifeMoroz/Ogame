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
    def __init__(self, res):
        self.metal, self.crystal, self.deuterium, self.energy = res.save_resoures()