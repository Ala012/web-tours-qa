# -*- coding: utf-8 -*-
"""Page Itinerary."""
from __future__ import annotations

from selenium.webdriver.common.by import By

from .base_page import BasePage
from .navbar import NavBar


class ItineraryPage(BasePage):
    def open(self) -> "ItineraryPage":
        NavBar(self.driver, self.base_url).click_itinerary()
        self.switch_to_info()
        self.wait.until(lambda d: "Itinerary" in d.find_element(By.TAG_NAME, "body").text)
        return self

    def text(self) -> str:
        return self.info_text()

    def flight_ids(self) -> list[str]:
        self.switch_to_info()
        return [e.get_attribute("value") for e in self.driver.find_elements(By.NAME, "flightID")]

    def flight_count(self) -> int:
        return len(self.flight_ids())

    def is_empty(self) -> bool:
        return "No flights have been reserved" in self.text()

    def remove_first(self) -> None:
        self.switch_to_info()
        self.driver.find_element(By.NAME, "1").click()
        self.driver.find_element(By.NAME, "removeFlights").click()
        self.switch_to_info()
        self.wait.until(lambda d: "Itinerary" in d.find_element(By.TAG_NAME, "body").text)

    def remove_all(self) -> None:
        self.switch_to_info()
        self.driver.find_element(By.NAME, "removeAllFlights").click()
        self.switch_to_info()
        self.wait.until(lambda d: "Itinerary" in d.find_element(By.TAG_NAME, "body").text)
