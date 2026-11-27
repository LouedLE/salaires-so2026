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


def definir_population(df: pd.DataFrame) -> pd.DataFrame:
    raise NotImplementedError("Socle commun : population à écrire")
