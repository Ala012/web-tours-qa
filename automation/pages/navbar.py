# -*- coding: utf-8 -*-
"""Barre de navigation WebTours (cadre navbar)."""
from __future__ import annotations

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from .base_page import BasePage


class NavBar(BasePage):
    def _click_image(self, alt: str) -> None:
        self.switch_to_navbar()
        self.driver.find_element(By.CSS_SELECTOR, f"img[alt='{alt}']").click()

    def click_flights(self) -> None:
        self._click_image("Search Flights Button")
        self.switch_to_info()
        self.wait.until(EC.presence_of_element_located((By.NAME, "depart")))

    def click_itinerary(self) -> None:
        self._click_image("Itinerary Button")
        self.switch_to_info()
        self.wait.until(lambda d: "Itinerary" in d.find_element(By.TAG_NAME, "body").text)

    def click_home(self) -> None:
        self._click_image("Home Button")
        self.switch_to_info()
        self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    def click_signoff(self) -> None:
        self._click_image("SignOff Button")
        self.switch_to_navbar()
        self.wait.until(EC.presence_of_element_located((By.NAME, "username")))
