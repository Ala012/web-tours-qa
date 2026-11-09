# -*- coding: utf-8 -*-
"""Client HTTP bas niveau pour WebTours.

Utilisé pour les tests de sécurité (POST forgés, cookies, IDOR) et pour
préparer des données de test rapidement. Les parcours UI passent par Selenium.
"""
from __future__ import annotations

import re
from datetime import date, timedelta
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup


def tomorrow(fmt: str = "%m/%d/%Y") -> str:
    return (date.today() + timedelta(days=1)).strftime(fmt)


def rotating_hash(username: str) -> int:
    """Réplique la fonction Perl rotatingHash de login.pl."""
    h = len(username)
    for ch in username:
        h = ((h << 5) ^ ord(ch)) & 0xFFFFFFFF
    return h & 127


class WebToursAPI:
    def __init__(self, base_url: str = "http://127.0.0.1:1080", timeout: int = 20):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()

    # ------------------------------------------------------------------ HTTP
    def url(self, path: str) -> str:
        if path.startswith("http://") or path.startswith("https://"):
            return path
        return self.base_url + (path if path.startswith("/") else "/" + path)

    def get(self, path: str, **kwargs) -> requests.Response:
        kwargs.setdefault("timeout", self.timeout)
        return self.session.get(self.url(path), **kwargs)

    def post(self, path: str, data=None, **kwargs) -> requests.Response:
        kwargs.setdefault("timeout", self.timeout)
        return self.session.post(self.url(path), data=data, **kwargs)

    @staticmethod
    def text(response: requests.Response) -> str:
        return BeautifulSoup(response.text, "html.parser").get_text(" ", strip=True)

    # ------------------------------------------------------------- Session
    def reset(self) -> requests.Response:
        return self.get("/cgi-bin/welcome.pl?signOff=true")

    def login(self, username: str = "jojo", password: str = "bean") -> requests.Response:
        self.reset()
        nav = self.get("/cgi-bin/nav.pl?in=home")
        match = re.search(r'name="userSession" value="([^"]+)"', nav.text)
        if not match:
            raise RuntimeError("Impossible de trouver le champ userSession dans nav.pl")
        response = self.post(
            "/cgi-bin/login.pl",
            data={
                "username": username,
                "password": password,
                "userSession": match.group(1),
                "login.x": "10",
                "login.y": "10",
                "JSFormSubmit": "off",
            },
        )
        if "password was correct" not in response.text:
            raise AssertionError(f"Connexion impossible pour {username!r}")
        return response

    def signup(
        self,
        username: str,
        password: str,
        first_name: str = "QA",
        last_name: str = "User",
        address1: str = "1 Test Street",
        address2: str = "Tunis",
    ) -> bool:
        response = self.post(
            "/cgi-bin/login.pl",
            data={
                "username": username,
                "password": password,
                "passwordConfirm": password,
                "firstName": first_name,
                "lastName": last_name,
                "address1": address1,
                "address2": address2,
                "register.x": "10",
                "register.y": "10",
            },
        )
        return "Thank you" in response.text

    # --------------------------------------------------------------- Vols
    def search_flights(
        self,
        depart: str = "Denver",
        arrive: str = "Paris",
        depart_date: str | None = None,
        return_date: str | None = None,
        passengers: int | str = 1,
        roundtrip: bool = False,
        seat_pref: str = "None",
        seat_type: str = "Coach",
    ) -> requests.Response:
        data = {
            "depart": depart,
            "arrive": arrive,
            "departDate": depart_date if depart_date is not None else tomorrow(),
            "returnDate": return_date if return_date is not None else tomorrow(),
            "numPassengers": str(passengers),
            "seatPref": seat_pref,
            "seatType": seat_type,
            "advanceDiscount": "0",
            "findFlights.x": "10",
            "findFlights.y": "10",
        }
        if roundtrip:
            data["roundtrip"] = "on"
        return self.post("/cgi-bin/reservations.pl", data=data)

    @staticmethod
    def flight_choices(html: str, name: str = "outboundFlight") -> list[str]:
        soup = BeautifulSoup(html, "html.parser")
        return [tag.get("value", "") for tag in soup.find_all("input", {"name": name})]

    def reserve(
        self,
        outbound_flight: str,
        passengers: int | str = 1,
        seat_pref: str = "None",
        seat_type: str = "Coach",
        advance_discount: int | str = 0,
        return_flight: str = "",
    ) -> requests.Response:
        return self.post(
            "/cgi-bin/reservations.pl",
            data={
                "outboundFlight": outbound_flight,
                "returnFlight": return_flight,
                "numPassengers": str(passengers),
                "seatType": seat_type,
                "seatPref": seat_pref,
                "advanceDiscount": str(advance_discount),
                "reserveFlights.x": "10",
                "reserveFlights.y": "10",
            },
        )

    def buy(
        self,
        outbound_flight: str,
        passengers: int = 1,
        first_name: str = "QA",
        last_name: str = "User",
        address1: str = "1 Test Street",
        address2: str = "Tunis",
        card: str = "4111111111111111",
        exp_date: str = "12/28",
        return_flight: str = "",
    ) -> requests.Response:
        data = {
            "firstName": first_name,
            "lastName": last_name,
            "address1": address1,
            "address2": address2,
            "creditCard": card,
            "expDate": exp_date,
            "saveCC": "on",
            "oldCCOption": "on",
            "numPassengers": str(passengers),
            "seatType": "Coach",
            "seatPref": "None",
            "outboundFlight": outbound_flight,
            "returnFlight": return_flight,
            "advanceDiscount": "0",
            "JSFormSubmit": "off",
            "buyFlights.x": "10",
            "buyFlights.y": "10",
        }
        for index in range(1, passengers + 1):
            data[f"pass{index}"] = f"{first_name} {last_name}" if index == 1 else f"Passenger {index}"
        return self.post("/cgi-bin/reservations.pl", data=data)

    def book_one(
        self,
        depart: str = "Denver",
        arrive: str = "Paris",
        passengers: int = 1,
        card: str = "4111111111111111",
        exp_date: str = "12/28",
    ) -> str:
        """Recherche, réserve et achète un vol. Retourne le outboundFlight utilisé."""
        search = self.search_flights(depart, arrive, passengers=passengers)
        choices = self.flight_choices(search.text)
        if not choices:
            raise AssertionError("Aucun vol trouvé pour la réservation de test")
        outbound = choices[0]
        self.reserve(outbound, passengers=passengers)
        self.buy(outbound, passengers=passengers, card=card, exp_date=exp_date)
        return outbound

    # ---------------------------------------------------------- Itinéraire
    def itinerary(self) -> requests.Response:
        return self.get("/cgi-bin/itinerary.pl")

    def remove_all(self) -> requests.Response:
        return self.post(
            "/cgi-bin/itinerary.pl",
            data={"removeAllFlights.x": "10", "removeAllFlights.y": "10"},
        )

    def remove_flight(self, flight_id: str, index: int = 1) -> requests.Response:
        return self.post(
            "/cgi-bin/itinerary.pl",
            data={
                str(index): "on",
                "flightID": flight_id,
                "removeFlights.x": "10",
                "removeFlights.y": "10",
            },
        )

    # ------------------------------------------------------------- Cookies
    def set_user_cookie(self, username: str, hash_value: int | None = None) -> None:
        if hash_value is None:
            hash_value = rotating_hash(username)
        host = urlparse(self.base_url).hostname or "127.0.0.1"
        self.session.cookies.set(
            "MTUserInfo",
            f"username&{username}&hash&{hash_value}",
            domain=host,
            path="/",
        )

    def clear_cookies(self) -> None:
        self.session.cookies.clear()
