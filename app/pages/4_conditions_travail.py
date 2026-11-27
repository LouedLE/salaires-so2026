import plotly.express as px
import streamlit as st

from composants import afficher_figure
from donnees import charger_population
from salaires.axes.axe4_conditions_travail import comparer_esn_editeurs, medianes_par_travail

st.title("Axe 4 : Conditions de travail et secteur")
st.info(
    "Le commanditaire est une ESN : la figure centrale compare les salaires médians "
    "des ESN et des éditeurs de logiciels."
)

niveau = st.session_state.get("niveau", "Tous")
pop = charger_population()
if niveau != "Tous":
    pop = pop[pop["Niveau"] == niveau]

st.subheader("ESN contre éditeurs de logiciels")
esn_editeurs = comparer_esn_editeurs(pop)
if esn_editeurs.empty:
    st.warning("Effectif insuffisant pour ce niveau.")
else:
    fig = px.bar(
        esn_editeurs,
        x="SecteurGroupe",
        y="mediane",
        text="mediane",
        labels={"SecteurGroupe": "Secteur", "mediane": "Salaire médian (€)"},
    )
    afficher_figure(fig, n=len(pop))

st.subheader("Salaire médian selon le mode de travail")
travail = medianes_par_travail(pop)
fig2 = px.bar(
    travail,
    x="Travail",
    y="mediane",
    text="mediane",
    labels={"Travail": "Mode de travail", "mediane": "Salaire médian (€)"},
)
afficher_figure(fig2, n=len(pop))
