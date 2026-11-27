"""Axe 2 : Métier et entreprise. Calculs de l'axe, aucun import Streamlit ici.

Responsable : Pierre.

Regroupements (tables de correspondance dans DECISIONS.md) :
- Famille : Role en familles d'au moins SEUIL_N répondants.
- Responsabilite : ICorPM en 3 groupes.
- TailleEntreprise : OrgSize en 4 classes, "I don't know" et freelance exclus.
"""

import pandas as pd

from salaires.logique import SEUIL_N

AUTRES_PROFILS = "Autres profils de développement"

FAMILLES = {
    "Developer, full-stack": "Développeur full-stack",
    "Developer, back-end": "Développeur back-end",
    "Architect, software or solutions": "Architecte",
}

RESPONSABILITES = {
    "Individual contributor": "Contributeur",
    "Individual contributor in a senior or staff-level role": "Contributeur senior",
    "Both people manager and individual contributor": "Manager",
    "People manager": "Manager",
}
ORDRE_RESPONSABILITES = ["Contributeur", "Contributeur senior", "Manager"]

TAILLES = {
    "Less than 20 employees": "Moins de 100",
    "20 to 99 employees": "Moins de 100",
    "100 to 499 employees": "100 à 999",
    "500 to 999 employees": "100 à 999",
    "1,000 to 4,999 employees": "1 000 à 9 999",
    "5,000 to 9,999 employees": "1 000 à 9 999",
    "10,000 or more employees": "10 000 et plus",
}
ORDRE_TAILLES = ["Moins de 100", "100 à 999", "1 000 à 9 999", "10 000 et plus"]


def ajouter_groupes(df: pd.DataFrame) -> pd.DataFrame:
    """Ajoute les colonnes Famille, Responsabilite et TailleEntreprise.

    Une valeur absente des tables (OrgSize "I don't know", freelance, réponse vide)
    donne une case vide : la ligne reste, mais ne compte dans aucun groupe.
    """
    d = df.copy()
    d["Famille"] = d["Role"].map(FAMILLES).fillna(AUTRES_PROFILS).where(d["Role"].notna())
    d["Responsabilite"] = d["ICorPM"].map(RESPONSABILITES)
    d["TailleEntreprise"] = pd.Categorical(
        d["OrgSize"].map(TAILLES), categories=ORDRE_TAILLES, ordered=True
    )
    return d


def groupes_sous_seuil(df: pd.DataFrame, colonne: str) -> pd.Series:
    """Effectif des groupes présents mais sous SEUIL_N, dont la médiane est masquée."""
    effectifs = df[colonne].value_counts()
    return effectifs[(effectifs > 0) & (effectifs < SEUIL_N)]
