# RSVI-PT-01 – Accès à l'itinéraire d'un autre utilisateur (cookie forgé)

| Champ | Valeur |
|---|---|
| Module | RSVI – Itinéraire |
| Type | PT – Permission Testing |
| Priorité | Critical |
| User Story | WT-US-04 |
| Test automatisé | `test_rsvi_itinerary.py::test_rsvi_pt_01_idor` |
| Tags | WebTours, RSVI, PT, RSVI-PT-01 |

**Statut : Échoué – BUG-04** — voir `docs/04_Bugs_Detectes.md#bug-04`

## Préconditions

- Aucune authentification.
- Le compte admin existe.

## Données de test

- `Cookie MTUserInfo = username&admin&hash&78`

## Étapes et résultats attendus

| # | Action | Résultat attendu |
|---|---|---|
| 1 | Envoyer une requête GET /cgi-bin/itinerary.pl avec le cookie MTUserInfo forgé pour admin. | Le serveur doit refuser l'accès ou retourner uniquement les données de la session authentifiée. |
| 2 | Lire la réponse. | Aucune donnée d'un autre utilisateur ne doit être exposée. |

## Résultat obtenu

L'itinéraire complet de admin (nom, adresse, carte masquée, vols) est affiché.

> **Anomalie :** BUG-04. Voir le rapport de bugs pour les détails et les preuves.

## Statut d'exécution

- [x] Exécuté
- [ ] Passé
- [x] Échoué
- [ ] Bloqué

## Notes

Test exécuté sur l'environnement local WebTours (Windows, Java 8, Strawberry Perl, Apache 2.2, port 1080).
