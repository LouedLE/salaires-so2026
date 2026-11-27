"""Logique partagée par tous les axes. Aucun import Streamlit ici."""

import pandas as pd

from salaires.population import DESCRIPTION

SEUIL_N = 30


def mediane_par_groupe(
    df: pd.DataFrame, colonne: str, valeur: str = "SalaireEUR"
) -> pd.DataFrame:
    """Médiane et effectif par groupe, sans les groupes sous SEUIL_N."""
    stats = (
        df.groupby(colonne)[valeur]
        .agg(mediane="median", n="count")
        .reset_index()
    )
    return stats[stats["n"] >= SEUIL_N].reset_index(drop=True)


def legende_population(
    n: int, annee: int = 2026, description: str = DESCRIPTION
) -> str:
    """Légende affichée sous chaque figure : qui, quelle enquête, combien."""
    return f"{description}, enquête Stack Overflow {annee}, n = {n} répondants"


def eclater_choix_multiples(df: pd.DataFrame, colonne: str) -> pd.DataFrame:
    """Une ligne par choix pour une colonne dont les valeurs sont séparées par ';'."""
    eclate = df.dropna(subset=[colonne]).copy()
    eclate[colonne] = eclate[colonne].str.split(";")
    eclate = eclate.explode(colonne)
    eclate[colonne] = eclate[colonne].str.strip()
    return eclate.reset_index(drop=True)
