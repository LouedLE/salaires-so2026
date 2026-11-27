import plotly.express as px
import streamlit as st

from composants import afficher_figure
from salaires.axes.axe5_france_europe import (
    DESCRIPTION,
    definir_population_europe,
    mediane_par_pays,
)
from salaires.chargement import charger_brut

BLEU = "#257de0"
GRIS = "#a3a3a3"


@st.cache_data
def charger_population_europe():
    return definir_population_europe(charger_brut())


def dollars(montant):
    return f"{montant:,.0f} $".replace(",", " ")


st.title("Axe 5 : France face à l'Europe")

pop = charger_population_europe()
par_pays = mediane_par_pays(pop)
mediane = par_pays.set_index("Pays")["mediane"]

ecart_uk = (1 - mediane["France"] / mediane["Royaume-Uni"]) * 100
st.subheader(
    f"Avec {dollars(mediane['France'])} de salaire médian, la France est au niveau de l'Espagne "
    f"et {ecart_uk:.0f} % sous le Royaume-Uni"
)
st.warning(
    "Salaire annuel brut déclaré : il ne tient compte ni du coût de la vie ni des cotisations sociales, "
    "très différentes entre ces pays. Un écart de salaire n'est pas un écart de niveau de vie."
)
st.caption(
    "Salaires comparés en ConvertedCompYearly, converti en dollars US par Stack Overflow : "
    "c'est la seule unité commune entre ces pays. Les montants dépendent donc aussi du taux de change."
)

# Vue 1 : médiane par pays.
st.subheader("Salaire médian par pays")
visibles = par_pays[par_pays["fiable"]]
fig = px.bar(
    visibles, x="mediane", y="Pays", orientation="h", text="n",
    labels={"mediane": "Salaire annuel médian (dollars US)", "Pays": ""},
)
fig.update_traces(
    marker_color=[BLEU if p == "France" else GRIS for p in visibles["Pays"]],
    texttemplate="%{x:,.0f} $ (n = %{text})", textposition="inside",
)
fig.update_layout(separators=", ")
afficher_figure(fig, int(visibles["n"].sum()), description=DESCRIPTION)
