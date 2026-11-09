# RSVI-ET-02 – Affichage de l'itinéraire sans aucune réservation

| Champ | Valeur |
|---|---|
| Module | RSVI – Itinéraire |
| Type | ET – Error Testing |
| Priorité | Medium |
| User Story | WT-US-04 |
| Test automatisé | `test_rsvi_itinerary.py::test_rsvi_et_02_sans_reservation` |
| Tags | WebTours, RSVI, ET, RSVI-ET-02 |

**Statut : Passé**

## Préconditions

- L'utilisateur est connecté avec un compte sans réservation.

## Données de test

- Aucune donnée spécifique.

## Étapes et résultats attendus

| # | Action | Résultat attendu |
|---|---|---|
| 1 | Cliquer sur Itinerary. | Le message « No flights have been reserved » s'affiche sans erreur. |

## Résultat obtenu

Message affiché correctement.

## Statut d'exécution

- [x] Exécuté
- [x] Passé
- [ ] Échoué
- [ ] Bloqué

## Notes

Test exécuté sur l'environnement local WebTours (Windows, Java 8, Strawberry Perl, Apache 2.2, port 1080).
