# -*- coding: utf-8 -*-
"""Tests du module RSVA – Authentification."""
from __future__ import annotations

import pytest

pytestmark = pytest.mark.rsva


# --------------------------------------------------------------------------
# FT – Functional Testing
# --------------------------------------------------------------------------
@pytest.mark.ft
def test_rsva_ft_01_login_valide(login_page):
    login_page.open()
    login_page.login_success("jojo", "bean")
    assert "Welcome, jojo" in login_page.get_info_text()


@pytest.mark.ft
def test_rsva_ft_02_deconnexion(login_page):
    login_page.open()
    login_page.login_success("jojo", "bean")
    login_page.logout()
    assert login_page.is_login_form_displayed()


@pytest.mark.ft
def test_rsva_ft_03_creation_compte(login_page, new_username):
    login_page.open()
    login_page.open_signup()
    login_page.register(new_username, "Passw0rd!", "Passw0rd!")
    assert f"Thank you, {new_username}" in login_page.registration_message()


# --------------------------------------------------------------------------
# ET – Error Testing
# --------------------------------------------------------------------------
@pytest.mark.et
def test_rsva_et_01_mot_de_passe_incorrect(login_page):
    login_page.open()
    login_page.login("jojo", "mauvais_mot_de_passe")
    assert "Incorrect Password" in login_page.get_info_text()


@pytest.mark.et
def test_rsva_et_02_champs_vides(login_page):
    login_page.open()
    login_page.login("", "")
    assert "Incorrect Password" in login_page.get_info_text()


@pytest.mark.et
def test_rsva_et_03_confirmation_differente(login_page, new_username):
    login_page.open()
    login_page.open_signup()
    login_page.register(new_username, "Passw0rd!", "AutrePassw0rd!")
    assert "Your password is invalid" in login_page.registration_message()


# --------------------------------------------------------------------------
# BT – Boundary Testing
# --------------------------------------------------------------------------
@pytest.mark.bt
def test_rsva_bt_01_username_14_caracteres(login_page, new_username_14):
    login_page.open()
    login_page.open_signup()
    login_page.register(new_username_14, "Passw0rd!", "Passw0rd!")
    assert f"Thank you, {new_username_14}" in login_page.registration_message()


@pytest.mark.bt
@pytest.mark.xfail(reason="BUG-11 : aucune politique de mot de passe (1 caractère accepté)", strict=False)
def test_rsva_bt_02_mot_de_passe_1_caractere(login_page, new_username):
    login_page.open()
    login_page.open_signup()
    login_page.register(new_username, "a", "a")
    assert "Your password is invalid" in login_page.registration_message()


@pytest.mark.bt
@pytest.mark.xfail(reason="BUG-12 : 'jojo!' est normalisé en 'jojo' et accepté", strict=False)
def test_rsva_bt_03_username_caracteres_speciaux(login_page):
    login_page.open()
    login_page.login("jojo!", "bean")
    assert "Incorrect Password" in login_page.get_info_text()


# --------------------------------------------------------------------------
# PT – Permission Testing
# --------------------------------------------------------------------------
@pytest.mark.pt
@pytest.mark.xfail(reason="BUG-01 : reservations.pl accessible sans authentification", strict=False)
def test_rsva_pt_01_reservations_sans_login(api_noauth):
    response = api_noauth.get("/cgi-bin/reservations.pl?page=welcome")
    assert response.status_code in (302, 401, 403) or "login" in response.url.lower()


@pytest.mark.pt
@pytest.mark.xfail(reason="BUG-02 : itinerary.pl accessible sans authentification", strict=False)
def test_rsva_pt_02_itinerary_sans_login(api_noauth):
    response = api_noauth.get("/cgi-bin/itinerary.pl")
    assert response.status_code in (302, 401, 403) or "login" in response.url.lower()


@pytest.mark.pt
@pytest.mark.xfail(reason="BUG-03 : admin.pl accessible sans authentification", strict=False)
def test_rsva_pt_03_admin_sans_login(api_noauth):
    response = api_noauth.get("/cgi-bin/admin.pl")
    assert response.status_code in (401, 403)
