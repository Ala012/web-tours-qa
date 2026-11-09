# RSVA-BT-01 – Nom d'utilisateur à la limite haute de 14 caractères

| Champ | Valeur |
|---|---|
| Module | RSVA – Authentification |
| Type | BT – Boundary Testing |
| Priorité | Medium |
| User Story | WT-US-01 / WT-US-02 |
| Test automatisé | `test_rsva_authentication.py::test_rsva_bt_01_username_14_caracteres` |
| Tags | WebTours, RSVA, BT, RSVA-BT-01 |

**Statut : Passé**

## Préconditions

- Le formulaire Customer Profile est affiché.

## Données de test

- `username = qa123456789012 (14 caractères)`

## Étapes et résultats attendus

| # | Action | Résultat attendu |
|---|---|---|
| 1 | Saisir un username alphanumérique de 14 caractères. | Le champ accepte les 14 caractères. |
| 2 | Compléter le formulaire et cliquer sur register. | Le compte est créé et le message de bienvenue s'affiche. |

## Résultat obtenu

Compte de 14 caractères accepté.

## Statut d'exécution

- [x] Exécuté
- [x] Passé
- [ ] Échoué
- [ ] Bloqué

## Notes

Test exécuté sur l'environnement local WebTours (Windows, Java 8, Strawberry Perl, Apache 2.2, port 1080).
