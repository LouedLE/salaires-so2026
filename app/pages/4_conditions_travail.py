"""Page 4 : conditions de travail et secteur. Auteur : Arthur Dousset."""

import plotly.express as px
import streamlit as st

from composants import afficher_figure
from donnees import charger_population
from filtres import filtre_niveau
from salaires.axes.axe4_conditions_travail import (
    EDITEURS,
    ESN,
    SUR_SITE,
    TELETRAVAIL,
    comparer_esn_editeurs,
    medianes_par_travail,
    regrouper_travail,
)


def euros(montant):
    return f"{montant:,.0f} €".replace(",", " ")


st.title("Axe 4 : Conditions de travail et secteur")

pop = filtre_niveau(charger_population())

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
    fig.update_traces(texttemplate="%{y:,.0f} €")
    afficher_figure(fig, n=int(esn_editeurs["n"].sum()))

st.markdown("### Salaire médian selon le mode de travail")
fig2 = px.bar(
    travail,
    x="Travail",
    y="mediane",
    text="mediane",
    labels={"Travail": "Mode de travail", "mediane": "Salaire médian (€)"},
)
fig2.update_traces(texttemplate="%{y:,.0f} €")
afficher_figure(fig2, n=int(travail["n"].sum()))

# Part des juniors par mode de travail, calculée sur toute la population (pas le filtre).
juniors = (
    regrouper_travail(charger_population())
    .dropna(subset=["Niveau"])
    .assign(junior=lambda d: d["Niveau"] == "Junior")
    .groupby("Travail", observed=True)["junior"]
    .mean()
)
st.markdown(
    f"Une partie de l'écart peut tenir à la composition des groupes : "
    f"{juniors[SUR_SITE] * 100:.0f} % des répondants sur site sont juniors, "
    f"contre {juniors[TELETRAVAIL] * 100:.0f} % en télétravail "
    f"(effectifs faibles : à lire avec prudence)."
)
