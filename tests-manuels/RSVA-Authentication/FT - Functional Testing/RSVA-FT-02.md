# RSVA-FT-02 – Déconnexion de l'utilisateur (Sign Off)

| Champ | Valeur |
|---|---|
| Module | RSVA – Authentification |
| Type | FT – Functional Testing |
| Priorité | High |
| User Story | WT-US-01 / WT-US-02 |
| Test automatisé | `test_rsva_authentication.py::test_rsva_ft_02_deconnexion` |
| Tags | WebTours, RSVA, FT, RSVA-FT-02 |

**Statut : Passé**

## Préconditions

- L'utilisateur jojo est connecté.

## Données de test

- Aucune donnée spécifique.

## Étapes et résultats attendus

| # | Action | Résultat attendu |
|---|---|---|
| 1 | Cliquer sur le bouton SignOff du menu de navigation. | Le cadre de navigation revient au formulaire de connexion. |
| 2 | Vérifier la page d'accueil. | Le message de bienvenue et les liens réservés aux utilisateurs connectés ne sont plus accessibles. |

## Résultat obtenu

Déconnexion effectuée, retour au formulaire de login.

## Statut d'exécution

- [x] Exécuté
- [x] Passé
- [ ] Échoué
- [ ] Bloqué

## Notes

Test exécuté sur l'environnement local WebTours (Windows, Java 8, Strawberry Perl, Apache 2.2, port 1080).
