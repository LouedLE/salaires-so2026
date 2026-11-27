"""Chargement des données brutes de l'enquête. Aucun import Streamlit ici."""

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
    chemin = RACINE / "data" / "raw" / str(annee) / "survey_results_public.csv"
    if not chemin.exists():
        raise FileNotFoundError(
            f"Fichier introuvable : {chemin}\n"
            f"Télécharge-le avec : uv run python scripts/telecharger_donnees.py --annee {annee}"
        )
    return pd.read_csv(chemin, usecols=COLONNES_UTILES, low_memory=False)
