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
