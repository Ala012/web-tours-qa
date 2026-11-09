# -*- coding: utf-8 -*-
"""Tests du module RSVI – Itinéraire."""
from __future__ import annotations

import re

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
# FT – Functional Testing
# --------------------------------------------------------------------------
@pytest.mark.ft
def test_rsvi_ft_01_affichage_apres_reservation(fresh_logged_in):
    _book_one(fresh_logged_in)
    itinerary = ItineraryPage(fresh_logged_in.driver, fresh_logged_in.base_url).open()
    text = itinerary.text()
    assert "Flight Transaction Summary" in text
    assert "Denver" in text and "Paris" in text
    assert itinerary.flight_count() == 1


@pytest.mark.ft
def test_rsvi_ft_02_suppression_un_vol(fresh_logged_in):
    _book_one(fresh_logged_in)
    _book_one(fresh_logged_in)
    itinerary = ItineraryPage(fresh_logged_in.driver, fresh_logged_in.base_url).open()
    assert itinerary.flight_count() == 2
    itinerary.remove_first()
    assert itinerary.flight_count() == 1


@pytest.mark.ft
def test_rsvi_ft_03_suppression_tous_vols(fresh_logged_in):
    _book_one(fresh_logged_in)
    _book_one(fresh_logged_in)
    itinerary = ItineraryPage(fresh_logged_in.driver, fresh_logged_in.base_url).open()
    assert itinerary.flight_count() == 2
    itinerary.remove_all()
    assert itinerary.is_empty()


# --------------------------------------------------------------------------
# ET – Error Testing
# --------------------------------------------------------------------------
@pytest.mark.et
def test_rsvi_et_01_id_vol_invalide(fresh_user_api):
    api = fresh_user_api["api"]
    api.book_one()
    itinerary = api.itinerary()
    flight_ids = re.findall(r'name="flightID" value="([^"]+)"', itinerary.text)
    assert flight_ids, "Aucune réservation trouvée pour le test"
    response = api.remove_flight("INVALID-ID")
    assert "database synchronization error" in api.text(response)


@pytest.mark.et
def test_rsvi_et_02_sans_reservation(fresh_logged_in):
    itinerary = ItineraryPage(fresh_logged_in.driver, fresh_logged_in.base_url).open()
    assert itinerary.is_empty()


@pytest.mark.et
def test_rsvi_et_03_double_suppression(fresh_logged_in):
    _book_one(fresh_logged_in)
    itinerary = ItineraryPage(fresh_logged_in.driver, fresh_logged_in.base_url).open()
    itinerary.remove_all()
    assert itinerary.is_empty()
    # Le bouton "Cancel All" n'est plus affiché : on recharge la page pour
    # vérifier que l'état vide est stable et qu'aucune erreur n'apparaît.
    itinerary.open()
    assert itinerary.is_empty()


# --------------------------------------------------------------------------
# BT – Boundary Testing
# --------------------------------------------------------------------------
@pytest.mark.bt
def test_rsvi_bt_01_un_passager(fresh_logged_in):
    _book_one(fresh_logged_in, passengers=1)
    itinerary = ItineraryPage(fresh_logged_in.driver, fresh_logged_in.base_url).open()
    text = itinerary.text()
    assert "1 Coach class ticket" in text or "A total of 1 scheduled flights" in text


@pytest.mark.bt
def test_rsvi_bt_02_8_passagers(fresh_logged_in):
    _book_one(fresh_logged_in, passengers=8)
    itinerary = ItineraryPage(fresh_logged_in.driver, fresh_logged_in.base_url).open()
    text = itinerary.text()
    assert "8 Coach class tickets" in text
    assert "Total Charge" in text


@pytest.mark.bt
def test_rsvi_bt_03_dernier_vol(fresh_logged_in):
    _book_one(fresh_logged_in, passengers=1)
    itinerary = ItineraryPage(fresh_logged_in.driver, fresh_logged_in.base_url).open()
    assert itinerary.flight_count() == 1
    itinerary.remove_first()
    assert itinerary.is_empty()


# --------------------------------------------------------------------------
# PT – Permission Testing
# --------------------------------------------------------------------------
@pytest.mark.pt
@pytest.mark.xfail(reason="BUG-04 : IDOR, itinéraire de admin via cookie forgé", strict=False)
def test_rsvi_pt_01_idor(api_noauth):
    api_noauth.set_user_cookie("admin", 78)
    response = api_noauth.itinerary()
    assert "admin" not in api_noauth.text(response).lower()


@pytest.mark.pt
@pytest.mark.xfail(reason="BUG-02 : itinerary.pl accessible sans session", strict=False)
def test_rsvi_pt_02_acces_sans_session(api_noauth):
    response = api_noauth.itinerary()
    assert response.status_code in (302, 401, 403) or "login" in response.url.lower()


@pytest.mark.pt
@pytest.mark.xfail(reason="BUG-02 : suppression sans session acceptée", strict=False)
def test_rsvi_pt_03_suppression_sans_session(api_noauth, users_dir):
    response = api_noauth.post("/cgi-bin/itinerary.pl", data={"removeAllFlights.x": "1"})
    assert response.status_code in (401, 403)
    # Nettoyage du fichier temporaire créé par le script pour un userID vide.
    (users_dir / "tmp").unlink(missing_ok=True)
