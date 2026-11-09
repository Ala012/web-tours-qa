# RSVF-FT-02 – Recherche d'un vol aller-retour

| Champ | Valeur |
|---|---|
| Module | RSVF – Vols |
| Type | FT – Functional Testing |
| Priorité | High |
| User Story | WT-US-03 |
| Test automatisé | `test_rsvf_flight.py::test_rsvf_ft_02_recherche_aller_retour` |
| Tags | WebTours, RSVF, FT, RSVF-FT-02 |

**Statut : Passé**

## Préconditions

- L'utilisateur jojo est connecté.

## Données de test

- `depart = Denver`
- `arrive = Paris`
- `roundtrip = coché`

## Étapes et résultats attendus

| # | Action | Résultat attendu |
|---|---|---|
| 1 | Ouvrir le formulaire Find Flight. | Le formulaire s'affiche. |
| 2 | Cocher Roundtrip ticket et lancer la recherche. | Les vols aller et les vols retour sont affichés. |

## Résultat obtenu

Les deux groupes de vols (outboundFlight et returnFlight) sont affichés.

## Statut d'exécution

- [x] Exécuté
- [x] Passé
- [ ] Échoué
- [ ] Bloqué

## Notes

Test exécuté sur l'environnement local WebTours (Windows, Java 8, Strawberry Perl, Apache 2.2, port 1080).
