"""Définition de la population étudiée. Aucun import Streamlit ici.

Responsable : à attribuer (socle commun).

À implémenter :
- definir_population(df) -> DataFrame filtré :
  pays France, personnes qui codent dans leur métier (CodeMain),
  salariés à temps plein (Employment), salaire renseigné,
  bornes basse et haute contre les valeurs aberrantes.
- Chaque filtre est justifié dans DECISIONS.md avec le nombre de lignes avant/après.
- Colonne "SalaireEUR" : salaire annuel en euros.
  Pour la France, partir de Compensation + Currency (EUR) plutôt que
  ConvertedCompYearly (en dollars, dépend du taux de change de l'année).
"""

import pandas as pd

DESCRIPTION = "Développeurs professionnels salariés à temps plein en France"

# Niveaux d'expérience, à partir de WorkExp (années d'expérience professionnelle).
# Junior : 0 à 4 ans, Confirmé : 5 à 9 ans, Senior : 10 ans et plus.
# Chaque niveau garde au moins SEUIL_N répondants : voir DECISIONS.md.
NIVEAUX = ["Junior", "Confirmé", "Senior"]
BORNES_NIVEAU = [-1, 4, 9, float("inf")]


def definir_population(df: pd.DataFrame) -> pd.DataFrame:
    raise NotImplementedError("Socle commun : population à écrire")


def ajouter_niveau(df: pd.DataFrame) -> pd.DataFrame:
    """Ajoute la colonne Niveau (Junior, Confirmé, Senior) à partir de WorkExp.

    Les répondants sans WorkExp restent dans le tableau, avec un Niveau vide.
    """
    resultat = df.copy()
    resultat["Niveau"] = pd.cut(resultat["WorkExp"], bins=BORNES_NIVEAU, labels=NIVEAUX)
    return resultat
