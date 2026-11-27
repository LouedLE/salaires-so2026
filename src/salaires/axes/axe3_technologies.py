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
