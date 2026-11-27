import plotly.express as px
import streamlit as st

from composants import afficher_figure
from donnees import charger_population
from filtres import filtre_niveau
from salaires.axes.axe3_technologies import COLONNE, DESCRIPTION, mediane_par_langage, population_langages
from salaires.logique import SEUIL_N

BLEU = "#257de0"
GRIS = "#a3a3a3"


def euros(montant):
    return f"{montant:,.0f} €".replace(",", " ")


st.title("Axe 3 : Technologies")

df = filtre_niveau(charger_population())
niveau = st.session_state["niveau"]
pop = population_langages(df)
langages = mediane_par_langage(df)
mediane_axe = pop["SalaireEUR"].median()
description = DESCRIPTION if niveau == "Tous" else f"{DESCRIPTION}, niveau {niveau}"

if langages.empty:
    st.subheader(f"Aucun langage n'atteint {SEUIL_N} répondants pour ce niveau")
    st.stop()

premier = langages.iloc[0]
st.subheader(
    f"{premier[COLONNE]} est le langage le mieux payé : {euros(premier['mediane'])} en médiane, "
    f"{premier['ecart_pct']:.0f} % de plus que l'ensemble des répondants ({euros(mediane_axe)})"
)
derniers = list(langages.loc[langages["mediane"] == langages["mediane"].min(), COLONNE])
noms = derniers[0] if len(derniers) == 1 else ", ".join(derniers[:-1]) + " et " + derniers[-1]
st.write(f"En bas du classement : {noms}, à {euros(langages['mediane'].min())}.")

# Vue : salaire médian par langage, au-dessus de la médiane de l'axe en bleu.
fig = px.bar(
    langages, x="mediane", y=COLONNE, orientation="h", text="n",
    labels={"mediane": "Salaire annuel médian (€)", COLONNE: ""},
)
fig.update_traces(
    marker_color=[BLEU if e >= 0 else GRIS for e in langages["ecart_pct"]],
    texttemplate="%{x:,.0f} € (n = %{text})", textposition="inside", insidetextanchor="start",
)
fig.add_vline(
    x=mediane_axe, line_dash="dash", line_color="#666666",
    annotation_text=f"Ensemble : {euros(mediane_axe)}", annotation_position="bottom right",
)
fig.update_yaxes(autorange="reversed")
fig.update_layout(separators=", ", height=120 + 35 * len(langages))
afficher_figure(fig, len(pop), description=description)

nb_choix = pop[COLONNE].str.count(";").add(1).median()
st.caption(
    "En bleu, les langages payés au-dessus de la médiane de l'ensemble. "
    f"Un répondant compte dans chaque langage qu'il a coché ({nb_choix:.0f} en médiane) : "
    "les barres se recouvrent et leurs n ne s'additionnent pas. La légende donne le nombre de répondants."
)
nb_langages = pop[COLONNE].str.split(";").explode().nunique()
st.info(f"{nb_langages - len(langages)} langages sur {nb_langages} ont moins de {SEUIL_N} répondants : leur médiane est masquée.")
