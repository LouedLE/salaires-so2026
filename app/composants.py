import plotly.graph_objects as go
import streamlit as st

from salaires.logique import legende_population
from salaires.population import DESCRIPTION


def afficher_figure(fig: go.Figure, n: int, description: str | None = None) -> None:
    """Affiche une figure Plotly suivie de la légende de population."""
    st.plotly_chart(fig, width="stretch")
    st.caption(legende_population(n, description=description or DESCRIPTION))
