import plotly.graph_objects as go
import streamlit as st

from composants import afficher_figure
from donnees import charger_population
from salaires.axes.axe1_experience import courbe_salaire, gain_par_annee
from salaires.logique import SEUIL_N

st.title("Axe 1 : Expérience")

population = charger_population()

# Filtres propres à l'axe. Le filtre de niveau partagé ne s'applique pas ici :
# l'expérience est justement la variable étudiée.
decoupage = st.sidebar.radio("Découpage de l'expérience", ["fines", "larges"],
                             format_func=lambda x: "6 tranches" if x == "fines" else "3 tranches")
afficher_quartiles = st.sidebar.checkbox("Afficher les 1er et 3e quartiles", value=True)

courbe = courbe_salaire(population, decoupage)
fiable = courbe[courbe["fiable"]]
gain = gain_par_annee(population)
n_total = int(fiable["n"].sum())

st.subheader(f"Chaque année d'expérience s'accompagne d'environ {gain:,.0f} € de salaire médian en plus".replace(",", " "))
st.write(
    f"De {fiable['Tranche'].iloc[0]} à {fiable['Tranche'].iloc[-1]}, le salaire médian passe de "
    f"{fiable['mediane'].iloc[0]:,.0f} € à {fiable['mediane'].iloc[-1]:,.0f} € "
    f"(+{fiable['progression_pct'].iloc[-1]:.0f} %).".replace(",", " ")
)

fig = go.Figure()
if afficher_quartiles:
    fig.add_trace(go.Scatter(x=fiable["Tranche"], y=fiable["q3"], mode="lines", line=dict(width=0),
                             showlegend=False, hoverinfo="skip"))
    fig.add_trace(go.Scatter(x=fiable["Tranche"], y=fiable["q1"], mode="lines", line=dict(width=0),
                             fill="tonexty", fillcolor="rgba(31,119,180,0.15)", name="1er à 3e quartile"))
fig.add_trace(go.Scatter(x=fiable["Tranche"], y=fiable["mediane"], mode="lines+markers+text",
                         text=[f"n = {n}" for n in fiable["n"]], textposition="top center",
                         name="Salaire médian"))
fig.update_layout(xaxis_title="Expérience professionnelle", yaxis_title="Salaire annuel brut déclaré (€)")
afficher_figure(fig, n_total)

exclues = courbe[~courbe["fiable"]]
if not exclues.empty:
    st.info("Tranches masquées, moins de " + str(SEUIL_N) + " répondants : "
            + ", ".join(f"{t} (n = {n})" for t, n in zip(exclues["Tranche"], exclues["n"])))

st.subheader("Détail par tranche")
tableau = courbe[["Tranche", "n", "mediane", "q1", "q3", "progression_pct"]].rename(columns={
    "n": "Répondants", "mediane": "Médiane (€)", "q1": "1er quartile (€)", "q3": "3e quartile (€)",
    "progression_pct": "Écart avec la 1re tranche fiable (%)"})
st.dataframe(tableau, hide_index=True,
             column_config={c: st.column_config.NumberColumn(format="%.0f") for c in tableau.columns[2:]})
st.caption("Médiane et quartiles plutôt que moyenne : quelques salaires très élevés tirent la moyenne vers le haut.")
