#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Capture les preuves des anomalies dans docs/evidence/."""
from __future__ import annotations

import os
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "automation"))

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from pages.flight_page import FlightPage
from pages.login_page import LoginPage
from pages.navbar import NavBar
from utils.webtours_api import WebToursAPI, tomorrow

BASE_URL = os.getenv("WEBTOURS_URL", "http://127.0.0.1:1080")
EVIDENCE = ROOT / "docs" / "evidence"
EVIDENCE.mkdir(parents=True, exist_ok=True)
USERS_DIR = Path(os.getenv("WEBTOURS_USERS_DIR", r"D:/web tours/WebTours/cgi-bin/users"))


def new_driver():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--window-size=1440,1000")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--log-level=3")
    driver = webdriver.Chrome(options=options)
    driver.set_page_load_timeout(30)
    return driver


def shot(driver, name: str) -> None:
    path = EVIDENCE / name
    driver.save_screenshot(str(path))
    print(f"  -> {path}")


def main() -> None:
    driver = new_driver()
    try:
        # BUG-01 : réservation sans login
        driver.get(f"{BASE_URL}/cgi-bin/reservations.pl?page=welcome")
        time.sleep(1)
        shot(driver, "01_reservations_sans_login.png")

        # BUG-03 : admin sans login
        driver.get(f"{BASE_URL}/cgi-bin/admin.pl")
        time.sleep(1)
        shot(driver, "02_admin_sans_login.png")

        # BUG-04 : IDOR admin
        driver.get(f"{BASE_URL}/WebTours/index.htm")
        driver.add_cookie({"name": "MTUserInfo", "value": "username&admin&hash&78", "path": "/"})
        driver.get(f"{BASE_URL}/cgi-bin/itinerary.pl")
        time.sleep(1)
        shot(driver, "03_idor_admin_itinerary.png")

        # BUG-05 : date invalide
        login = LoginPage(driver, BASE_URL)
        login.open()
        login.login_success("jojo", "bean")
        NavBar(driver, BASE_URL).click_flights()
        flight = FlightPage(driver, BASE_URL)
        flight.search("Denver", "Paris", "13/45/2026", wait_results=False)
        time.sleep(1)
        shot(driver, "05_date_invalide.png")

        # BUG-09 : prix manipulé
        username = "qa" + str(int(time.time()))[-8:]
        api = WebToursAPI(BASE_URL)
        api.signup(username, "Passw0rd!")
        driver.get(f"{BASE_URL}/WebTours/index.htm")
        driver.delete_all_cookies()
        login = LoginPage(driver, BASE_URL)
        login.open()
        login.login_success(username, "Passw0rd!")
        NavBar(driver, BASE_URL).click_flights()
        flight = FlightPage(driver, BASE_URL)
        flight.search("Denver", "Paris", tomorrow(), passengers=1)
        flight.switch_to_info()
        radio = driver.find_element(By.NAME, "outboundFlight")
        original = radio.get_attribute("value")
        number, _, date = original.split(";")
        tampered = f"{number};1;{date}"
        driver.execute_script("arguments[0].value = arguments[1];", radio, tampered)
        driver.find_element(By.NAME, "reserveFlights").click()
        flight.switch_to_info()
        time.sleep(1)
        shot(driver, "04_prix_modifie.png")
        flight.fill_payment_and_buy(passengers=1)
        shot(driver, "04b_facture_prix_modifie.png")
        (USERS_DIR / username).unlink(missing_ok=True)
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
