# Décisions

Chaque choix est daté et justifié. Les chiffres viennent du fichier, pas de la restitution officielle.

## Commanditaire et message

- Commanditaire : la direction de la rémunération d'une ESN qui révise sa grille salariale.
- Message du tableau de bord : à écrire après l'exploration.

## Constats sur les données 2026

- `survey_results_schema.csv` 2026 décrit 30 903 répondants.
- Salaire : colonnes `Compensation` (montant déclaré, 14 447 renseignés), `Currency`,
  et `ConvertedCompYearly` (converti en dollars, 13 507 renseignés au niveau mondial).
- Le métier est dans `Role` (plus de `DevType`), le télétravail dans `WorkSetting` (plus de `RemoteWork`).
  Toute comparaison avec 2025 demande donc une table de correspondance dans HARMONISATION.md.
- France : 794 répondants, dont 560 avec un salaire renseigné (551 en euros).
- France, code comme activité principale (`CodeMain`), salarié (`Employment = Employed`),
  salaire en euros : 382 répondants, salaire médian déclaré 53 000 €.
- Valeurs aberrantes : salaires déclarés de 54 € à 7 000 000 €. Bornes à fixer et justifier.
- Conséquence : avec un seuil de 30 répondants, seuls 3 métiers passent
  (full-stack 153, back-end 60, architecte 31). Les croisements à 2 filtres sont à éviter.
- Comparaison européenne (salaire renseigné) : Allemagne 1 343, Royaume-Uni 918,
  Pays-Bas 377, Espagne 357.

## Axe 5 : France face à l'Europe (27/11/2026)

- Population propre à l'axe, définie dans `src/salaires/axes/axe5_france_europe.py` (pas dans `population.py`) :
  `Country` parmi France, Allemagne, Pays-Bas, Espagne et Royaume-Uni, code comme activité principale (`CodeMain`),
  salarié (`Employment = Employed`), `ConvertedCompYearly` renseigné. 2 516 répondants :
  Allemagne 951, Royaume-Uni 657, France 386, Pays-Bas 287, Espagne 235.
- Unité : les salaires sont comparés en `ConvertedCompYearly` (dollars US), seule unité commune entre pays.
  Les montants dépendent donc du taux de change et ne se comparent pas aux euros des autres axes
  (France : 60 276 $ ici, 53 000 € dans la population principale).
- Pas de bornes contre les valeurs aberrantes dans cet axe : on ne compare que des médianes, peu sensibles
  aux quelques salaires extrêmes déclarés (jusqu'à 10,6 millions de dollars au Royaume-Uni).
- Salaires médians : France 60 276 $, Espagne 62 550 $, Pays-Bas 77 335 $, Allemagne 81 884 $, Royaume-Uni 93 098 $.
- Limite affichée sur la page : salaire brut, sans prise en compte du coût de la vie ni des cotisations sociales,
  très différentes entre ces pays.
- Écart par niveau d'expérience : mêmes niveaux que `ajouter_niveau` (Junior, Confirmé, Senior).
  Les juniors espagnols (n = 28) sont sous le seuil de 30 : médiane et écart masqués.

## Population

- À compléter : chaque filtre avec le nombre de lignes avant et après.
