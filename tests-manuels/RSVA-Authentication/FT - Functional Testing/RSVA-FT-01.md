# RSVA-FT-01 – Connexion avec des identifiants valides

| Champ | Valeur |
|---|---|
| Module | RSVA – Authentification |
| Type | FT – Functional Testing |
| Priorité | High |
| User Story | WT-US-01 / WT-US-02 |
| Test automatisé | `test_rsva_authentication.py::test_rsva_ft_01_login_valide` |
| Tags | WebTours, RSVA, FT, RSVA-FT-01 |

**Statut : Passé**

## Préconditions

- Le serveur WebTours est démarré sur http://127.0.0.1:1080.
- Le compte de démonstration jojo / bean existe.

## Données de test

- `username = jojo`
- `password = bean`

## Étapes et résultats attendus

| # | Action | Résultat attendu |
|---|---|---|
| 1 | Ouvrir http://127.0.0.1:1080/WebTours/index.htm. | La page Web Tours s'affiche avec le cadre de navigation et la page d'accueil. |
| 2 | Saisir jojo dans le champ Username et bean dans le champ Password. | Les deux champs sont renseignés. |
| 3 | Cliquer sur le bouton Login. | Le message « Welcome, jojo » s'affiche et le menu Flights / Itinerary / Home / SignOff apparaît. |

## Résultat obtenu

Connexion réussie, message de bienvenue affiché.

## Statut d'exécution

- [x] Exécuté
- [x] Passé
- [ ] Échoué
- [ ] Bloqué

## Notes

Test exécuté sur l'environnement local WebTours (Windows, Java 8, Strawberry Perl, Apache 2.2, port 1080).
