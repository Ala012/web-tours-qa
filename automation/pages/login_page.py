# -*- coding: utf-8 -*-
"""Page de connexion / inscription."""
from __future__ import annotations

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from .base_page import BasePage


class LoginPage(BasePage):
    USERNAME = (By.NAME, "username")
    PASSWORD = (By.NAME, "password")
    LOGIN_BUTTON = (By.NAME, "login")
    PASSWORD_CONFIRM = (By.NAME, "passwordConfirm")
    REGISTER_BUTTON = (By.NAME, "register")

    def open(self) -> "LoginPage":
        self.driver.get(self.base_url + "/WebTours/index.htm")
        self.switch_to_body()
        self.switch_to_navbar()
        self.wait.until(EC.presence_of_element_located(self.USERNAME))
        return self

    def login(self, username: str, password: str) -> None:
        self.switch_to_navbar()
        field = self.driver.find_element(*self.USERNAME)
        field.clear()
        field.send_keys(username)
        pwd = self.driver.find_element(*self.PASSWORD)
        pwd.clear()
        pwd.send_keys(password)
        self.driver.find_element(*self.LOGIN_BUTTON).click()

    def wait_logged_in(self) -> bool:
        return self.wait_info_contains("Welcome,")

    def login_success(self, username: str = "jojo", password: str = "bean") -> "LoginPage":
        self.login(username, password)
        self.wait_logged_in()
        return self

    def get_info_text(self) -> str:
        return self.info_text()

    def is_login_form_displayed(self) -> bool:
        try:
            self.switch_to_navbar()
            return self.driver.find_element(*self.USERNAME).is_displayed()
        except Exception:
            return False

    def logout(self) -> None:
        self.switch_to_navbar()
        self.driver.find_element(By.CSS_SELECTOR, "img[alt='SignOff Button']").click()
        self.switch_to_navbar()
        self.wait.until(EC.presence_of_element_located(self.USERNAME))

    # ----------------------------------------------------------- Inscription
    def open_signup(self) -> None:
        self.switch_to_info()
        self.driver.find_element(By.LINK_TEXT, "sign up now").click()
        self.switch_to_info()
        self.wait.until(EC.presence_of_element_located(self.PASSWORD_CONFIRM))

    def _fill(self, name: str, value: str) -> None:
        element = self.driver.find_element(By.NAME, name)
        element.clear()
        element.send_keys(value)

    def register(
        self,
        username: str,
        password: str,
        confirm: str,
        first_name: str = "QA",
        last_name: str = "User",
        address1: str = "1 Test Street",
        address2: str = "Tunis",
    ) -> None:
        self.switch_to_info()
        self._fill("username", username)
        self._fill("password", password)
        self._fill("passwordConfirm", confirm)
        self._fill("firstName", first_name)
        self._fill("lastName", last_name)
        self._fill("address1", address1)
        self._fill("address2", address2)
        self.driver.find_element(*self.REGISTER_BUTTON).click()

    def registration_message(self) -> str:
        return self.info_text()
