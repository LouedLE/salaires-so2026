"""Définition de la population étudiée. Aucun import Streamlit ici.

Population : répondants en France qui codent comme activité principale,
salariés, payés en euros, avec un salaire renseigné et compris entre
SALAIRE_MIN et SALAIRE_MAX. Chaque filtre est justifié dans DECISIONS.md.

Colonne "SalaireEUR" : salaire annuel en euros, repris de Compensation.
Pour la France on part de Compensation + Currency (EUR) plutôt que de
ConvertedCompYearly (en dollars, dépend du taux de change de l'année).
"""

import pandas as pd

DESCRIPTION = "Développeurs professionnels salariés en France"

PAYS = "France"
CODE_PRINCIPAL = "I create code as a primary part of my job"
SALARIE = "Employed"
DEVISE = "EUR"

# Niveaux d'expérience, à partir de WorkExp (années d'expérience professionnelle).
# Junior : 0 à 4 ans, Confirmé : 5 à 9 ans, Senior : 10 ans et plus.
# Chaque niveau garde au moins SEUIL_N répondants : voir DECISIONS.md.
NIVEAUX = ["Junior", "Confirmé", "Senior"]
BORNES_NIVEAU = [-1, 4, 9, float("inf")]

# Bornes contre les valeurs aberrantes, incluses.
# Sur les 382 répondants avant bornes : 2e centile ≈ 15 000 €, 99e centile ≈ 192 000 €.
SALAIRE_MIN = 15_000
SALAIRE_MAX = 200_000


def definir_population(df: pd.DataFrame) -> pd.DataFrame:
    """Applique les filtres de population et ajoute la colonne SalaireEUR."""
    d = df[df["Country"] == PAYS]
    d = d[d["CodeMain"] == CODE_PRINCIPAL]
    d = d[d["Employment"] == SALARIE]
    d = d[d["Currency"].str.startswith(DEVISE, na=False)]
    d = d[d["Compensation"].notna()].copy()
    d["SalaireEUR"] = d["Compensation"]
    return d[d["SalaireEUR"].between(SALAIRE_MIN, SALAIRE_MAX)]


def ajouter_niveau(df: pd.DataFrame) -> pd.DataFrame:
    """Ajoute la colonne Niveau (Junior, Confirmé, Senior) à partir de WorkExp.

    Les répondants sans WorkExp restent dans le tableau, avec un Niveau vide.
    """
    resultat = df.copy()
    resultat["Niveau"] = pd.cut(resultat["WorkExp"], bins=BORNES_NIVEAU, labels=NIVEAUX)
    return resultat
