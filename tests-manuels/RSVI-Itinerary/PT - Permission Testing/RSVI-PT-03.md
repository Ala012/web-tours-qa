# RSVI-PT-03 – Suppression de vols sans session authentifiée

| Champ | Valeur |
|---|---|
| Module | RSVI – Itinéraire |
| Type | PT – Permission Testing |
| Priorité | High |
| User Story | WT-US-04 |
| Test automatisé | `test_rsvi_itinerary.py::test_rsvi_pt_03_suppression_sans_session` |
| Tags | WebTours, RSVI, PT, RSVI-PT-03 |

**Statut : Échoué – BUG-02** — voir `docs/04_Bugs_Detectes.md#bug-02`

## Préconditions

- Aucune session utilisateur.

## Données de test

- `POST removeAllFlights.x=1`

## Étapes et résultats attendus

| # | Action | Résultat attendu |
|---|---|---|
| 1 | Envoyer directement une requête POST de suppression sans cookie de session. | Le serveur doit refuser la requête (401/403). |

## Résultat obtenu

La requête est traitée et retourne une page Itinerary vide.

> **Anomalie :** BUG-02. Voir le rapport de bugs pour les détails et les preuves.

## Statut d'exécution

- [x] Exécuté
- [ ] Passé
- [x] Échoué
- [ ] Bloqué

## Notes

Test exécuté sur l'environnement local WebTours (Windows, Java 8, Strawberry Perl, Apache 2.2, port 1080).
