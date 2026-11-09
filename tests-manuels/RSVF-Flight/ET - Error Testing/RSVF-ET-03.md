# RSVF-ET-03 – Recherche avec la ville de départ identique à la ville d'arrivée

| Champ | Valeur |
|---|---|
| Module | RSVF – Vols |
| Type | ET – Error Testing |
| Priorité | Medium |
| User Story | WT-US-03 |
| Test automatisé | `test_rsvf_flight.py::test_rsvf_et_03_meme_ville` |
| Tags | WebTours, RSVF, ET, RSVF-ET-03 |

**Statut : Échoué – BUG-07** — voir `docs/04_Bugs_Detectes.md#bug-07`

## Préconditions

- Le formulaire Find Flight est affiché.

## Données de test

- `depart = Denver`
- `arrive = Denver`

## Étapes et résultats attendus

| # | Action | Résultat attendu |
|---|---|---|
| 1 | Sélectionner Denver pour le départ et Denver pour l'arrivée. | Les deux listes affichent Denver. |
| 2 | Cliquer sur Next (findFlights). | La recherche doit être refusée avec un message explicite. |

## Résultat obtenu

Quatre vols fictifs Denver → Denver sont proposés à 0 $.

> **Anomalie :** BUG-07. Voir le rapport de bugs pour les détails et les preuves.

## Statut d'exécution

- [x] Exécuté
- [ ] Passé
- [x] Échoué
- [ ] Bloqué

## Notes

Test exécuté sur l'environnement local WebTours (Windows, Java 8, Strawberry Perl, Apache 2.2, port 1080).
