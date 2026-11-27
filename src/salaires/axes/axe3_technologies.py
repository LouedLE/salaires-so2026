"""Axe 3 : Technologies. Calculs de l'axe, aucun import Streamlit ici.

Responsable : Yann.

Un répondant coche plusieurs langages dans LanguagesHaveWorkedWith (séparés par ";").
Après éclatement, il compte une fois dans chaque langage coché : les groupes se recouvrent.
"""

import pandas as pd

from salaires.logique import eclater_choix_multiples, mediane_par_groupe

COLONNE = "LanguagesHaveWorkedWith"
DESCRIPTION = "Développeurs professionnels salariés en France qui indiquent leurs langages"


def population_langages(df: pd.DataFrame) -> pd.DataFrame:
    """Population de l'axe : les répondants qui indiquent au moins un langage."""
    return df[df[COLONNE].notna()]


def mediane_par_langage(df: pd.DataFrame) -> pd.DataFrame:
    """Salaire médian et effectif par langage, du mieux au moins bien payé.

    Les langages sous SEUIL_N répondants sont retirés par mediane_par_groupe.
    ecart_pct : écart en % avec la médiane de toute la population de l'axe.
    """
    pop = population_langages(df)
    eclate = eclater_choix_multiples(pop, COLONNE)
    tableau = mediane_par_groupe(eclate, COLONNE)
    tableau["ecart_pct"] = (tableau["mediane"] / pop["SalaireEUR"].median() - 1) * 100
    return tableau.sort_values("mediane", ascending=False).reset_index(drop=True)
