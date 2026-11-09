# RSVA-ET-02 – Connexion avec des champs vides

| Champ | Valeur |
|---|---|
| Module | RSVA – Authentification |
| Type | ET – Error Testing |
| Priorité | Medium |
| User Story | WT-US-01 / WT-US-02 |
| Test automatisé | `test_rsva_authentication.py::test_rsva_et_02_champs_vides` |
| Tags | WebTours, RSVA, ET, RSVA-ET-02 |

**Statut : Passé**

## Préconditions

- Le formulaire de connexion est affiché.

## Données de test

- `username = (vide)`
- `password = (vide)`

## Étapes et résultats attendus

| # | Action | Résultat attendu |
|---|---|---|
| 1 | Laisser les champs Username et Password vides. | Les champs sont vides. |
| 2 | Cliquer sur Login. | Un message d'erreur est affiché et la connexion est refusée. |

## Résultat obtenu

Message « Incorrect Password » affiché.

## Statut d'exécution

- [x] Exécuté
- [x] Passé
- [ ] Échoué
- [ ] Bloqué

## Notes

Test exécuté sur l'environnement local WebTours (Windows, Java 8, Strawberry Perl, Apache 2.2, port 1080).
