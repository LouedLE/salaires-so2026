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

## Axe 2 : métier et entreprise (27/11/2026)

Code : `ajouter_groupes` dans `src/salaires/axes/axe2_metier_entreprise.py`.
Effectifs et médianes sur la population de 371 répondants.

### Familles de métier (`Role` → `Famille`)

Seuls trois métiers dépassent 30 répondants. Les autres sont réunis pour ne pas perdre 134 personnes.

| `Role` | Famille | n | Médiane |
|--------|---------|--:|--------:|
| Developer, full-stack | Développeur full-stack | 149 | 49 000 € |
| Developer, back-end | Développeur back-end | 57 | 58 000 € |
| Architect, software or solutions | Architecte | 31 | 72 000 € |
| Toutes les autres valeurs (26 métiers) | Autres profils de développement | 134 | 53 250 € |

- Les effectifs 153 / 60 / 31 cités plus haut sont comptés avant les bornes de salaire (382 répondants).
- La famille « Autres » est hétérogène (bureau, embarqué, DevOps, IA, mais aussi 6 engineering managers
  et 8 chercheurs) : sa médiane ne décrit pas un métier.

### Responsabilité (`ICorPM` → `Responsabilite`)

| `ICorPM` | Groupe | n | Médiane |
|----------|--------|--:|--------:|
| Individual contributor | Contributeur | 209 | 48 000 € |
| Individual contributor in a senior or staff-level role | Contributeur senior | 111 | 64 000 € |
| Both people manager and individual contributor + People manager | Manager | 49 (46 + 3) | 60 000 € |

- « People manager » seul ne compte que 3 répondants : regroupé avec les managers qui codent encore.
- 2 répondants sans réponse : hors groupes.

### Taille d'entreprise (`OrgSize` → `TailleEntreprise`)

| `OrgSize` | Classe | n | Médiane |
|-----------|--------|--:|--------:|
| Less than 20 + 20 to 99 employees | Moins de 100 | 151 (60 + 91) | 52 000 € |
| 100 to 499 + 500 to 999 employees | 100 à 999 | 104 (70 + 34) | 55 000 € |
| 1,000 to 4,999 + 5,000 to 9,999 employees | 1 000 à 9 999 | 62 (50 + 12) | 52 890 € |
| 10,000 or more employees | 10 000 et plus | 52 | 55 000 € |

- Exclus : « I don't know » (1) et « Just me - I am a freelancer » (1, incohérent avec un salarié).
  Les lignes restent dans la population avec une classe vide.
- 4 classes plutôt que 7 : « 5 000 à 9 999 » seule n'a que 12 répondants.
- Classes ordonnées (catégorie pandas) pour garder l'ordre des tailles sur les graphiques.

### Présentation sur la page (validé par le chef de projet, 27/11/2026)

- « Autres profils de développement » reste sur le graphique des métiers, en gris, avec la mention
  « groupe hétérogène (desktop, DevOps, embarqué, IA, recherche...), médiane non interprétable comme un métier ».
  Il n'est jamais cité dans le message. Le retirer ferait disparaître 134 répondants sur 371 sans le dire.
- Le message de la page porte sur la responsabilité : 48 000 € pour un contributeur, 64 000 € pour un contributeur senior.
- À expérience égale, l'écart se réduit sans disparaître : chez les seniors (10 ans et plus), 67 750 € pour un
  contributeur senior (n = 86) contre 58 000 € pour un contributeur (n = 81), soit 9 750 € au lieu de 16 000 €.
  Une partie de l'écart global vient donc de l'expérience.
- La figure sur la taille d'entreprise est gardée et présentée comme un constat : la taille de l'entreprise
  ne change presque pas le salaire (52 000 à 55 000 €). Un résultat nul reste une information utile pour l'ESN.
