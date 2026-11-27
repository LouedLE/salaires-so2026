import plotly.express as px
import streamlit as st

from composants import afficher_figure
from donnees import charger_population
from salaires.axes.axe4_conditions_travail import (
    EDITEURS,
    ESN,
    comparer_esn_editeurs,
    medianes_par_travail,
)


def euros(montant):
    return f"{montant:,.0f} €".replace(",", " ")


st.title("Axe 4 : Conditions de travail et secteur")

niveau = st.session_state.get("niveau", "Tous")
pop = charger_population()
if niveau != "Tous":
    pop = pop[pop["Niveau"] == niveau]

esn_editeurs = comparer_esn_editeurs(pop)
travail = medianes_par_travail(pop)

if esn_editeurs.empty:
    st.warning("Effectif insuffisant pour ce niveau.")
else:
    medianes = esn_editeurs.set_index("SecteurGroupe")["mediane"]
    ecart = (1 - medianes[ESN] / medianes[EDITEURS]) * 100
    st.subheader(
        f"Les ESN versent un salaire médian de {euros(medianes[ESN])}, "
        f"{ecart:.0f} % de moins que les éditeurs de logiciels ({euros(medianes[EDITEURS])})."
    )

    st.markdown("### ESN contre éditeurs de logiciels")
    fig = px.bar(
        esn_editeurs,
        x="SecteurGroupe",
        y="mediane",
        text="mediane",
        labels={"SecteurGroupe": "Secteur", "mediane": "Salaire médian (€)"},
    )
    afficher_figure(fig, n=int(esn_editeurs["n"].sum()))

st.markdown("### Salaire médian selon le mode de travail")
fig2 = px.bar(
    travail,
    x="Travail",
    y="mediane",
    text="mediane",
    labels={"Travail": "Mode de travail", "mediane": "Salaire médian (€)"},
)
afficher_figure(fig2, n=int(travail["n"].sum()))
