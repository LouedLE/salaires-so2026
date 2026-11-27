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
| Tableau de bord | app/Accueil.py, app/filtres.py | filtre_niveau |
| Axes 1 à 5 | src/salaires/axes/, app/pages/ | à compléter |
| Axe 2 : Métier et entreprise | src/salaires/axes/axe2_metier_entreprise.py, app/pages/2_metier_entreprise.py | ajouter_groupes, groupes_sous_seuil |
| Axe 5 : France face à l'Europe | src/salaires/axes/axe5_france_europe.py, app/pages/5_france_europe.py | definir_population_europe, mediane_par_pays, mediane_par_niveau, ecart_avec_france |

## Cache

- `charger_population()` (app/donnees.py) est décorée par `@st.cache_data` : elle enchaîne `charger_brut`, `definir_population` puis `ajouter_niveau`. Le résultat est calculé une fois puis réutilisé par toutes les pages.
- Axe 5 : `charger_population_europe` (page 5) met en cache la population des cinq pays.

## Données de session (`st.session_state`)

- `niveau` : niveau d'expérience choisi (Tous, Junior, Confirmé, Senior), géré par `app/filtres.py`.
  Le widget utilise la clé `_choix_niveau`, recopiée dans `niveau` à chaque changement :
  Streamlit efface les clés de widget au changement de page, pas les autres.
- Toutes les pages d'axe lisent `st.session_state.get("niveau", "Tous")`, sauf l'axe 1 (l'expérience y est la variable étudiée).
- Axe 2 : lit `st.session_state.get("niveau", "Tous")` et filtre sur la colonne `Niveau` si la valeur
  n'est pas « Tous ». Le filtre propre à l'axe (taille d'entreprise) reste dans `st.sidebar`, hors session.
