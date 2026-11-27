"""Données partagées par les pages Streamlit. Ici, Streamlit est autorisé."""

import pandas as pd
import streamlit as st

from salaires.chargement import charger_brut
from salaires.population import ajouter_niveau, definir_population


@st.cache_data
def charger_population() -> pd.DataFrame:
    brut = charger_brut()
    population = definir_population(brut)
    return ajouter_niveau(population)
