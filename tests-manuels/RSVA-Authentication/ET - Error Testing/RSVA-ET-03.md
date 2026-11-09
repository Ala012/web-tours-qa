# RSVA-ET-03 – Création de compte avec confirmation du mot de passe différente

| Champ | Valeur |
|---|---|
| Module | RSVA – Authentification |
| Type | ET – Error Testing |
| Priorité | Medium |
| User Story | WT-US-01 / WT-US-02 |
| Test automatisé | `test_rsva_authentication.py::test_rsva_et_03_confirmation_differente` |
| Tags | WebTours, RSVA, ET, RSVA-ET-03 |

**Statut : Passé**

## Préconditions

- Le formulaire Customer Profile est affiché.

## Données de test

- `password = Passw0rd!`
- `passwordConfirm = AutrePassw0rd!`

## Étapes et résultats attendus

| # | Action | Résultat attendu |
|---|---|---|
| 1 | Remplir le formulaire avec deux mots de passe différents. | Les champs sont renseignés. |
| 2 | Cliquer sur register. | Le message « Your password is invalid. Please re-enter it and it's confirmation. » s'affiche et aucun compte n'est créé. |

## Résultat obtenu

Création refusée avec message d'erreur.

## Statut d'exécution

- [x] Exécuté
- [x] Passé
- [ ] Échoué
- [ ] Bloqué

## Notes

Test exécuté sur l'environnement local WebTours (Windows, Java 8, Strawberry Perl, Apache 2.2, port 1080).
