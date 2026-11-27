# Architecture technique

Document à compléter au fil du socle commun.

## Flux des données

```
data/raw/2026/survey_results_public.csv
        │  scripts/telecharger_donnees.py
        ▼
src/salaires/chargement.py      charger_brut()        colonnes utiles seulement
        │  mis en cache côté app avec @st.cache_data
        ▼
src/salaires/population.py      definir_population()  France, pros, salaire en euros
        ▼
src/salaires/logique.py         médianes, seuil n, légende de population
        ▼
src/salaires/axes/axeN_*.py     calculs propres à chaque axe
        ▼
app/Accueil.py                  tableau de bord principal, message pour le commanditaire
app/pages/N_*.py                une page par axe, filtres et vues
```

## Fonctionnalités principales

| Fonctionnalité | Fichiers | Fonctions |
|----------------|----------|-----------|
| Téléchargement des données | scripts/telecharger_donnees.py | telecharger |
| Chargement | src/salaires/chargement.py | charger_brut |
| Population | src/salaires/population.py | definir_population |
| Logique partagée | src/salaires/logique.py | mediane_par_groupe, legende_population |
| Tableau de bord | app/Accueil.py | à compléter |
| Axes 1 à 5 | src/salaires/axes/, app/pages/ | à compléter |

## Cache

- `charger_population()` (app/donnees.py) est décorée par `@st.cache_data` : elle enchaîne `charger_brut`, `definir_population` puis `ajouter_niveau`. Le résultat est calculé une fois puis réutilisé par toutes les pages.

## Données de session (`st.session_state`)

- Filtres partagés entre les pages : à compléter.
