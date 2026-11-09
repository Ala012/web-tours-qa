# -*- coding: utf-8 -*-
"""Pages de recherche, sélection et paiement des vols."""
from __future__ import annotations

import re
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

from .base_page import BasePage


class FlightPage(BasePage):
    # ------------------------------------------------------------- Recherche
    def _set(self, name: str, value: str) -> None:
        element = self.driver.find_element(By.NAME, name)
        element.clear()
        element.send_keys(value)

    def _select_radio(self, name: str, value: str) -> None:
        radio = self.driver.find_element(By.CSS_SELECTOR, f"input[name='{name}'][value='{value}']")
        if not radio.is_selected():
            radio.click()

    def search(
        self,
        depart: str = "Denver",
        arrive: str = "Paris",
        depart_date: str | None = None,
        return_date: str | None = None,
        passengers: int | str = 1,
        roundtrip: bool = False,
        seat_pref: str = "None",
        seat_type: str = "Coach",
        wait_results: bool = True,
    ) -> None:
        from utils.webtours_api import tomorrow

        self.switch_to_info()
        self.wait.until(EC.presence_of_element_located((By.NAME, "depart")))
        Select(self.driver.find_element(By.NAME, "depart")).select_by_visible_text(depart)
        Select(self.driver.find_element(By.NAME, "arrive")).select_by_visible_text(arrive)
        self._set("departDate", depart_date if depart_date is not None else tomorrow())
        self._set("returnDate", return_date if return_date is not None else tomorrow())
        self._set("numPassengers", str(passengers))
        checkbox = self.driver.find_element(By.NAME, "roundtrip")
        if checkbox.is_selected() != roundtrip:
            checkbox.click()
        self._select_radio("seatPref", seat_pref)
        self._select_radio("seatType", seat_type)
        self.driver.find_element(By.NAME, "findFlights").click()
        if wait_results:
            self.switch_to_info()
            self.wait.until(EC.presence_of_element_located((By.NAME, "outboundFlight")))
        else:
            time.sleep(1.0)
            self.switch_to_info()

    def outbound_values(self) -> list[str]:
        self.switch_to_info()
        return [e.get_attribute("value") for e in self.driver.find_elements(By.NAME, "outboundFlight")]

    def return_values(self) -> list[str]:
        self.switch_to_info()
        return [e.get_attribute("value") for e in self.driver.find_elements(By.NAME, "returnFlight")]

    def text(self) -> str:
        return self.info_text()

    # -------------------------------------------------------------- Sélection
    def select_outbound(self, index: int = 0) -> None:
        self.switch_to_info()
        radios = self.driver.find_elements(By.NAME, "outboundFlight")
        if not radios:
            raise AssertionError("Aucun vol à sélectionner")
        radios[index].click()
        self.driver.find_element(By.NAME, "reserveFlights").click()
        self.switch_to_info()
        self.wait.until(EC.presence_of_element_located((By.NAME, "firstName")))

    # --------------------------------------------------------------- Paiement
    def fill_payment_and_buy(
        self,
        passengers: int = 1,
        first_name: str = "QA",
        last_name: str = "User",
        address1: str = "1 Test Street",
        address2: str = "Tunis",
        card: str = "4111111111111111",
        exp_date: str = "12/28",
    ) -> None:
        self.switch_to_info()
        self._set("firstName", first_name)
        self._set("lastName", last_name)
        self._set("address1", address1)
        self._set("address2", address2)
        for index in range(1, passengers + 1):
            name = f"pass{index}"
            value = f"{first_name} {last_name}" if index == 1 else f"Passenger {index}"
            self._set(name, value)
        self._set("creditCard", card)
        self._set("expDate", exp_date)
        self.driver.find_element(By.NAME, "buyFlights").click()
        self.switch_to_info()
        self.wait.until(lambda d: "Invoice" in d.find_element(By.TAG_NAME, "body").text)

    def invoice_text(self) -> str:
        return self.info_text()

    def payment_total(self) -> tuple[int, float] | None:
        text = self.info_text()
        match = re.search(r"Total for (\d+) ticket\(s\) is =\s*\$ ?([\d.]+)", text)
        if not match:
            return None
        return int(match.group(1)), float(match.group(2))
