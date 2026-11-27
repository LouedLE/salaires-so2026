"""Logique partagée par tous les axes. Aucun import Streamlit ici.

Responsable : à attribuer (socle commun).

À implémenter :
- SEUIL_N : en dessous, une médiane n'est pas affichée.
- mediane_par_groupe(df, colonne) -> DataFrame [colonne, mediane, n]
  avec les groupes sous SEUIL_N marqués ou retirés.
- legende_population(n, annee) -> str, par exemple :
  "Développeurs professionnels salariés à temps plein en France,
   enquête Stack Overflow 2026, n = 412 répondants"
- eclater_choix_multiples(df, colonne) : pour les colonnes séparées par ";"
  (LanguagesHaveWorkedWith...), une ligne par choix.
"""

import pandas as pd

SEUIL_N = 30


def mediane_par_groupe(df: pd.DataFrame, colonne: str) -> pd.DataFrame:
    raise NotImplementedError


def legende_population(n: int, annee: int = 2026) -> str:
    raise NotImplementedError


def eclater_choix_multiples(df: pd.DataFrame, colonne: str) -> pd.DataFrame:
    raise NotImplementedError
