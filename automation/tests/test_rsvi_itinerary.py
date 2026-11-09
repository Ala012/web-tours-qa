# -*- coding: utf-8 -*-
"""Tests du module RSVI – Itinéraire (campagne réduite : 3 tests réels)."""
from __future__ import annotations

import pytest

pytestmark = pytest.mark.rsvi


# --------------------------------------------------------------------------
# PT – Permission Testing (sécurité)
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
