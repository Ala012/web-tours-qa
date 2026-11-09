# -*- coding: utf-8 -*-
"""Tests du module RSVA – Authentification.

Campagne : 9 tests réels en échec (xfail) + 5 tests de non-régression (PASS).
"""
from __future__ import annotations

import pytest

pytestmark = pytest.mark.rsva


# --------------------------------------------------------------------------
# FT – Functional Testing (PASS)
# --------------------------------------------------------------------------
@pytest.mark.ft
def test_rsva_ft_01_login_valide(login_page):
    login_page.open()
    login_page.login_success("jojo", "bean")
    assert "Welcome, jojo" in login_page.get_info_text()


# --------------------------------------------------------------------------
# ET – Error Testing (PASS)
# --------------------------------------------------------------------------
@pytest.mark.et
def test_rsva_et_01_mot_de_passe_incorrect(login_page):
    login_page.open()
    login_page.login("jojo", "mauvais_mot_de_passe")
    assert "Incorrect Password" in login_page.get_info_text()


# --------------------------------------------------------------------------
# BT – Boundary Testing (FAIL – BUG-12)
# --------------------------------------------------------------------------
@pytest.mark.bt
@pytest.mark.xfail(
    reason="BUG-12 : 'jojo!' normalisé en 'jojo' et accepté",
    strict=False,
)
def test_rsva_bt_03_username_caracteres_speciaux(login_page):
    login_page.open()
    login_page.login("jojo!", "bean")
    assert "Incorrect Password" in login_page.get_info_text()


# --------------------------------------------------------------------------
# PT – Permission Testing (FAIL – BUG-01, BUG-03)
# --------------------------------------------------------------------------
@pytest.mark.pt
@pytest.mark.xfail(
    reason="BUG-01 : reservations.pl accessible sans authentification",
    strict=False,
)
def test_rsva_pt_01_reservations_sans_login(api_noauth):
    response = api_noauth.get("/cgi-bin/reservations.pl?page=welcome")
    assert response.status_code in (302, 401, 403) or "login" in response.url.lower()


@pytest.mark.pt
@pytest.mark.xfail(
    reason="BUG-03 : admin.pl accessible sans authentification",
    strict=False,
)
def test_rsva_pt_03_admin_sans_login(api_noauth):
    response = api_noauth.get("/cgi-bin/admin.pl")
    assert response.status_code in (401, 403)
