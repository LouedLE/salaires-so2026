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

## Population

- À compléter : chaque filtre avec le nombre de lignes avant et après.

## Niveaux d'expérience (27/11/2026)

- Colonne `Niveau`, calculée par `ajouter_niveau` (`src/salaires/population.py`) à partir de `WorkExp`
  (années d'expérience professionnelle) : Junior de 0 à 4 ans, Confirmé de 5 à 9 ans, Senior 10 ans et plus.
- Premier découpage écarté : « moins de 3 ans » ne donnait que 22 juniors, sous le seuil de 30.
- Effectifs sur la population (France, code comme activité principale, salarié, salaire en euros
  entre 15 000 et 200 000 €, 371 répondants) : 56 juniors, 107 confirmés, 207 seniors.
- Le répondant sans `WorkExp` reste dans la population avec un `Niveau` vide :
  il compte dans « Tous » mais dans aucun niveau.
