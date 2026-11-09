# RSVA-FT-03 – Création d'un nouveau compte client (Sign Up)

| Champ | Valeur |
|---|---|
| Module | RSVA – Authentification |
| Type | FT – Functional Testing |
| Priorité | High |
| User Story | WT-US-01 / WT-US-02 |
| Test automatisé | `test_rsva_authentication.py::test_rsva_ft_03_creation_compte` |
| Tags | WebTours, RSVA, FT, RSVA-FT-03 |

**Statut : Passé**

## Préconditions

- Le serveur WebTours est démarré.

## Données de test

- `username = qa<horodatage>`
- `password = Passw0rd!`
- `firstName = QA`
- `lastName = User`

## Étapes et résultats attendus

| # | Action | Résultat attendu |
|---|---|---|
| 1 | Ouvrir la page d'accueil et cliquer sur le lien « sign up now ». | Le formulaire Customer Profile s'affiche dans le cadre de droite. |
| 2 | Remplir le username, le password, la confirmation et les informations de profil. | Les champs sont acceptés. |
| 3 | Cliquer sur le bouton Next (register). | Le message « Thank you, <username>, for registering » s'affiche et l'utilisateur est connecté. |

## Résultat obtenu

Compte créé et connexion automatique.

## Statut d'exécution

- [x] Exécuté
- [x] Passé
- [ ] Échoué
- [ ] Bloqué

## Notes

Test exécuté sur l'environnement local WebTours (Windows, Java 8, Strawberry Perl, Apache 2.2, port 1080).
