# -*- coding: utf-8 -*-
"""Tests du module RSVA – Authentification (campagne réduite : 3 tests réels)."""
from __future__ import annotations

import pytest

pytestmark = pytest.mark.rsva


# --------------------------------------------------------------------------
# PT – Permission Testing
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


# --------------------------------------------------------------------------
# BT – Boundary Testing
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
