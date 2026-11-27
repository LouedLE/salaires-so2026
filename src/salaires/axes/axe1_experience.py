"""Axe 1 : Expérience. Calculs de l'axe, aucun import Streamlit ici.

Responsable : Louis-Edouard.
"""

import pandas as pd

from salaires.logique import SEUIL_N

# Bornes des tranches d'années d'expérience professionnelle (WorkExp).
# Chaque tranche doit garder au moins SEUIL_N répondants : vérifié dans DECISIONS.md.
TRANCHES = {
    "fines": ([-1, 2, 5, 9, 14, 19, 100], ["0-2 ans", "3-5 ans", "6-9 ans", "10-14 ans", "15-19 ans", "20 ans et plus"]),
    "larges": ([-1, 4, 9, 100], ["0-4 ans", "5-9 ans", "10 ans et plus"]),
}


def ajouter_tranche(df: pd.DataFrame, decoupage: str = "fines") -> pd.DataFrame:
    """Ajoute la colonne Tranche à partir de WorkExp. Les WorkExp manquants sont retirés."""
    bornes, etiquettes = TRANCHES[decoupage]
    d = df.dropna(subset=["WorkExp"]).copy()
    d["Tranche"] = pd.cut(d["WorkExp"], bornes, labels=etiquettes)
    return d


def courbe_salaire(df: pd.DataFrame, decoupage: str = "fines") -> pd.DataFrame:
    """Salaire médian, 1er et 3e quartiles et effectif par tranche d'expérience.

    Renvoie aussi la progression en % par rapport à la première tranche.
    Les tranches sous SEUIL_N sont marquées fiable=False au lieu d'être retirées,
    pour garder l'axe des x complet sur le graphique.
    """
    d = ajouter_tranche(df, decoupage)
    t = (
        d.groupby("Tranche", observed=False)["SalaireEUR"]
        .agg(
            mediane="median",
            q1=lambda s: s.quantile(0.25),
            q3=lambda s: s.quantile(0.75),
            n="count",
        )
        .reset_index()
    )
    t["fiable"] = t["n"] >= SEUIL_N
    premiere = t.loc[t["fiable"], "mediane"].iloc[0] if t["fiable"].any() else None
    t["progression_pct"] = (t["mediane"] / premiere - 1) * 100 if premiere else None
    return t


def gain_par_annee(df: pd.DataFrame, max_annees: int = 20) -> float:
    """Gain annuel moyen en euros : pente d'une droite ajustée sur les médianes par année.

    On se limite à max_annees : au-delà, les effectifs par année deviennent trop faibles.
    """
    d = df.dropna(subset=["WorkExp"])
    d = d[d["WorkExp"] <= max_annees]
    med = d.groupby("WorkExp")["SalaireEUR"].median()
    x, y = med.index.to_numpy(float), med.to_numpy(float)
    pente = ((x - x.mean()) * (y - y.mean())).sum() / ((x - x.mean()) ** 2).sum()
    return float(pente)
