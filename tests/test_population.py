import pandas as pd

from salaires.population import ajouter_niveau


def test_bornes_des_niveaux():
    df = pd.DataFrame({"WorkExp": [0, 4, 5, 9, 10, 40]})
    niveaux = ajouter_niveau(df)["Niveau"].tolist()
    assert niveaux == ["Junior", "Junior", "Confirmé", "Confirmé", "Senior", "Senior"]


def test_workexp_manquant_garde_la_ligne():
    df = pd.DataFrame({"WorkExp": [3, None]})
    resultat = ajouter_niveau(df)
    assert len(resultat) == 2
    assert pd.isna(resultat["Niveau"].iloc[1])


def test_ne_modifie_pas_le_tableau_d_origine():
    df = pd.DataFrame({"WorkExp": [3]})
    ajouter_niveau(df)
    assert "Niveau" not in df.columns
