"""Axe 4 : Conditions de travail et secteur. Calculs de l'axe, aucun import Streamlit ici.

Responsable : à attribuer.
"""

import pandas as pd

from salaires.logique import mediane_par_groupe

TELETRAVAIL = "Télétravail complet"
HYBRIDE = "Hybride"
SUR_SITE = "Sur site"

ESN = "ESN et conseil"
EDITEURS = "Éditeurs de logiciels"
AUTRES = "Autres secteurs"

CORRESPONDANCE_TRAVAIL = {
    "Remote": TELETRAVAIL,
    "Hybrid (some remote, leans heavy to in-person)": HYBRIDE,
    "Hybrid (some in-person, leans heavy to flexibility)": HYBRIDE,
    "Your choice (very flexible, you can come in when you want or just as needed)": HYBRIDE,
    "In-person": SUR_SITE,
}

CORRESPONDANCE_SECTEUR = {
    "IT services, consulting, systems integration, or managed services": ESN,
    "Software development": EDITEURS,
}


def regrouper_travail(df: pd.DataFrame) -> pd.DataFrame:
    """Ajoute la colonne Travail (3 groupes) à partir de WorkSetting."""
    resultat = df.copy()
    resultat["Travail"] = resultat["WorkSetting"].map(CORRESPONDANCE_TRAVAIL)
    return resultat


def regrouper_secteur(df: pd.DataFrame) -> pd.DataFrame:
    """Ajoute la colonne SecteurGroupe. Secteur non renseigné : reste vide."""
    resultat = df.copy()
    secteur = resultat["Industry"].map(CORRESPONDANCE_SECTEUR).fillna(AUTRES)
    resultat["SecteurGroupe"] = secteur.where(resultat["Industry"].notna())
    return resultat


def medianes_par_travail(df: pd.DataFrame) -> pd.DataFrame:
    """Médiane et effectif pour chacun des 3 modes de travail."""
    return mediane_par_groupe(regrouper_travail(df), "Travail")


def comparer_esn_editeurs(df: pd.DataFrame) -> pd.DataFrame:
    """Médiane et effectif pour l'ESN et les éditeurs : la figure centrale de l'axe."""
    secteurs = regrouper_secteur(df)
    retenus = secteurs[secteurs["SecteurGroupe"].isin([ESN, EDITEURS])]
    return mediane_par_groupe(retenus, "SecteurGroupe")
