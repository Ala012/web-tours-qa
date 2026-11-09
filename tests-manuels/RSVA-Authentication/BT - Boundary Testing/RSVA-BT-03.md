# RSVA-BT-03 – Connexion avec des caractères spéciaux dans le nom d'utilisateur

| Champ | Valeur |
|---|---|
| Module | RSVA – Authentification |
| Type | BT – Boundary Testing |
| Priorité | High |
| User Story | WT-US-01 / WT-US-02 |
| Test automatisé | `test_rsva_authentication.py::test_rsva_bt_03_username_caracteres_speciaux` |
| Tags | WebTours, RSVA, BT, RSVA-BT-03 |

**Statut : Échoué – BUG-12** — voir `docs/04_Bugs_Detectes.md#bug-12`

## Préconditions

- Le compte jojo / bean existe.

## Données de test

- `username = jojo!`
- `password = bean`

## Étapes et résultats attendus

| # | Action | Résultat attendu |
|---|---|---|
| 1 | Saisir jojo! comme username et bean comme password. | Les champs sont renseignés. |
| 2 | Cliquer sur Login. | La connexion doit être refusée car le username saisi ne correspond pas exactement au compte jojo. |

## Résultat obtenu

La connexion réussit : les caractères non alphanumériques sont supprimés silencieusement (jojo! devient jojo).

> **Anomalie :** BUG-12. Voir le rapport de bugs pour les détails et les preuves.

## Statut d'exécution

- [x] Exécuté
- [ ] Passé
- [x] Échoué
- [ ] Bloqué

## Notes

Test exécuté sur l'environnement local WebTours (Windows, Java 8, Strawberry Perl, Apache 2.2, port 1080).
