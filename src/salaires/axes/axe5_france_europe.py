"""Axe 5 : France face à l'Europe. Calculs de l'axe, aucun import Streamlit ici.

Responsable : Fayssal.

Les salaires sont comparés en ConvertedCompYearly (salaire annuel converti en dollars US) :
c'est la seule unité commune entre pays qui ne déclarent pas dans la même devise.
"""

import pandas as pd

from salaires.logique import SEUIL_N
from salaires.population import NIVEAUX, ajouter_niveau

# Nom du pays dans l'enquête -> nom affiché.
PAYS = {
    "France": "France",
    "Germany": "Allemagne",
    "Netherlands": "Pays-Bas",
    "Spain": "Espagne",
    "United Kingdom of Great Britain and Northern Ireland": "Royaume-Uni",
}

DESCRIPTION = (
    "Développeurs professionnels salariés de cinq pays européens "
    "(France, Allemagne, Pays-Bas, Espagne, Royaume-Uni)"
)


def definir_population_europe(df: pd.DataFrame) -> pd.DataFrame:
    """Population de l'axe : les cinq pays, code comme activité principale, salarié, salaire en dollars renseigné.

    Ajoute les colonnes Pays (nom affiché) et Niveau.
    """
    garder = (
        df["Country"].isin(PAYS)
        & (df["CodeMain"] == "I create code as a primary part of my job")
        & (df["Employment"] == "Employed")
        & df["ConvertedCompYearly"].notna()
    )
    pop = df[garder].copy()
    pop["Pays"] = pop["Country"].map(PAYS)
    return ajouter_niveau(pop)


def mediane_par_pays(pop: pd.DataFrame) -> pd.DataFrame:
    """Salaire médian en dollars et effectif par pays, du plus bas au plus haut."""
    tableau = (
        pop.groupby("Pays")["ConvertedCompYearly"]
        .agg(mediane="median", n="count")
        .reset_index()
        .sort_values("mediane")
    )
    tableau["fiable"] = tableau["n"] >= SEUIL_N
    return tableau
