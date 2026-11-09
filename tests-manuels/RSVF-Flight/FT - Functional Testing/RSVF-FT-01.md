# RSVF-FT-01 – Recherche d'un vol aller simple Denver → Paris

| Champ | Valeur |
|---|---|
| Module | RSVF – Vols |
| Type | FT – Functional Testing |
| Priorité | High |
| User Story | WT-US-03 |
| Test automatisé | `test_rsvf_flight.py::test_rsvf_ft_01_recherche_aller_simple` |
| Tags | WebTours, RSVF, FT, RSVF-FT-01 |

**Statut : Passé**

## Préconditions

- L'utilisateur jojo est connecté.
- La date de départ est fixée à demain.

## Données de test

- `depart = Denver`
- `arrive = Paris`
- `departDate = demain (MM/DD/YYYY)`
- `numPassengers = 1`

## Étapes et résultats attendus

| # | Action | Résultat attendu |
|---|---|---|
| 1 | Cliquer sur Flights dans le menu. | Le formulaire Find Flight s'affiche. |
| 2 | Sélectionner Denver, Paris, la date de demain et 1 passager. | Les valeurs sont sélectionnées. |
| 3 | Cliquer sur le bouton Next (findFlights). | Quatre vols (040, 041, 042, 043) sont proposés avec les horaires et les prix. |

## Résultat obtenu

Quatre vols affichés pour Denver → Paris.

## Statut d'exécution

- [x] Exécuté
- [x] Passé
- [ ] Échoué
- [ ] Bloqué

## Notes

Test exécuté sur l'environnement local WebTours (Windows, Java 8, Strawberry Perl, Apache 2.2, port 1080).
