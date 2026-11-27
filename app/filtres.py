"""Filtre partagé entre les pages : le niveau d'expérience.

Le choix est rangé dans st.session_state["niveau"].
Il suit l'utilisateur d'une page à l'autre.
"""

import pandas as pd
import streamlit as st

NIVEAUX = ["Tous", "Junior", "Confirmé", "Senior"]
AIDE = "Junior : 0 à 4 ans d'expérience pro. Confirmé : 5 à 9 ans. Senior : 10 ans et plus."


def _memoriser():
    # Streamlit efface la clé d'un widget quand on change de page.
    # On recopie donc la valeur dans une clé qui n'appartient à aucun widget.
    st.session_state["niveau"] = st.session_state["_choix_niveau"]


def filtre_niveau(df: pd.DataFrame) -> pd.DataFrame:
    """Affiche le sélecteur de niveau dans la sidebar et renvoie df filtré."""
    st.session_state.setdefault("niveau", "Tous")
    st.sidebar.selectbox(
        "Niveau d'expérience",
        NIVEAUX,
        index=NIVEAUX.index(st.session_state["niveau"]),
        key="_choix_niveau",
        on_change=_memoriser,
        help=AIDE,
    )
    niveau = st.session_state["niveau"]
    if niveau == "Tous":
        return df
    return df[df["Niveau"] == niveau]
