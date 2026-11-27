import plotly.express as px
import streamlit as st

from composants import afficher_figure
from donnees import charger_population
from filtres import filtre_niveau
from salaires.axes.axe1_experience import courbe_salaire

st.set_page_config(page_title="Salaires des développeurs en France", layout="wide")

ESN = "IT services, consulting, systems integration, or managed services"
EDITEUR = "Software development"

population = charger_population()
df = filtre_niveau(population)
niveau = st.session_state["niveau"]

st.title("Salaires des développeurs en France")
st.caption(
    "Pour la direction de la rémunération d'une ESN. Enquête Stack Overflow 2026 : "
    "répondants volontaires à une enquête en ligne, pas un échantillon représentatif de tous les développeurs."
)

# Message pour le commanditaire, recalculé sur le niveau choisi.
esn = df.loc[df["Industry"] == ESN, "SalaireEUR"]
editeur = df.loc[df["Industry"] == EDITEUR, "SalaireEUR"]
comparable = len(esn) >= 30 and len(editeur) >= 30

if comparable:
    ecart = editeur.median() - esn.median()
    ecart_pct = ecart / editeur.median() * 100
    st.subheader(
        f"Les ESN paient leurs développeurs {ecart_pct:.0f} % de moins que les éditeurs de logiciels"
    )
    st.write(
        f"Salaire médian déclaré : {esn.median():,.0f} € en ESN contre {editeur.median():,.0f} € "
        f"chez les éditeurs, soit {ecart:,.0f} € d'écart. Les profils expérimentés sont les plus "
        "exposés à un départ vers un éditeur : l'axe 1 montre la progression avec l'expérience, "
        "l'axe 4 détaille l'écart par secteur."
        .replace(",", " ")
    )
else:
    st.subheader("Comparaison ESN et éditeurs indisponible pour ce niveau")
    st.write(f"Moins de 30 répondants dans l'un des deux groupes ({len(esn)} en ESN, {len(editeur)} chez les éditeurs).")

# Indicateurs clés.
c1, c2, c3, c4 = st.columns(4)
c1.metric("Salaire médian", f"{df['SalaireEUR'].median():,.0f} €".replace(",", " "))
c2.metric("Répondants", len(df))
c3.metric("Médiane ESN", f"{esn.median():,.0f} €".replace(",", " ") if len(esn) >= 30 else "n < 30")
c4.metric("Médiane éditeurs", f"{editeur.median():,.0f} €".replace(",", " ") if len(editeur) >= 30 else "n < 30")
st.caption(f"Population : développeurs professionnels salariés en France, enquête 2026, niveau : {niveau}. "
           f"ESN n = {len(esn)}, éditeurs n = {len(editeur)}.")

# Figure de synthèse : progression avec l'expérience, sur toute la population.
st.subheader("Le salaire progresse avec l'expérience")
courbe = courbe_salaire(population, "larges")
fig = px.bar(courbe, x="Tranche", y="mediane", text="n",
             labels={"Tranche": "Expérience professionnelle", "mediane": "Salaire médian (€)"})
fig.update_traces(texttemplate="n = %{text}", textposition="inside")
afficher_figure(fig, int(courbe["n"].sum()))
st.caption("Ce graphique porte sur tous les niveaux : le filtre de niveau ne s'y applique pas.")

st.subheader("Explorer")
st.page_link("pages/1_experience.py", label="Axe 1 : Expérience")
st.page_link("pages/2_metier_entreprise.py", label="Axe 2 : Métier et entreprise")
st.page_link("pages/3_technologies.py", label="Axe 3 : Technologies")
st.page_link("pages/4_conditions_travail.py", label="Axe 4 : Conditions de travail et secteur")
st.page_link("pages/5_france_europe.py", label="Axe 5 : France face à l'Europe")
