# RSVF-FT-03 – Réservation et paiement d'un vol

| Champ | Valeur |
|---|---|
| Module | RSVF – Vols |
| Type | FT – Functional Testing |
| Priorité | High |
| User Story | WT-US-03 |
| Test automatisé | `test_rsvf_flight.py::test_rsvf_ft_03_reservation_paiement` |
| Tags | WebTours, RSVF, FT, RSVF-FT-03 |

**Statut : Passé**

## Préconditions

- L'utilisateur jojo est connecté.
- Un vol Denver → Paris est recherché.

## Données de test

- `Carte = 4111111111111111`
- `Expiration = 12/28`
- `Passager = Jojo Bean`

## Étapes et résultats attendus

| # | Action | Résultat attendu |
|---|---|---|
| 1 | Sélectionner le premier vol et cliquer sur Next (reserveFlights). | La page Payment Details s'affiche avec le total. |
| 2 | Remplir les informations de paiement et cliquer sur Next (buyFlights). | La page « Reservation Made! Invoice » s'affiche avec le total facturé. |

## Résultat obtenu

Réservation confirmée et facture affichée.

## Statut d'exécution

- [x] Exécuté
- [x] Passé
- [ ] Échoué
- [ ] Bloqué

## Notes

Test exécuté sur l'environnement local WebTours (Windows, Java 8, Strawberry Perl, Apache 2.2, port 1080).
