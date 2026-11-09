# RSVF-PT-01 – Manipulation du prix dans la requête POST

| Champ | Valeur |
|---|---|
| Module | RSVF – Vols |
| Type | PT – Permission Testing |
| Priorité | Critical |
| User Story | WT-US-03 |
| Test automatisé | `test_rsvf_flight.py::test_rsvf_pt_01_prix_modifie_post` |
| Tags | WebTours, RSVF, PT, RSVF-PT-01 |

**Statut : Échoué – BUG-09** — voir `docs/04_Bugs_Detectes.md#bug-09`

## Préconditions

- L'utilisateur est connecté.
- Un vol Denver → Paris est recherché.

## Données de test

- `outboundFlight original = 040;350;11/10/2026`
- `outboundFlight modifié = 040;1;11/10/2026`

## Étapes et résultats attendus

| # | Action | Résultat attendu |
|---|---|---|
| 1 | Intercepter la requête POST reserveFlights. | La requête contient le prix du vol. |
| 2 | Remplacer 350 par 1 dans le champ outboundFlight et soumettre. | Le serveur doit recalculer le prix ou refuser la requête. |
| 3 | Finaliser le paiement. | Le montant facturé doit être le prix réel du vol (350 $). |

## Résultat obtenu

Le serveur fait confiance au prix envoyé : la facture est de 1 $.

> **Anomalie :** BUG-09. Voir le rapport de bugs pour les détails et les preuves.

## Statut d'exécution

- [x] Exécuté
- [ ] Passé
- [x] Échoué
- [ ] Bloqué

## Notes

Test exécuté sur l'environnement local WebTours (Windows, Java 8, Strawberry Perl, Apache 2.2, port 1080).
