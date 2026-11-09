# RSVA-BT-02 – Mot de passe d'un seul caractère

| Champ | Valeur |
|---|---|
| Module | RSVA – Authentification |
| Type | BT – Boundary Testing |
| Priorité | Medium |
| User Story | WT-US-01 / WT-US-02 |
| Test automatisé | `test_rsva_authentication.py::test_rsva_bt_02_mot_de_passe_1_caractere` |
| Tags | WebTours, RSVA, BT, RSVA-BT-02 |

**Statut : Échoué – BUG-11** — voir `docs/04_Bugs_Detectes.md#bug-11`

## Préconditions

- Le formulaire Customer Profile est affiché.

## Données de test

- `password = a`
- `passwordConfirm = a`

## Étapes et résultats attendus

| # | Action | Résultat attendu |
|---|---|---|
| 1 | Saisir un mot de passe d'un seul caractère. | Le champ accepte la saisie. |
| 2 | Cliquer sur register. | Le système doit refuser un mot de passe trop faible (longueur minimale). |

## Résultat obtenu

Le compte est créé avec un mot de passe d'un caractère : aucune politique de complexité n'est appliquée.

> **Anomalie :** BUG-11. Voir le rapport de bugs pour les détails et les preuves.

## Statut d'exécution

- [x] Exécuté
- [ ] Passé
- [x] Échoué
- [ ] Bloqué

## Notes

Test exécuté sur l'environnement local WebTours (Windows, Java 8, Strawberry Perl, Apache 2.2, port 1080).
