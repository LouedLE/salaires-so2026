import pandas as pd

from salaires.axes.axe5_france_europe import definir_population_europe, ecart_avec_france, mediane_par_niveau
from salaires.logique import SEUIL_N


def repondant(pays, salaire, experience=12, code="I create code as a primary part of my job", statut="Employed"):
    return {"Country": pays, "CodeMain": code, "Employment": statut,
            "ConvertedCompYearly": salaire, "WorkExp": experience}


def test_population_garde_les_cinq_pays_et_les_salaries_qui_codent():
    df = pd.DataFrame([
        repondant("France", 50_000),
        repondant("Spain", 40_000),
        repondant("Italy", 45_000),
        repondant("France", 60_000, statut="Student"),
        repondant("France", 60_000, code="I create code occasionally"),
        repondant("Germany", None),
    ])
    pop = definir_population_europe(df)
    assert pop["Pays"].tolist() == ["France", "Espagne"]


def test_ecart_vide_sous_le_seuil():
    seniors_france = [repondant("France", 50_000) for _ in range(SEUIL_N)]
    seniors_espagne = [repondant("Spain", 60_000) for _ in range(SEUIL_N)]
    juniors_espagne = [repondant("Spain", 30_000, experience=2) for _ in range(SEUIL_N - 1)]
    pop = definir_population_europe(pd.DataFrame(seniors_france + seniors_espagne + juniors_espagne))

    ecart = ecart_avec_france(mediane_par_niveau(pop, "Espagne"), "Espagne").set_index("Niveau")
    assert round(ecart.loc["Senior", "ecart_pct"]) == 20
    assert pd.isna(ecart.loc["Junior", "ecart_pct"])
