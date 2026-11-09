# RSVI-PT-02 – Accès direct à itinerary.pl sans session

| Champ | Valeur |
|---|---|
| Module | RSVI – Itinéraire |
| Type | PT – Permission Testing |
| Priorité | High |
| User Story | WT-US-04 |
| Test automatisé | `test_rsvi_itinerary.py::test_rsvi_pt_02_acces_sans_session` |
| Tags | WebTours, RSVI, PT, RSVI-PT-02 |

**Statut : Échoué – BUG-02** — voir `docs/04_Bugs_Detectes.md#bug-02`

## Préconditions

- Aucune session utilisateur.

## Données de test

- `URL = /cgi-bin/itinerary.pl`

## Étapes et résultats attendus

| # | Action | Résultat attendu |
|---|---|---|
| 1 | Ouvrir directement l'URL de l'itinéraire. | L'application doit rediriger vers le login. |

## Résultat obtenu

Page Itinerary affichée avec « No flights have been reserved ».

> **Anomalie :** BUG-02. Voir le rapport de bugs pour les détails et les preuves.

## Statut d'exécution

- [x] Exécuté
- [ ] Passé
- [x] Échoué
- [ ] Bloqué

## Notes

Test exécuté sur l'environnement local WebTours (Windows, Java 8, Strawberry Perl, Apache 2.2, port 1080).
