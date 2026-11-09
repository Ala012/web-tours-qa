# -*- coding: utf-8 -*-
"""Classe de base pour la navigation dans les frames de WebTours."""
from __future__ import annotations

import time

from selenium.common.exceptions import (
    NoSuchFrameException,
    StaleElementReferenceException,
    TimeoutException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


class BasePage:
    def __init__(self, driver, base_url: str = "http://127.0.0.1:1080", timeout: int = 15):
        self.driver = driver
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.wait = WebDriverWait(driver, timeout)

    # ------------------------------------------------------------- Frames
    def _find_frame(self, name: str, timeout: int = 10):
        end = time.time() + timeout
        last_error = None
        while time.time() < end:
            try:
                for frame in self.driver.find_elements(By.TAG_NAME, "frame"):
                    if frame.get_attribute("name") == name:
                        return frame
            except (StaleElementReferenceException, NoSuchFrameException) as exc:
                last_error = exc
            time.sleep(0.2)
        raise TimeoutException(f"Frame {name!r} introuvable") from last_error

    def _switch_in_current(self, name: str) -> None:
        frame = self._find_frame(name)
        try:
            self.driver.switch_to.frame(frame)
        except StaleElementReferenceException:
            frame = self._find_frame(name)
            self.driver.switch_to.frame(frame)

    def switch_to_body(self) -> None:
        self.driver.switch_to.default_content()
        self._switch_in_current("body")

    def switch_to_navbar(self) -> None:
        for _ in range(3):
            try:
                self.switch_to_body()
                self._switch_in_current("navbar")
                return
            except TimeoutException:
                time.sleep(0.5)
        raise TimeoutException("Frame 'navbar' introuvable")

    def switch_to_info(self) -> None:
        for _ in range(3):
            try:
                self.switch_to_body()
                self._switch_in_current("info")
                return
            except TimeoutException:
                time.sleep(0.5)
        raise TimeoutException("Frame 'info' introuvable")

    def switch_to_default(self) -> None:
        self.driver.switch_to.default_content()

    # -------------------------------------------------------------- Texte
    def info_text(self) -> str:
        self.switch_to_info()
        return self.driver.find_element(By.TAG_NAME, "body").text

    def wait_info_contains(self, text: str, timeout: int | None = None) -> bool:
        self.switch_to_info()
        WebDriverWait(self.driver, timeout or self.timeout).until(
            lambda d: text in d.find_element(By.TAG_NAME, "body").text
        )
        return True
