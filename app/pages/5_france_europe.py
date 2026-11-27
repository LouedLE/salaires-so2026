import plotly.express as px
import streamlit as st

from composants import afficher_figure
from salaires.axes.axe5_france_europe import (
    DESCRIPTION,
    definir_population_europe,
    ecart_avec_france,
    mediane_par_niveau,
    mediane_par_pays,
)
from salaires.chargement import charger_brut
from salaires.logique import SEUIL_N
from salaires.population import NIVEAUX

BLEU = "#257de0"
ORANGE = "#f47230"
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

# Vue 2 : écart par niveau d'expérience entre la France et un pays choisi.
autres = [p for p in par_pays["Pays"] if p != "France"]
pays = st.sidebar.selectbox("Pays comparé à la France", autres, index=autres.index("Allemagne"))

st.subheader(f"France et {pays} par niveau d'expérience")
par_niveau = mediane_par_niveau(pop, pays)
fiables = par_niveau[par_niveau["fiable"]]
fig2 = px.bar(
    fiables, x="Niveau", y="mediane", color="Pays", barmode="group", text="n",
    category_orders={"Niveau": NIVEAUX, "Pays": ["France", pays]},
    color_discrete_map={"France": BLEU, pays: ORANGE},
    labels={"mediane": "Salaire annuel médian (dollars US)", "Niveau": "Niveau d'expérience"},
)
fig2.update_traces(texttemplate="n = %{text}", textposition="inside")
afficher_figure(
    fig2, int(fiables["n"].sum()),
    description=f"Développeurs professionnels salariés, France et {pays}, expérience renseignée",
)

masques = par_niveau[~par_niveau["fiable"]]
if not masques.empty:
    st.info(
        f"Médianes masquées, moins de {SEUIL_N} répondants : "
        + ", ".join(f"{p} {niv} (n = {n})" for p, niv, n in zip(masques["Pays"], masques["Niveau"], masques["n"]))
    )

ecart = ecart_avec_france(par_niveau, pays).rename(columns={
    "France": "France ($)", pays: f"{pays} ($)", "ecart_pct": f"Écart {pays} / France (%)",
})
st.dataframe(
    ecart, hide_index=True,
    column_config={c: st.column_config.NumberColumn(format="%.0f") for c in ecart.columns[1:]},
)
st.caption("Écart positif : le pays paie plus que la France à niveau égal.")
