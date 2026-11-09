# -*- coding: utf-8 -*-
"""Fixtures pytest communes à la suite WebTours."""
from __future__ import annotations

import os
import uuid
from pathlib import Path

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from pages.login_page import LoginPage
from utils.webtours_api import WebToursAPI

BASE_URL = os.getenv("WEBTOURS_URL", "http://127.0.0.1:1080")
USERS_DIR = Path(os.getenv("WEBTOURS_USERS_DIR", r"D:/web tours/WebTours/cgi-bin/users"))
PASSWORD = "Passw0rd!"


def _unique(prefix: str = "qa", length: int = 8) -> str:
    return prefix + uuid.uuid4().hex[:length]


def cleanup_user(username: str) -> None:
    """Supprime le fichier utilisateur créé par le test (environnement local)."""
    for candidate in (USERS_DIR / username, USERS_DIR / f"tmp{username}"):
        try:
            candidate.unlink()
        except FileNotFoundError:
            pass
    try:
        for candidate in USERS_DIR.rglob(username):
            if candidate.is_file():
                candidate.unlink()
    except FileNotFoundError:
        pass


@pytest.fixture(scope="session")
def base_url() -> str:
    return BASE_URL


@pytest.fixture(scope="session")
def users_dir() -> Path:
    return USERS_DIR


@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--window-size=1440,1000")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--log-level=3")
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    browser = webdriver.Chrome(options=options)
    browser.set_page_load_timeout(30)
    yield browser
    browser.quit()


@pytest.fixture
def login_page(driver, base_url) -> LoginPage:
    return LoginPage(driver, base_url)


@pytest.fixture
def logged_in(login_page) -> LoginPage:
    """Session Selenium connectée avec le compte de démonstration jojo."""
    login_page.open()
    login_page.login_success("jojo", "bean")
    return login_page


@pytest.fixture
def api(base_url) -> WebToursAPI:
    client = WebToursAPI(base_url)
    client.login("jojo", "bean")
    return client


@pytest.fixture
def api_noauth(base_url) -> WebToursAPI:
    return WebToursAPI(base_url)


@pytest.fixture
def new_username() -> str:
    username = _unique()
    yield username
    cleanup_user(username)


@pytest.fixture
def new_username_14() -> str:
    username = _unique(length=12)  # 'qa' + 12 = 14 caractères
    yield username
    cleanup_user(username)


@pytest.fixture
def fresh_user(base_url) -> dict:
    """Crée un compte unique via HTTP, sans ouvrir de session Selenium."""
    username = _unique()
    client = WebToursAPI(base_url)
    if not client.signup(username, PASSWORD):
        raise AssertionError(f"Création du compte {username} impossible")
    yield {"username": username, "password": PASSWORD, "api": client}
    cleanup_user(username)


@pytest.fixture
def fresh_user_api(base_url) -> dict:
    """Crée et connecte un compte unique via HTTP."""
    username = _unique()
    client = WebToursAPI(base_url)
    if not client.signup(username, PASSWORD):
        raise AssertionError(f"Création du compte {username} impossible")
    client.login(username, PASSWORD)
    yield {"username": username, "password": PASSWORD, "api": client}
    cleanup_user(username)


@pytest.fixture
def fresh_logged_in(login_page, fresh_user) -> LoginPage:
    """Session Selenium connectée avec un compte neuf (isole les données)."""
    login_page.open()
    login_page.login_success(fresh_user["username"], fresh_user["password"])
    return login_page
