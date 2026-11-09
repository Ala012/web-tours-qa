# RSVA-ET-01 – Connexion avec un mot de passe incorrect

| Champ | Valeur |
|---|---|
| Module | RSVA – Authentification |
| Type | ET – Error Testing |
| Priorité | High |
| User Story | WT-US-01 / WT-US-02 |
| Test automatisé | `test_rsva_authentication.py::test_rsva_et_01_mot_de_passe_incorrect` |
| Tags | WebTours, RSVA, ET, RSVA-ET-01 |

**Statut : Passé**

## Préconditions

- Le compte jojo / bean existe.

## Données de test

- `username = jojo`
- `password = mauvais_mot_de_passe`

## Étapes et résultats attendus

| # | Action | Résultat attendu |
|---|---|---|
| 1 | Saisir jojo et un mot de passe erroné. | Les champs sont renseignés. |
| 2 | Cliquer sur Login. | La page « Web Tours Error - Incorrect Password » s'affiche et l'utilisateur n'est pas connecté. |

## Résultat obtenu

Message d'erreur affiché, accès refusé.

## Statut d'exécution

- [x] Exécuté
- [x] Passé
- [ ] Échoué
- [ ] Bloqué

## Notes

Test exécuté sur l'environnement local WebTours (Windows, Java 8, Strawberry Perl, Apache 2.2, port 1080).
