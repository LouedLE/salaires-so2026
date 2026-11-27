import plotly.express as px
import streamlit as st

from composants import afficher_figure
from donnees import charger_population
from filtres import filtre_niveau
from salaires.axes.axe2_metier_entreprise import (
    AUTRES_PROFILS,
    ORDRE_RESPONSABILITES,
    ORDRE_TAILLES,
    ajouter_groupes,
    groupes_sous_seuil,
)
from salaires.logique import SEUIL_N, mediane_par_groupe
from salaires.population import DESCRIPTION

BLEU = "#257de0"
GRIS = "#a3a3a3"
NOTE_AUTRES = (
    "Autres profils de développement : groupe hétérogène (desktop, DevOps, embarqué, IA, recherche...), "
    "médiane non interprétable comme un métier."
)


def euros(montant):
    return f"{montant:,.0f} €".replace(",", " ")


def signaler_masques(df, colonne):
    masques = groupes_sous_seuil(df, colonne)
    if not masques.empty:
        st.info(
            f"Médianes masquées, moins de {SEUIL_N} répondants : "
            + ", ".join(f"{groupe} (n = {n})" for groupe, n in masques.items())
        )


def afficher_vue(table, x, couleurs, ordre, description, titre_x=""):
    """Graphique en barres des médianes, ou un message si aucun groupe n'atteint le seuil."""
    if table.empty:
        st.warning(f"Aucun groupe n'atteint {SEUIL_N} répondants avec ces filtres.")
        return
    fig = px.bar(
        table, x=x, y="mediane", text="n",
        category_orders={x: ordre},
        labels={"mediane": "Salaire annuel médian (€)", x: titre_x},
    )
    fig.update_traces(
        marker_color=couleurs,
        texttemplate="%{y:,.0f} € (n = %{text})", textposition="inside",
    )
    fig.update_layout(separators=", ")
    afficher_figure(fig, int(table["n"].sum()), description=description)


st.title("Axe 2 : Métier et entreprise")

# Filtre partagé entre les pages : sélecteur de niveau d'expérience dans la sidebar.
pop = filtre_niveau(ajouter_groupes(charger_population()))
niveau = st.session_state["niveau"]

# Filtre de l'axe : taille d'entreprise, appliqué aux vues métier et responsabilité.
taille = st.sidebar.selectbox("Taille d'entreprise", ["Toutes"] + ORDRE_TAILLES)
df = pop if taille == "Toutes" else pop[pop["TailleEntreprise"] == taille]

description_pop = DESCRIPTION if niveau == "Tous" else f"{DESCRIPTION}, niveau {niveau}"
description = description_pop if taille == "Toutes" else f"{description_pop}, entreprises de {taille} salariés"

# Message, calculé sur les filtres choisis.
resp = mediane_par_groupe(df, "Responsabilite")
mediane = resp.set_index("Responsabilite")["mediane"]
if {"Contributeur", "Contributeur senior"} <= set(mediane.index):
    ecart = mediane["Contributeur senior"] - mediane["Contributeur"]
    st.subheader(
        f"Les contributeurs seniors gagnent {euros(ecart)} de plus par an que les contributeurs : "
        f"{euros(mediane['Contributeur senior'])} contre {euros(mediane['Contributeur'])} en médiane"
    )
else:
    st.subheader("Trop peu de répondants avec ces filtres pour comparer contributeurs et contributeurs seniors")

# Vue 1 : responsabilité.
st.subheader("Salaire médian selon la responsabilité")
afficher_vue(resp, "Responsabilite", BLEU, ORDRE_RESPONSABILITES, description)
signaler_masques(df, "Responsabilite")

# Vue 2 : famille de métier, autres profils en gris et en dernier.
st.subheader("Salaire médian selon le métier")
fam = mediane_par_groupe(df, "Famille")
fam["autre"] = fam["Famille"] == AUTRES_PROFILS
fam = fam.sort_values(["autre", "mediane"], ascending=[True, False])
couleurs = [GRIS if autre else BLEU for autre in fam["autre"]]
afficher_vue(fam, "Famille", couleurs, fam["Famille"].tolist(), description)
if fam["autre"].any():
    st.caption(NOTE_AUTRES)
signaler_masques(df, "Famille")

# Vue 3 : taille d'entreprise, toujours sur toutes les tailles.
st.subheader("Salaire médian selon la taille de l'entreprise")
tai = mediane_par_groupe(pop, "TailleEntreprise")
if not tai.empty:
    bas, haut = tai["mediane"].min(), tai["mediane"].max()
    if (haut - bas) / haut < 0.10:
        st.write(f"La taille de l'entreprise ne change presque pas le salaire ({euros(bas)} à {euros(haut)}).")
    else:
        st.write(f"Selon la taille de l'entreprise, le salaire médian va de {euros(bas)} à {euros(haut)}.")
afficher_vue(tai, "TailleEntreprise", BLEU, ORDRE_TAILLES, f"{description_pop}, taille d'entreprise renseignée", "Nombre de salariés")
signaler_masques(pop, "TailleEntreprise")
if taille != "Toutes":
    st.caption("Cette vue compare les tailles entre elles : le filtre de taille ne s'y applique pas.")
