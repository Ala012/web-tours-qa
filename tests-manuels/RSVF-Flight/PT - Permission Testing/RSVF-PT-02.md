# RSVF-PT-02 – Falsification de l'identifiant de vol (flightID)

| Champ | Valeur |
|---|---|
| Module | RSVF – Vols |
| Type | PT – Permission Testing |
| Priorité | Critical |
| User Story | WT-US-03 |
| Test automatisé | `test_rsvf_flight.py::test_rsvf_pt_02_flightid_falsifie` |
| Tags | WebTours, RSVF, PT, RSVF-PT-02 |

**Statut : Échoué – BUG-10** — voir `docs/04_Bugs_Detectes.md#bug-10`

## Préconditions

- L'utilisateur est connecté.

## Données de test

- `outboundFlight = 999;1;01/01/2027`

## Étapes et résultats attendus

| # | Action | Résultat attendu |
|---|---|---|
| 1 | Soumettre directement une réservation avec un numéro de vol inexistant (999). | Le serveur doit refuser un vol qui n'existe pas. |
| 2 | Finaliser le paiement. | Aucune facture ne doit être générée pour un vol inexistant. |

## Résultat obtenu

La facture est générée pour le vol 999 Zurich → Zurich à 1 $.

> **Anomalie :** BUG-10. Voir le rapport de bugs pour les détails et les preuves.

## Statut d'exécution

- [x] Exécuté
- [ ] Passé
- [x] Échoué
- [ ] Bloqué

## Notes

Test exécuté sur l'environnement local WebTours (Windows, Java 8, Strawberry Perl, Apache 2.2, port 1080).
