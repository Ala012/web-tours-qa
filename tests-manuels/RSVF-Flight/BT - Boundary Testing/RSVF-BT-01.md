# RSVF-BT-01 – Recherche avec le nombre minimum de passagers (1)

| Champ | Valeur |
|---|---|
| Module | RSVF – Vols |
| Type | BT – Boundary Testing |
| Priorité | Medium |
| User Story | WT-US-03 |
| Test automatisé | `test_rsvf_flight.py::test_rsvf_bt_01_un_passager` |
| Tags | WebTours, RSVF, BT, RSVF-BT-01 |

**Statut : Passé**

## Préconditions

- Le formulaire Find Flight est affiché.

## Données de test

- `numPassengers = 1`

## Étapes et résultats attendus

| # | Action | Résultat attendu |
|---|---|---|
| 1 | Saisir 1 passager et lancer la recherche. | Quatre vols sont affichés et le total correspond à 1 billet. |

## Résultat obtenu

Recherche acceptée avec 1 passager.

## Statut d'exécution

- [x] Exécuté
- [x] Passé
- [ ] Échoué
- [ ] Bloqué

## Notes

Test exécuté sur l'environnement local WebTours (Windows, Java 8, Strawberry Perl, Apache 2.2, port 1080).
