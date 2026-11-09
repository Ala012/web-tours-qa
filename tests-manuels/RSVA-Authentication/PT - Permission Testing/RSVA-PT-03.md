# RSVA-PT-03 – Accès à la page d'administration sans authentification

| Champ | Valeur |
|---|---|
| Module | RSVA – Authentification |
| Type | PT – Permission Testing |
| Priorité | Critical |
| User Story | WT-US-01 / WT-US-02 |
| Test automatisé | `test_rsva_authentication.py::test_rsva_pt_03_admin_sans_login` |
| Tags | WebTours, RSVA, PT, RSVA-PT-03 |

**Statut : Échoué – BUG-03** — voir `docs/04_Bugs_Detectes.md#bug-03`

## Préconditions

- Aucune session administrateur n'est ouverte.

## Données de test

- `URL = /cgi-bin/admin.pl`

## Étapes et résultats attendus

| # | Action | Résultat attendu |
|---|---|---|
| 1 | Ouvrir directement l'URL admin.pl. | L'accès doit être refusé (401/403) ou rediriger vers le login. |
| 2 | Vérifier les options serveur affichées. | Aucune option de configuration ne doit être modifiable sans authentification. |

## Résultat obtenu

La page « Web Tours Admin Page » est accessible et les options serveur sont modifiables.

> **Anomalie :** BUG-03. Voir le rapport de bugs pour les détails et les preuves.

## Statut d'exécution

- [x] Exécuté
- [ ] Passé
- [x] Échoué
- [ ] Bloqué

## Notes

Test exécuté sur l'environnement local WebTours (Windows, Java 8, Strawberry Perl, Apache 2.2, port 1080).
