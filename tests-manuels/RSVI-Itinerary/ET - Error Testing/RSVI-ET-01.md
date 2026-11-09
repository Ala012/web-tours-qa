# RSVI-ET-01 – Suppression avec un identifiant de vol invalide

| Champ | Valeur |
|---|---|
| Module | RSVI – Itinéraire |
| Type | ET – Error Testing |
| Priorité | High |
| User Story | WT-US-04 |
| Test automatisé | `test_rsvi_itinerary.py::test_rsvi_et_01_id_vol_invalide` |
| Tags | WebTours, RSVI, ET, RSVI-ET-01 |

**Statut : Passé**

## Préconditions

- L'utilisateur possède une réservation.

## Données de test

- `flightID = INVALID-ID`

## Étapes et résultats attendus

| # | Action | Résultat attendu |
|---|---|---|
| 1 | Envoyer une requête de suppression avec un flightID falsifié. | Le serveur doit refuser la suppression. |
| 2 | Vérifier l'itinéraire. | Le vol d'origine doit être conservé et un message d'erreur affiché. |

## Résultat obtenu

Message « database synchronization error » et réservation conservée.

## Statut d'exécution

- [x] Exécuté
- [x] Passé
- [ ] Échoué
- [ ] Bloqué

## Notes

Test exécuté sur l'environnement local WebTours (Windows, Java 8, Strawberry Perl, Apache 2.2, port 1080).
