# Salaires des développeurs en France : enquête Stack Overflow 2026

Application Streamlit d'analyse des salaires des développeurs en France,
réalisée pour une ESN qui révise sa grille salariale.

Projet final du module Data visualisation, ECE ING4.

## Lancer l'application depuis un clone neuf

Prérequis : Python 3.11 ou plus, [uv](https://docs.astral.sh/uv/), Git.

```bash
git clone <URL_DU_DEPOT>
cd salaires-so2026
uv sync
uv run python scripts/telecharger_donnees.py
uv run streamlit run app/Accueil.py
```

Pour la comparaison avec 2025 (optionnelle) :

```bash
uv run python scripts/telecharger_donnees.py --annee 2025
```

Les données ne sont pas versionnées. Elles sont téléchargées dans `data/raw/`.

## Organisation du dépôt

- `app/` : interface Streamlit (tableau de bord principal et une page par axe)
- `src/salaires/` : chargement, population, logique partagée et calculs des axes, sans Streamlit
- `scripts/` : téléchargement des données
- `notebooks/` : explorations, un notebook par membre
- `ARCHITECTURE.md` : fonctionnalités, fichiers, flux de données, cache et session
- `DECISIONS.md` : choix et justifications
- `HARMONISATION.md` : correspondance 2025 / 2026, si la comparaison est faite

## Équipe et axes

Chef de projet : Louis-Edouard.

| Axe | Sujet | Responsable |
|-----|-------|-------------|
| 1 | Expérience | Louis-Edouard |
| 2 | Métier et entreprise | Pierre |
| 3 | Technologies | Yann |
| 4 | Conditions de travail et secteur | Arthur |
| 5 | France face à l'Europe | Fayssal |

Socle commun :

| Brique | Fichiers | Responsable |
|--------|----------|-------------|
| Chargement et cache | src/salaires/chargement.py, app/donnees.py | Arthur |
| Population | src/salaires/population.py (definir_population) | Pierre |
| Niveaux d'expérience et exploration | src/salaires/population.py (ajouter_niveau), notebooks/exploration_fayssal.ipynb | Fayssal |
| Logique partagée et légende des figures | src/salaires/logique.py, app/composants.py | Yann |
| Tableau de bord et filtre partagé | app/Accueil.py, app/filtres.py | Louis-Edouard |

## Règles de travail

- Une branche par axe (`axe-1` à `axe-5`), fusion dans `main` par Pull Request.
- Chaque figure affiche sa population : qui, quelle année, combien de répondants.
- Aucune médiane affichée sous le seuil défini dans `src/salaires/logique.py`.
- Sorties des notebooks vidées avant chaque commit (`uv run nbstripout --install` une fois).
