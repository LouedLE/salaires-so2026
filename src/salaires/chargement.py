"""Chargement des données brutes de l'enquête. Aucun import Streamlit ici.

Responsable : à attribuer (socle commun).

À implémenter :
- charger_brut(annee) : lit data/raw/<annee>/survey_results_public.csv
  avec usecols=COLONNES_UTILES pour limiter la mémoire (le fichier fait ~120 Mo).
- La mise en cache (@st.cache_data) se fait côté app/, pas ici.
"""

from pathlib import Path

import pandas as pd

RACINE = Path(__file__).resolve().parents[2]

# Noms vérifiés dans survey_results_schema.csv 2026.
COLONNES_UTILES = [
    "ResponseId",
    "CodeMain",
    "Employment",
    "Country",
    "Currency",
    "Compensation",
    "ConvertedCompYearly",
    "WorkExp",
    "YearsCode",
    "Role",
    "ICorPM",
    "OrgSize",
    "Industry",
    "WorkSetting",
    "Education",
    "Age",
    "LanguagesHaveWorkedWith",
    "AISelect",
]


def charger_brut(annee: int = 2026) -> pd.DataFrame:
    raise NotImplementedError("Socle commun : chargement à écrire")
