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
| Axe 5 : France face à l'Europe | src/salaires/axes/axe5_france_europe.py, app/pages/5_france_europe.py | definir_population_europe, mediane_par_pays, mediane_par_niveau, ecart_avec_france |

## Cache

- `@st.cache_data` sur le chargement et la population : à compléter.
- Axe 5 : `charger_population_europe` (page 5) met en cache la population des cinq pays.

## Données de session (`st.session_state`)

- Filtres partagés entre les pages : à compléter.
