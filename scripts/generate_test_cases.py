#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Génère les fiches de test manuelles et les fichiers d'import Jira/Xray.

Source unique de vérité : la liste TESTS ci-dessous.
Exécution : python scripts/generate_test_cases.py
"""
from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANUAL = ROOT / "tests-manuels"
XRAY = ROOT / "jira-xray"

MODULES = {
    "RSVA": {
        "name": "RSVA – Authentification",
        "folder": "RSVA-Authentication",
        "story": "WT-US-01 / WT-US-02",
    },
    "RSVF": {
        "name": "RSVF – Vols",
        "folder": "RSVF-Flight",
        "story": "WT-US-03",
    },
    "RSVI": {
        "name": "RSVI – Itinéraire",
        "folder": "RSVI-Itinerary",
        "story": "WT-US-04",
    },
}

TYPES = {
    "FT": {"name": "FT – Functional Testing", "folder": "FT - Functional Testing"},
    "ET": {"name": "ET – Error Testing", "folder": "ET - Error Testing"},
    "BT": {"name": "BT – Boundary Testing", "folder": "BT - Boundary Testing"},
    "PT": {"name": "PT – Permission Testing", "folder": "PT - Permission Testing"},
}

# ---------------------------------------------------------------------------
# Données de test
# Chaque test : id, module, type, summary, priority, automated, status,
# preconditions (liste), data (liste), steps (liste de tuples action/attendu),
# actual (résultat réel constaté), bug (référence éventuelle)
# ---------------------------------------------------------------------------
TESTS = [
    # ======================= RSVA – Authentification =======================
    {
        "id": "RSVA-FT-01",
        "module": "RSVA",
        "type": "FT",
        "summary": "Connexion avec des identifiants valides",
        "priority": "High",
        "automated": "test_rsva_authentication.py::test_rsva_ft_01_login_valide",
        "status": "Passé",
        "preconditions": [
            "Le serveur WebTours est démarré sur http://127.0.0.1:1080.",
            "Le compte de démonstration jojo / bean existe.",
        ],
        "data": ["username = jojo", "password = bean"],
        "steps": [
            ("Ouvrir http://127.0.0.1:1080/WebTours/index.htm.", "La page Web Tours s'affiche avec le cadre de navigation et la page d'accueil."),
            ("Saisir jojo dans le champ Username et bean dans le champ Password.", "Les deux champs sont renseignés."),
            ("Cliquer sur le bouton Login.", "Le message « Welcome, jojo » s'affiche et le menu Flights / Itinerary / Home / SignOff apparaît."),
        ],
        "actual": "Connexion réussie, message de bienvenue affiché.",
    },
    {
        "id": "RSVA-FT-02",
        "module": "RSVA",
        "type": "FT",
        "summary": "Déconnexion de l'utilisateur (Sign Off)",
        "priority": "High",
        "automated": "test_rsva_authentication.py::test_rsva_ft_02_deconnexion",
        "status": "Passé",
        "preconditions": ["L'utilisateur jojo est connecté."],
        "data": [],
        "steps": [
            ("Cliquer sur le bouton SignOff du menu de navigation.", "Le cadre de navigation revient au formulaire de connexion."),
            ("Vérifier la page d'accueil.", "Le message de bienvenue et les liens réservés aux utilisateurs connectés ne sont plus accessibles."),
        ],
        "actual": "Déconnexion effectuée, retour au formulaire de login.",
    },
    {
        "id": "RSVA-FT-03",
        "module": "RSVA",
        "type": "FT",
        "summary": "Création d'un nouveau compte client (Sign Up)",
        "priority": "High",
        "automated": "test_rsva_authentication.py::test_rsva_ft_03_creation_compte",
        "status": "Passé",
        "preconditions": ["Le serveur WebTours est démarré."],
        "data": ["username = qa<horodatage>", "password = Passw0rd!", "firstName = QA", "lastName = User"],
        "steps": [
            ("Ouvrir la page d'accueil et cliquer sur le lien « sign up now ».", "Le formulaire Customer Profile s'affiche dans le cadre de droite."),
            ("Remplir le username, le password, la confirmation et les informations de profil.", "Les champs sont acceptés."),
            ("Cliquer sur le bouton Next (register).", "Le message « Thank you, <username>, for registering » s'affiche et l'utilisateur est connecté."),
        ],
        "actual": "Compte créé et connexion automatique.",
    },
    {
        "id": "RSVA-ET-01",
        "module": "RSVA",
        "type": "ET",
        "summary": "Connexion avec un mot de passe incorrect",
        "priority": "High",
        "automated": "test_rsva_authentication.py::test_rsva_et_01_mot_de_passe_incorrect",
        "status": "Passé",
        "preconditions": ["Le compte jojo / bean existe."],
        "data": ["username = jojo", "password = mauvais_mot_de_passe"],
        "steps": [
            ("Saisir jojo et un mot de passe erroné.", "Les champs sont renseignés."),
            ("Cliquer sur Login.", "La page « Web Tours Error - Incorrect Password » s'affiche et l'utilisateur n'est pas connecté."),
        ],
        "actual": "Message d'erreur affiché, accès refusé.",
    },
    {
        "id": "RSVA-ET-02",
        "module": "RSVA",
        "type": "ET",
        "summary": "Connexion avec des champs vides",
        "priority": "Medium",
        "automated": "test_rsva_authentication.py::test_rsva_et_02_champs_vides",
        "status": "Passé",
        "preconditions": ["Le formulaire de connexion est affiché."],
        "data": ["username = (vide)", "password = (vide)"],
        "steps": [
            ("Laisser les champs Username et Password vides.", "Les champs sont vides."),
            ("Cliquer sur Login.", "Un message d'erreur est affiché et la connexion est refusée."),
        ],
        "actual": "Message « Incorrect Password » affiché.",
    },
    {
        "id": "RSVA-ET-03",
        "module": "RSVA",
        "type": "ET",
        "summary": "Création de compte avec confirmation du mot de passe différente",
        "priority": "Medium",
        "automated": "test_rsva_authentication.py::test_rsva_et_03_confirmation_differente",
        "status": "Passé",
        "preconditions": ["Le formulaire Customer Profile est affiché."],
        "data": ["password = Passw0rd!", "passwordConfirm = AutrePassw0rd!"],
        "steps": [
            ("Remplir le formulaire avec deux mots de passe différents.", "Les champs sont renseignés."),
            ("Cliquer sur register.", "Le message « Your password is invalid. Please re-enter it and it's confirmation. » s'affiche et aucun compte n'est créé."),
        ],
        "actual": "Création refusée avec message d'erreur.",
    },
    {
        "id": "RSVA-BT-01",
        "module": "RSVA",
        "type": "BT",
        "summary": "Nom d'utilisateur à la limite haute de 14 caractères",
        "priority": "Medium",
        "automated": "test_rsva_authentication.py::test_rsva_bt_01_username_14_caracteres",
        "status": "Passé",
        "preconditions": ["Le formulaire Customer Profile est affiché."],
        "data": ["username = qa123456789012 (14 caractères)"],
        "steps": [
            ("Saisir un username alphanumérique de 14 caractères.", "Le champ accepte les 14 caractères."),
            ("Compléter le formulaire et cliquer sur register.", "Le compte est créé et le message de bienvenue s'affiche."),
        ],
        "actual": "Compte de 14 caractères accepté.",
    },
    {
        "id": "RSVA-BT-02",
        "module": "RSVA",
        "type": "BT",
        "summary": "Mot de passe d'un seul caractère",
        "priority": "Medium",
        "automated": "test_rsva_authentication.py::test_rsva_bt_02_mot_de_passe_1_caractere",
        "status": "Échoué – BUG-11",
        "bug": "BUG-11",
        "preconditions": ["Le formulaire Customer Profile est affiché."],
        "data": ["password = a", "passwordConfirm = a"],
        "steps": [
            ("Saisir un mot de passe d'un seul caractère.", "Le champ accepte la saisie."),
            ("Cliquer sur register.", "Le système doit refuser un mot de passe trop faible (longueur minimale)."),
        ],
        "actual": "Le compte est créé avec un mot de passe d'un caractère : aucune politique de complexité n'est appliquée.",
    },
    {
        "id": "RSVA-BT-03",
        "module": "RSVA",
        "type": "BT",
        "summary": "Connexion avec des caractères spéciaux dans le nom d'utilisateur",
        "priority": "High",
        "automated": "test_rsva_authentication.py::test_rsva_bt_03_username_caracteres_speciaux",
        "status": "Échoué – BUG-12",
        "bug": "BUG-12",
        "preconditions": ["Le compte jojo / bean existe."],
        "data": ["username = jojo!", "password = bean"],
        "steps": [
            ("Saisir jojo! comme username et bean comme password.", "Les champs sont renseignés."),
            ("Cliquer sur Login.", "La connexion doit être refusée car le username saisi ne correspond pas exactement au compte jojo."),
        ],
        "actual": "La connexion réussit : les caractères non alphanumériques sont supprimés silencieusement (jojo! devient jojo).",
    },
    {
        "id": "RSVA-PT-01",
        "module": "RSVA",
        "type": "PT",
        "summary": "Accès direct à reservations.pl sans être connecté",
        "priority": "Critical",
        "automated": "test_rsva_authentication.py::test_rsva_pt_01_reservations_sans_login",
        "status": "Échoué – BUG-01",
        "bug": "BUG-01",
        "preconditions": ["Aucune session utilisateur n'est ouverte."],
        "data": ["URL = /cgi-bin/reservations.pl?page=welcome"],
        "steps": [
            ("Ouvrir directement l'URL de recherche de vols sans passer par le login.", "L'application doit rediriger vers la page de connexion."),
            ("Vérifier le contenu affiché.", "Aucun formulaire de réservation ne doit être accessible sans authentification."),
        ],
        "actual": "Le formulaire « Find Flight » est affiché sans authentification.",
    },
    {
        "id": "RSVA-PT-02",
        "module": "RSVA",
        "type": "PT",
        "summary": "Accès direct à itinerary.pl sans être connecté",
        "priority": "High",
        "automated": "test_rsva_authentication.py::test_rsva_pt_02_itinerary_sans_login",
        "status": "Échoué – BUG-02",
        "bug": "BUG-02",
        "preconditions": ["Aucune session utilisateur n'est ouverte."],
        "data": ["URL = /cgi-bin/itinerary.pl"],
        "steps": [
            ("Ouvrir directement l'URL de l'itinéraire.", "L'application doit rediriger vers la page de connexion."),
            ("Vérifier le contenu affiché.", "Aucune donnée d'itinéraire ne doit être accessible."),
        ],
        "actual": "La page Itinerary est affichée avec le message « No flights have been reserved ».",
    },
    {
        "id": "RSVA-PT-03",
        "module": "RSVA",
        "type": "PT",
        "summary": "Accès à la page d'administration sans authentification",
        "priority": "Critical",
        "automated": "test_rsva_authentication.py::test_rsva_pt_03_admin_sans_login",
        "status": "Échoué – BUG-03",
        "bug": "BUG-03",
        "preconditions": ["Aucune session administrateur n'est ouverte."],
        "data": ["URL = /cgi-bin/admin.pl"],
        "steps": [
            ("Ouvrir directement l'URL admin.pl.", "L'accès doit être refusé (401/403) ou rediriger vers le login."),
            ("Vérifier les options serveur affichées.", "Aucune option de configuration ne doit être modifiable sans authentification."),
        ],
        "actual": "La page « Web Tours Admin Page » est accessible et les options serveur sont modifiables.",
    },
    # ============================ RSVF – Vols ==============================
    {
        "id": "RSVF-FT-01",
        "module": "RSVF",
        "type": "FT",
        "summary": "Recherche d'un vol aller simple Denver → Paris",
        "priority": "High",
        "automated": "test_rsvf_flight.py::test_rsvf_ft_01_recherche_aller_simple",
        "status": "Passé",
        "preconditions": ["L'utilisateur jojo est connecté.", "La date de départ est fixée à demain."],
        "data": ["depart = Denver", "arrive = Paris", "departDate = demain (MM/DD/YYYY)", "numPassengers = 1"],
        "steps": [
            ("Cliquer sur Flights dans le menu.", "Le formulaire Find Flight s'affiche."),
            ("Sélectionner Denver, Paris, la date de demain et 1 passager.", "Les valeurs sont sélectionnées."),
            ("Cliquer sur le bouton Next (findFlights).", "Quatre vols (040, 041, 042, 043) sont proposés avec les horaires et les prix."),
        ],
        "actual": "Quatre vols affichés pour Denver → Paris.",
    },
    {
        "id": "RSVF-FT-02",
        "module": "RSVF",
        "type": "FT",
        "summary": "Recherche d'un vol aller-retour",
        "priority": "High",
        "automated": "test_rsvf_flight.py::test_rsvf_ft_02_recherche_aller_retour",
        "status": "Passé",
        "preconditions": ["L'utilisateur jojo est connecté."],
        "data": ["depart = Denver", "arrive = Paris", "roundtrip = coché"],
        "steps": [
            ("Ouvrir le formulaire Find Flight.", "Le formulaire s'affiche."),
            ("Cocher Roundtrip ticket et lancer la recherche.", "Les vols aller et les vols retour sont affichés."),
        ],
        "actual": "Les deux groupes de vols (outboundFlight et returnFlight) sont affichés.",
    },
    {
        "id": "RSVF-FT-03",
        "module": "RSVF",
        "type": "FT",
        "summary": "Réservation et paiement d'un vol",
        "priority": "High",
        "automated": "test_rsvf_flight.py::test_rsvf_ft_03_reservation_paiement",
        "status": "Passé",
        "preconditions": ["L'utilisateur jojo est connecté.", "Un vol Denver → Paris est recherché."],
        "data": ["Carte = 4111111111111111", "Expiration = 12/28", "Passager = Jojo Bean"],
        "steps": [
            ("Sélectionner le premier vol et cliquer sur Next (reserveFlights).", "La page Payment Details s'affiche avec le total."),
            ("Remplir les informations de paiement et cliquer sur Next (buyFlights).", "La page « Reservation Made! Invoice » s'affiche avec le total facturé."),
        ],
        "actual": "Réservation confirmée et facture affichée.",
    },
    {
        "id": "RSVF-ET-01",
        "module": "RSVF",
        "type": "ET",
        "summary": "Recherche avec une date de départ vide",
        "priority": "High",
        "automated": "test_rsvf_flight.py::test_rsvf_et_01_date_vide",
        "status": "Échoué – BUG-05",
        "bug": "BUG-05",
        "preconditions": ["L'utilisateur jojo est connecté.", "Le formulaire Find Flight est affiché."],
        "data": ["departDate = (vide)"],
        "steps": [
            ("Vider le champ Departure Date.", "Le champ est vide."),
            ("Cliquer sur Next (findFlights).", "Un message de validation doit s'afficher et le formulaire doit rester utilisable."),
        ],
        "actual": "La page se limite au titre « Find Flight » : formulaire absent, aucun message d'erreur. Le log Apache contient « Month '-1' out of range ».",
    },
    {
        "id": "RSVF-ET-02",
        "module": "RSVF",
        "type": "ET",
        "summary": "Recherche avec une date invalide (13/45/2026)",
        "priority": "High",
        "automated": "test_rsvf_flight.py::test_rsvf_et_02_date_invalide",
        "status": "Échoué – BUG-05",
        "bug": "BUG-05",
        "preconditions": ["Le formulaire Find Flight est affiché."],
        "data": ["departDate = 13/45/2026"],
        "steps": [
            ("Saisir 13/45/2026 dans Departure Date.", "La valeur est saisie."),
            ("Cliquer sur Next (findFlights).", "Un message d'erreur explicite doit être affiché."),
        ],
        "actual": "Page incomplète sans formulaire ni message d'erreur ; erreur Perl dans le log.",
    },
    {
        "id": "RSVF-ET-03",
        "module": "RSVF",
        "type": "ET",
        "summary": "Recherche avec la ville de départ identique à la ville d'arrivée",
        "priority": "Medium",
        "automated": "test_rsvf_flight.py::test_rsvf_et_03_meme_ville",
        "status": "Échoué – BUG-07",
        "bug": "BUG-07",
        "preconditions": ["Le formulaire Find Flight est affiché."],
        "data": ["depart = Denver", "arrive = Denver"],
        "steps": [
            ("Sélectionner Denver pour le départ et Denver pour l'arrivée.", "Les deux listes affichent Denver."),
            ("Cliquer sur Next (findFlights).", "La recherche doit être refusée avec un message explicite."),
        ],
        "actual": "Quatre vols fictifs Denver → Denver sont proposés à 0 $.",
    },
    {
        "id": "RSVF-BT-01",
        "module": "RSVF",
        "type": "BT",
        "summary": "Recherche avec le nombre minimum de passagers (1)",
        "priority": "Medium",
        "automated": "test_rsvf_flight.py::test_rsvf_bt_01_un_passager",
        "status": "Passé",
        "preconditions": ["Le formulaire Find Flight est affiché."],
        "data": ["numPassengers = 1"],
        "steps": [
            ("Saisir 1 passager et lancer la recherche.", "Quatre vols sont affichés et le total correspond à 1 billet."),
        ],
        "actual": "Recherche acceptée avec 1 passager.",
    },
    {
        "id": "RSVF-BT-02",
        "module": "RSVF",
        "type": "BT",
        "summary": "Recherche avec zéro passager",
        "priority": "High",
        "automated": "test_rsvf_flight.py::test_rsvf_bt_02_zero_passager",
        "status": "Échoué – BUG-08",
        "bug": "BUG-08",
        "preconditions": ["Le formulaire Find Flight est affiché."],
        "data": ["numPassengers = 0"],
        "steps": [
            ("Saisir 0 dans No. of Passengers.", "La valeur 0 est saisie."),
            ("Cliquer sur Next (findFlights).", "La recherche doit être refusée : le nombre de passagers doit être supérieur ou égal à 1."),
        ],
        "actual": "Les vols sont affichés normalement, sans validation.",
    },
    {
        "id": "RSVF-BT-03",
        "module": "RSVF",
        "type": "BT",
        "summary": "Recherche avec un nombre de passagers très élevé (999)",
        "priority": "Medium",
        "automated": "test_rsvf_flight.py::test_rsvf_bt_03_999_passagers",
        "status": "Échoué – BUG-08",
        "bug": "BUG-08",
        "preconditions": ["Le formulaire Find Flight est affiché."],
        "data": ["numPassengers = 999"],
        "steps": [
            ("Saisir 999 passagers.", "La valeur est saisie."),
            ("Cliquer sur Next (findFlights).", "La recherche doit être refusée au-delà du maximum autorisé."),
        ],
        "actual": "Les vols sont affichés normalement ; aucune limite haute n'est appliquée.",
    },
    {
        "id": "RSVF-PT-01",
        "module": "RSVF",
        "type": "PT",
        "summary": "Manipulation du prix dans la requête POST",
        "priority": "Critical",
        "automated": "test_rsvf_flight.py::test_rsvf_pt_01_prix_modifie_post",
        "status": "Échoué – BUG-09",
        "bug": "BUG-09",
        "preconditions": ["L'utilisateur est connecté.", "Un vol Denver → Paris est recherché."],
        "data": ["outboundFlight original = 040;350;11/10/2026", "outboundFlight modifié = 040;1;11/10/2026"],
        "steps": [
            ("Intercepter la requête POST reserveFlights.", "La requête contient le prix du vol."),
            ("Remplacer 350 par 1 dans le champ outboundFlight et soumettre.", "Le serveur doit recalculer le prix ou refuser la requête."),
            ("Finaliser le paiement.", "Le montant facturé doit être le prix réel du vol (350 $)."),
        ],
        "actual": "Le serveur fait confiance au prix envoyé : la facture est de 1 $.",
    },
    {
        "id": "RSVF-PT-02",
        "module": "RSVF",
        "type": "PT",
        "summary": "Falsification de l'identifiant de vol (flightID)",
        "priority": "Critical",
        "automated": "test_rsvf_flight.py::test_rsvf_pt_02_flightid_falsifie",
        "status": "Échoué – BUG-10",
        "bug": "BUG-10",
        "preconditions": ["L'utilisateur est connecté."],
        "data": ["outboundFlight = 999;1;01/01/2027"],
        "steps": [
            ("Soumettre directement une réservation avec un numéro de vol inexistant (999).", "Le serveur doit refuser un vol qui n'existe pas."),
            ("Finaliser le paiement.", "Aucune facture ne doit être générée pour un vol inexistant."),
        ],
        "actual": "La facture est générée pour le vol 999 Zurich → Zurich à 1 $.",
    },
    {
        "id": "RSVF-PT-03",
        "module": "RSVF",
        "type": "PT",
        "summary": "Accès direct à buyFlights sans sélection de vol",
        "priority": "Critical",
        "automated": "test_rsvf_flight.py::test_rsvf_pt_03_buy_direct",
        "status": "Échoué – BUG-10",
        "bug": "BUG-10",
        "preconditions": ["L'utilisateur est connecté."],
        "data": ["POST reservations.pl avec buyFlights.x=1 et des champs arbitraires"],
        "steps": [
            ("Envoyer directement une requête POST buyFlights sans passer par la recherche ni la sélection.", "Le serveur doit refuser la requête."),
            ("Vérifier l'itinéraire.", "Aucune réservation ne doit être enregistrée."),
        ],
        "actual": "Une réservation est créée et une facture est affichée.",
    },
    # ========================= RSVI – Itinéraire ===========================
    {
        "id": "RSVI-FT-01",
        "module": "RSVI",
        "type": "FT",
        "summary": "Affichage de l'itinéraire après une réservation",
        "priority": "High",
        "automated": "test_rsvi_itinerary.py::test_rsvi_ft_01_affichage_apres_reservation",
        "status": "Passé",
        "preconditions": ["L'utilisateur est connecté.", "Au moins un vol a été réservé."],
        "data": ["Vol Denver → Paris du lendemain"],
        "steps": [
            ("Cliquer sur Itinerary dans le menu.", "La page Itinerary s'affiche."),
            ("Vérifier les informations du vol.", "Le vol, la date, le prix et les 4 derniers chiffres de la carte sont affichés."),
        ],
        "actual": "Itinéraire affiché avec les détails de la réservation.",
    },
    {
        "id": "RSVI-FT-02",
        "module": "RSVI",
        "type": "FT",
        "summary": "Suppression d'un vol de l'itinéraire",
        "priority": "High",
        "automated": "test_rsvi_itinerary.py::test_rsvi_ft_02_suppression_un_vol",
        "status": "Passé",
        "preconditions": ["L'utilisateur possède au moins deux réservations."],
        "data": ["Cocher le premier vol"],
        "steps": [
            ("Ouvrir l'itinéraire.", "Les vols réservés sont listés."),
            ("Cocher le premier vol et cliquer sur Cancel Reservation.", "Le vol est supprimé et les autres vols restent affichés."),
        ],
        "actual": "Suppression effectuée, itinéraire mis à jour.",
    },
    {
        "id": "RSVI-FT-03",
        "module": "RSVI",
        "type": "FT",
        "summary": "Suppression de tous les vols de l'itinéraire",
        "priority": "High",
        "automated": "test_rsvi_itinerary.py::test_rsvi_ft_03_suppression_tous_vols",
        "status": "Passé",
        "preconditions": ["L'utilisateur possède au moins une réservation."],
        "data": [],
        "steps": [
            ("Ouvrir l'itinéraire.", "Les vols réservés sont listés."),
            ("Cliquer sur Cancel All Reservations.", "Tous les vols sont supprimés et le message « No flights have been reserved » s'affiche."),
        ],
        "actual": "Itinéraire vidé.",
    },
    {
        "id": "RSVI-ET-01",
        "module": "RSVI",
        "type": "ET",
        "summary": "Suppression avec un identifiant de vol invalide",
        "priority": "High",
        "automated": "test_rsvi_itinerary.py::test_rsvi_et_01_id_vol_invalide",
        "status": "Passé",
        "preconditions": ["L'utilisateur possède une réservation."],
        "data": ["flightID = INVALID-ID"],
        "steps": [
            ("Envoyer une requête de suppression avec un flightID falsifié.", "Le serveur doit refuser la suppression."),
            ("Vérifier l'itinéraire.", "Le vol d'origine doit être conservé et un message d'erreur affiché."),
        ],
        "actual": "Message « database synchronization error » et réservation conservée.",
    },
    {
        "id": "RSVI-ET-02",
        "module": "RSVI",
        "type": "ET",
        "summary": "Affichage de l'itinéraire sans aucune réservation",
        "priority": "Medium",
        "automated": "test_rsvi_itinerary.py::test_rsvi_et_02_sans_reservation",
        "status": "Passé",
        "preconditions": ["L'utilisateur est connecté avec un compte sans réservation."],
        "data": [],
        "steps": [
            ("Cliquer sur Itinerary.", "Le message « No flights have been reserved » s'affiche sans erreur."),
        ],
        "actual": "Message affiché correctement.",
    },
    {
        "id": "RSVI-ET-03",
        "module": "RSVI",
        "type": "ET",
        "summary": "Double suppression de tous les vols",
        "priority": "Low",
        "automated": "test_rsvi_itinerary.py::test_rsvi_et_03_double_suppression",
        "status": "Passé",
        "preconditions": ["L'utilisateur possède une réservation."],
        "data": [],
        "steps": [
            ("Cliquer une première fois sur Cancel All Reservations.", "L'itinéraire est vidé."),
            ("Cliquer une seconde fois sur Cancel All Reservations.", "Le système reste stable et affiche un itinéraire vide."),
        ],
        "actual": "Aucune erreur, itinéraire vide.",
    },
    {
        "id": "RSVI-BT-01",
        "module": "RSVI",
        "type": "BT",
        "summary": "Itinéraire avec un seul passager",
        "priority": "Medium",
        "automated": "test_rsvi_itinerary.py::test_rsvi_bt_01_un_passager",
        "status": "Passé",
        "preconditions": ["L'utilisateur est connecté."],
        "data": ["numPassengers = 1"],
        "steps": [
            ("Réserver un vol pour 1 passager.", "La réservation est enregistrée."),
            ("Ouvrir l'itinéraire.", "Un seul billet est affiché et le total correspond à 1 passager."),
        ],
        "actual": "Un billet affiché.",
    },
    {
        "id": "RSVI-BT-02",
        "module": "RSVI",
        "type": "BT",
        "summary": "Itinéraire avec huit passagers (limite de l'interface)",
        "priority": "Medium",
        "automated": "test_rsvi_itinerary.py::test_rsvi_bt_02_8_passagers",
        "status": "Passé",
        "preconditions": ["L'utilisateur est connecté."],
        "data": ["numPassengers = 8"],
        "steps": [
            ("Réserver un vol pour 8 passagers.", "Huit champs de nom de passager sont affichés."),
            ("Ouvrir l'itinéraire.", "Le total est multiplié par 8 et les 8 passagers sont enregistrés."),
        ],
        "actual": "Réservation pour 8 passagers affichée.",
    },
    {
        "id": "RSVI-BT-03",
        "module": "RSVI",
        "type": "BT",
        "summary": "Suppression du dernier vol de l'itinéraire",
        "priority": "Medium",
        "automated": "test_rsvi_itinerary.py::test_rsvi_bt_03_dernier_vol",
        "status": "Passé",
        "preconditions": ["L'utilisateur possède exactement une réservation."],
        "data": [],
        "steps": [
            ("Ouvrir l'itinéraire.", "Un vol est affiché."),
            ("Cocher le vol et cliquer sur Cancel Reservation.", "L'itinéraire devient vide sans erreur."),
        ],
        "actual": "Dernier vol supprimé, itinéraire vide.",
    },
    {
        "id": "RSVI-PT-01",
        "module": "RSVI",
        "type": "PT",
        "summary": "Accès à l'itinéraire d'un autre utilisateur (cookie forgé)",
        "priority": "Critical",
        "automated": "test_rsvi_itinerary.py::test_rsvi_pt_01_idor",
        "status": "Échoué – BUG-04",
        "bug": "BUG-04",
        "preconditions": ["Aucune authentification.", "Le compte admin existe."],
        "data": ["Cookie MTUserInfo = username&admin&hash&78"],
        "steps": [
            ("Envoyer une requête GET /cgi-bin/itinerary.pl avec le cookie MTUserInfo forgé pour admin.", "Le serveur doit refuser l'accès ou retourner uniquement les données de la session authentifiée."),
            ("Lire la réponse.", "Aucune donnée d'un autre utilisateur ne doit être exposée."),
        ],
        "actual": "L'itinéraire complet de admin (nom, adresse, carte masquée, vols) est affiché.",
    },
    {
        "id": "RSVI-PT-02",
        "module": "RSVI",
        "type": "PT",
        "summary": "Accès direct à itinerary.pl sans session",
        "priority": "High",
        "automated": "test_rsvi_itinerary.py::test_rsvi_pt_02_acces_sans_session",
        "status": "Échoué – BUG-02",
        "bug": "BUG-02",
        "preconditions": ["Aucune session utilisateur."],
        "data": ["URL = /cgi-bin/itinerary.pl"],
        "steps": [
            ("Ouvrir directement l'URL de l'itinéraire.", "L'application doit rediriger vers le login."),
        ],
        "actual": "Page Itinerary affichée avec « No flights have been reserved ».",
    },
    {
        "id": "RSVI-PT-03",
        "module": "RSVI",
        "type": "PT",
        "summary": "Suppression de vols sans session authentifiée",
        "priority": "High",
        "automated": "test_rsvi_itinerary.py::test_rsvi_pt_03_suppression_sans_session",
        "status": "Échoué – BUG-02",
        "bug": "BUG-02",
        "preconditions": ["Aucune session utilisateur."],
        "data": ["POST removeAllFlights.x=1"],
        "steps": [
            ("Envoyer directement une requête POST de suppression sans cookie de session.", "Le serveur doit refuser la requête (401/403)."),
        ],
        "actual": "La requête est traitée et retourne une page Itinerary vide.",
    },
]


def md_escape(text: str) -> str:
    return text.replace("|", "\\|")


def write_markdown(test: dict) -> Path:
    mod = MODULES[test["module"]]
    typ = TYPES[test["type"]]
    out_dir = MANUAL / mod["folder"] / typ["folder"]
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"{test['id']}.md"

    status = test["status"]
    bug = test.get("bug")
    status_line = f"**Statut : {status}**"
    if bug:
        status_line += f" — voir `docs/04_Bugs_Detectes.md#{bug.lower()}`"

    lines = [
        f"# {test['id']} – {test['summary']}",
        "",
        "| Champ | Valeur |",
        "|---|---|",
        f"| Module | {mod['name']} |",
        f"| Type | {typ['name']} |",
        f"| Priorité | {test['priority']} |",
        f"| User Story | {mod['story']} |",
        f"| Test automatisé | `{test['automated']}` |",
        f"| Tags | WebTours, {test['module']}, {test['type']}, {test['id']} |",
        "",
        status_line,
        "",
        "## Préconditions",
        "",
    ]
    if test["preconditions"]:
        lines += [f"- {p}" for p in test["preconditions"]]
    else:
        lines.append("- Aucune.")
    lines += ["", "## Données de test", ""]
    if test["data"]:
        lines += [f"- `{d}`" for d in test["data"]]
    else:
        lines.append("- Aucune donnée spécifique.")
    lines += ["", "## Étapes et résultats attendus", "", "| # | Action | Résultat attendu |", "|---|---|---|"]
    for i, (action, expected) in enumerate(test["steps"], 1):
        lines.append(f"| {i} | {md_escape(action)} | {md_escape(expected)} |")
    lines += ["", "## Résultat obtenu", "", test["actual"], ""]
    if bug:
        lines += [f"> **Anomalie :** {bug}. Voir le rapport de bugs pour les détails et les preuves.", ""]
    lines += [
        "## Statut d'exécution",
        "",
        "- [x] Exécuté" if status != "À exécuter" else "- [ ] À exécuter",
        f"- [{'x' if status == 'Passé' else ' '}] Passé",
        f"- [{'x' if status.startswith('Échoué') else ' '}] Échoué",
        "- [ ] Bloqué",
        "",
        "## Notes",
        "",
        "Test exécuté sur l'environnement local WebTours (Windows, Java 8, Strawberry Perl, Apache 2.2, port 1080).",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def write_xray_csv() -> Path:
    path = XRAY / "WebTours_Xray_Import.csv"
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f, quoting=csv.QUOTE_ALL, lineterminator="\n")
        writer.writerow([
            "Issue Type", "Summary", "Description", "Test Type", "Precondition",
            "Steps", "Expected Result", "Priority", "Labels", "Folder",
        ])
        for t in TESTS:
            mod = MODULES[t["module"]]
            typ = TYPES[t["type"]]
            steps = "\n".join(f"{i}. {a}" for i, (a, _) in enumerate(t["steps"], 1))
            expected = "\n".join(f"{i}. {e}" for i, (_, e) in enumerate(t["steps"], 1))
            description = (
                f"{t['summary']}\n\n"
                f"User Story : {mod['story']}\n"
                f"Test automatisé : {t['automated']}\n"
                f"Statut constaté : {t['status']}"
            )
            labels = f"WebTours {t['module']} {t['type']} {t['id']} MANUAL-MANUAL"
            folder = f"/WebTours/{mod['folder']}/{typ['folder']}"
            writer.writerow([
                "Test",
                f"{t['id']} – {t['summary']}",
                description,
                "Manual",
                "\n".join(t["preconditions"]),
                steps,
                expected,
                t["priority"],
                labels,
                folder,
            ])
    return path


def write_user_stories_csv() -> Path:
    path = XRAY / "WebTours_UserStories.csv"
    stories = [
        ("WT-US-01", "Authentification", "En tant que visiteur, je veux me connecter avec mes identifiants afin d'accéder à mes réservations.", "High", "Connexion valide, message de bienvenue, menu utilisateur, déconnexion."),
        ("WT-US-02", "Inscription", "En tant que visiteur, je veux créer un compte afin de pouvoir réserver des vols.", "High", "Création de compte, validation des champs, confirmation du mot de passe."),
        ("WT-US-03", "Recherche et réservation de vols", "En tant que client, je veux rechercher et réserver un vol afin de planifier mon voyage.", "High", "Recherche aller simple/aller-retour, sélection, paiement, facture."),
        ("WT-US-04", "Gestion de l'itinéraire", "En tant que client, je veux consulter et supprimer mes réservations afin de gérer mon voyage.", "High", "Affichage, suppression d'un vol, suppression de tous les vols."),
        ("WT-US-05", "Déconnexion", "En tant que client, je veux me déconnecter afin de protéger mes données.", "Medium", "SignOff, retour au login, session invalidée."),
        ("WT-US-06", "Sécurité et permissions", "En tant qu'administrateur, je veux que les pages sensibles soient protégées afin d'éviter les accès non autorisés.", "Critical", "Pas d'accès sans login, pas d'IDOR, pas de falsification de prix, admin protégé."),
    ]
    with path.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f, quoting=csv.QUOTE_ALL, lineterminator="\n")
        writer.writerow(["Issue Type", "Summary", "Description", "Priority", "Labels", "Acceptance Criteria"])
        for key, title, desc, prio, ac in stories:
            writer.writerow(["Story", f"{key} – {title}", desc, prio, f"WebTours {key}", ac])
    return path


def write_bugs_csv() -> Path:
    path = XRAY / "WebTours_Bugs.csv"
    bugs = [
        ("BUG-01", "Accès non authentifié à la recherche de vols", "Critical", "RSVA", "reservations.pl?page=welcome est accessible sans login.", "Redirection vers le login.", "Formulaire Find Flight affiché."),
        ("BUG-02", "Accès non authentifié à l'itinéraire", "High", "RSVA/RSVI", "itinerary.pl est accessible sans login.", "Redirection vers le login.", "Page Itinerary vide affichée."),
        ("BUG-03", "Page d'administration accessible sans authentification", "Critical", "RSVA", "admin.pl est accessible sans login et permet de modifier les options serveur.", "401/403 ou login.", "Page Admin affichée."),
        ("BUG-04", "IDOR sur itinerary.pl via le cookie MTUserInfo", "Critical", "RSVI", "Un cookie MTUserInfo forgé permet de lire l'itinéraire de admin.", "Contrôle serveur de la session.", "Données de admin affichées."),
        ("BUG-05", "Date vide ou invalide : page blanche sans message", "High", "RSVF", "departDate vide ou 13/45/2026 provoque une page incomplète et une erreur Perl.", "Message de validation.", "Page sans formulaire ; log Month '-1' out of range."),
        ("BUG-06", "Date passée acceptée", "High", "RSVF", "Une date de départ passée est acceptée et les vols sont proposés.", "Refus avec message.", "Vols proposés pour 01/01/2020."),
        ("BUG-07", "Ville de départ = ville d'arrivée acceptée", "High", "RSVF", "Denver → Denver affiche des vols à 0 $.", "Refus avec message.", "Quatre vols à 0 $."),
        ("BUG-08", "Nombre de passagers non validé (0, négatif, 999)", "High", "RSVF", "Le nombre de passagers n'est pas contrôlé côté serveur.", "1 ≤ passagers ≤ maximum.", "0, -1, abc et 999 acceptés."),
        ("BUG-09", "Prix manipulable dans le POST", "Critical", "RSVF", "Le prix envoyé dans outboundFlight est utilisé pour la facture.", "Prix recalculé côté serveur.", "Facture de 1 $ au lieu de 350 $."),
        ("BUG-10", "Falsification du flightID et achat direct", "Critical", "RSVF", "Un vol inexistant (999) et un POST buyFlights direct sont acceptés.", "Validation du vol et du parcours.", "Facture générée pour un vol inexistant."),
        ("BUG-11", "Politique de mot de passe absente", "Medium", "RSVA", "Un mot de passe d'un caractère est accepté.", "Longueur et complexité minimales.", "Compte créé avec 'a'."),
        ("BUG-12", "Normalisation silencieuse du username", "High", "RSVA", "jojo! est accepté comme jojo ; la casse est ignorée sous Windows.", "Comparaison exacte.", "Connexion réussie avec jojo!."),
        ("BUG-13", "Mots de passe stockés en clair", "Critical", "RSVA", "Les fichiers utilisateurs contiennent le mot de passe en clair.", "Hachage salé.", "Lecture directe du fichier users/jojo."),
        ("BUG-14", "Absence de validation de la carte bancaire", "High", "RSVF", "Une carte vide et une date d'expiration vide sont acceptées.", "Validation carte/expiration.", "Facture générée avec une carte vide."),
        ("BUG-15", "Absence de jetons anti-CSRF", "Medium", "Tous", "Les formulaires de réservation/suppression ne contiennent pas de jeton CSRF.", "Jeton CSRF par formulaire.", "Suppression de vols via une requête POST forgée."),
    ]
    with path.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f, quoting=csv.QUOTE_ALL, lineterminator="\n")
        writer.writerow(["Issue Type", "Summary", "Priority", "Labels", "Description", "Expected Result", "Actual Result"])
        for key, title, prio, module, desc, exp, act in bugs:
            writer.writerow(["Bug", f"{key} – {title}", prio, f"WebTours {module} BUG", desc, exp, act])
    return path


def main() -> None:
    for t in TESTS:
        write_markdown(t)
    xray = write_xray_csv()
    stories = write_user_stories_csv()
    bugs = write_bugs_csv()
    print(f"{len(TESTS)} fiches générées dans {MANUAL}")
    print(f"Import Xray : {xray}")
    print(f"User stories : {stories}")
    print(f"Bugs : {bugs}")


if __name__ == "__main__":
    main()
