# -*- coding: utf-8 -*-
"""Tests du module RSVI – Itinéraire.

Campagne : 9 tests réels en échec (xfail) + 5 tests de non-régression (PASS).
"""
from __future__ import annotations

import pytest

from pages.flight_page import FlightPage
from pages.itinerary_page import ItineraryPage
from pages.navbar import NavBar
from utils.webtours_api import tomorrow

pytestmark = pytest.mark.rsvi


def _book_one(page, passengers: int = 1) -> None:
    """Réserve un vol via l'interface et revient à l'état courant."""
    NavBar(page.driver, page.base_url).click_flights()
    flight = FlightPage(page.driver, page.base_url)
    flight.search("Denver", "Paris", tomorrow(), passengers=passengers)
    flight.select_outbound(0)
    flight.fill_payment_and_buy(passengers=passengers)


# --------------------------------------------------------------------------
# FT – Functional Testing (PASS)
# --------------------------------------------------------------------------
@pytest.mark.ft
def test_rsvi_ft_01_affichage_apres_reservation(fresh_logged_in):
    _book_one(fresh_logged_in)
    itinerary = ItineraryPage(
        fresh_logged_in.driver, fresh_logged_in.base_url
    ).open()
    text = itinerary.text()
    assert "Flight Transaction Summary" in text
    assert "Denver" in text and "Paris" in text
    assert itinerary.flight_count() == 1


# --------------------------------------------------------------------------
# PT – Permission Testing (FAIL – BUG-04, BUG-02)
# --------------------------------------------------------------------------
@pytest.mark.pt
@pytest.mark.xfail(
    reason="BUG-04 : IDOR, itinéraire de admin via cookie forgé",
    strict=False,
)
def test_rsvi_pt_01_idor(api_noauth):
    api_noauth.set_user_cookie("admin", 78)
    response = api_noauth.itinerary()
    assert "admin" not in api_noauth.text(response).lower()


@pytest.mark.pt
@pytest.mark.xfail(
    reason="BUG-02 : itinerary.pl accessible sans session",
    strict=False,
)
def test_rsvi_pt_02_acces_sans_session(api_noauth):
    response = api_noauth.itinerary()
    assert response.status_code in (302, 401, 403) or "login" in response.url.lower()


@pytest.mark.pt
@pytest.mark.xfail(
    reason="BUG-02 : suppression sans session acceptée",
    strict=False,
)
def test_rsvi_pt_03_suppression_sans_session(api_noauth, users_dir):
    response = api_noauth.post("/cgi-bin/itinerary.pl", data={"removeAllFlights.x": "1"})
    assert response.status_code in (401, 403)
    # Nettoyage du fichier temporaire créé par le script pour un userID vide.
    (users_dir / "tmp").unlink(missing_ok=True)
