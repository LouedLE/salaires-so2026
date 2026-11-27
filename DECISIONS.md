# Décisions

Chaque choix est daté et justifié. Les chiffres viennent du fichier, pas de la restitution officielle.

## Commanditaire et message

- Commanditaire : la direction de la rémunération d'une ESN qui révise sa grille salariale.

### Message

Trois constats les plus nets de l'exploration (`notebooks/exploration_fayssal.ipynb`, 27/11/2026).
Population : France, code comme activité principale, salarié, salaire déclaré en euros
entre 15 000 et 200 000 €, soit 371 répondants. Salaire médian 53 000 €,
1er quartile 42 000 €, 3e quartile 70 000 €.

1. Le salaire suit l'expérience : médiane de 38 315 € pour les juniors (n = 56),
   48 000 € pour les confirmés (n = 107) et 62 000 € pour les seniors (n = 207), soit +62 % entre junior et senior.
2. Les ESN paient moins que les éditeurs de logiciels : 44 500 € (n = 66) contre 53 000 € (n = 65),
   soit 16 % de moins. L'expérience médiane est comparable (10,5 ans contre 10), l'écart ne vient donc pas de là.
   Ce sont les deux seuls secteurs au-dessus du seuil de 30 répondants.
3. Le télétravail complet est le mieux payé : 65 000 € en télétravail (n = 65) contre 41 394 € en présentiel (n = 44).
   Écart à nuancer : 45 % des répondants en présentiel sont juniors, contre 6 % en télétravail.

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

Code : `definir_population` dans `src/salaires/population.py`. Filtres appliqués dans cet ordre,
comptés sur `survey_results_public.csv` 2026.

| # | Filtre | Avant | Après | Justification |
|---|--------|------:|------:|---------------|
| 1 | `Country == "France"` | 30 903 | 794 | Grille salariale d'une ESN française. |
| 2 | `CodeMain == "I create code as a primary part of my job"` | 794 | 628 | Garder les développeurs, pas les managers ni ceux qui codent occasionnellement. |
| 3 | `Employment == "Employed"` | 628 | 463 | Salariés seulement : les freelances (96 en France) facturent un chiffre d'affaires, pas un salaire. |
| 4 | `Currency` commence par `"EUR"` | 463 | 454 | Comparer des montants dans la même monnaie, sans taux de change. |
| 5 | `Compensation` renseigné | 454 | 382 | Pas de salaire, pas de médiane possible. |
| 6 | `SalaireEUR` entre 15 000 et 200 000 € inclus | 382 | 371 | Valeurs aberrantes (voir ci-dessous). |

- `SalaireEUR = Compensation` : montant annuel déclaré en euros, plutôt que `ConvertedCompYearly`
  (converti en dollars, dépend du taux de change).
- Bornes : sur les 382 lignes avant bornes, le 2e centile vaut 15 050 € et le 99e 191 900 €.
  15 000 € est sous le SMIC annuel brut à temps plein : en dessous, il s'agit d'un salaire mensuel
  ou d'une saisie erronée (minimum observé 54 €). 200 000 € écarte les quelques montants
  très au-dessus du marché (maximum 320 000 €). 8 lignes retirées en bas, 3 en haut.
- Salaire médian de la population finale : 53 000 € (n = 371), identique à celui avant bornes.
- Limite : `Employment = "Employed"` ne distingue pas temps plein et temps partiel en 2026.

## Niveaux d'expérience (27/11/2026)

- Colonne `Niveau`, calculée par `ajouter_niveau` (`src/salaires/population.py`) à partir de `WorkExp`
  (années d'expérience professionnelle) : Junior de 0 à 4 ans, Confirmé de 5 à 9 ans, Senior 10 ans et plus.
- Premier découpage écarté : « moins de 3 ans » ne donnait que 22 juniors, sous le seuil de 30.
- Effectifs sur la population (France, code comme activité principale, salarié, salaire en euros
  entre 15 000 et 200 000 €, 371 répondants) : 56 juniors, 107 confirmés, 207 seniors.
- Le répondant sans `WorkExp` reste dans la population avec un `Niveau` vide :
  il compte dans « Tous » mais dans aucun niveau.
