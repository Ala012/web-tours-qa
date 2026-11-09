# -*- coding: utf-8 -*-
"""Tests du module RSVF – Vols.

Campagne : 9 tests réels en échec (xfail) + 5 tests de non-régression (PASS).
"""
from __future__ import annotations

import re

import pytest

from pages.flight_page import FlightPage
from pages.navbar import NavBar
from utils.webtours_api import tomorrow

pytestmark = pytest.mark.rsvf


def _open_flights(page) -> FlightPage:
    NavBar(page.driver, page.base_url).click_flights()
    return FlightPage(page.driver, page.base_url)


# --------------------------------------------------------------------------
# FT – Functional Testing (PASS)
# --------------------------------------------------------------------------
@pytest.mark.ft
def test_rsvf_ft_01_recherche_aller_simple(logged_in):
    flight = _open_flights(logged_in)
    flight.search("Denver", "Paris", tomorrow(), passengers=1)
    assert len(flight.outbound_values()) == 4
    text = flight.text()
    assert "Denver" in text and "Paris" in text


@pytest.mark.ft
def test_rsvf_ft_02_recherche_aller_retour(logged_in):
    flight = _open_flights(logged_in)
    flight.search(
        "Denver", "Paris", tomorrow(), return_date=tomorrow(), roundtrip=True
    )
    assert len(flight.outbound_values()) == 4
    assert len(flight.return_values()) == 4


# --------------------------------------------------------------------------
# ET – Error Testing (FAIL – BUG-05)
# --------------------------------------------------------------------------
@pytest.mark.et
@pytest.mark.xfail(
    reason="BUG-05 : date vide -> page incomplète sans message",
    strict=False,
)
def test_rsvf_et_01_date_vide(logged_in):
    flight = _open_flights(logged_in)
    flight.search("Denver", "Paris", "", passengers=1, wait_results=False)
    text = flight.text().lower()
    assert "date" in text and ("error" in text or "invalid" in text or "required" in text)


# --------------------------------------------------------------------------
# PT – Permission Testing (FAIL – BUG-09, BUG-10)
# --------------------------------------------------------------------------
@pytest.mark.pt
@pytest.mark.xfail(
    reason="BUG-09 : prix manipulable dans le POST",
    strict=False,
)
def test_rsvf_pt_01_prix_modifie_post(fresh_user_api):
    api = fresh_user_api["api"]
    search = api.search_flights("Denver", "Paris", tomorrow())
    choices = api.flight_choices(search.text)
    assert choices
    flight_number, price, flight_date = choices[0].split(";")
    tampered = f"{flight_number};1;{flight_date}"
    payment = api.reserve(tampered, passengers=1)
    text = api.text(payment)
    match = re.search(r"Total for 1 ticket\(s\) is =\s*\$ ?([\d.]+)", text)
    assert match, text
    assert float(match.group(1)) == 350.0


@pytest.mark.pt
@pytest.mark.xfail(
    reason="BUG-10 : flightID 999 accepté",
    strict=False,
)
def test_rsvf_pt_02_flightid_falsifie(fresh_user_api):
    api = fresh_user_api["api"]
    api.buy("999;1;01/01/2027", passengers=1)
    invoice = api.text(api.itinerary())
    assert "999" not in invoice
