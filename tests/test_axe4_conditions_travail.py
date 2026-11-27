import pandas as pd

from salaires.axes.axe4_conditions_travail import AUTRES, EDITEURS, regrouper_secteur, regrouper_travail


def test_regroupe_les_trois_modes_de_travail():
    df = pd.DataFrame(
        {
            "WorkSetting": [
                "Remote",
                "In-person",
                "Your choice (very flexible, you can come in when you want or just as needed)",
            ]
        }
    )
    assert list(regrouper_travail(df)["Travail"]) == ["Télétravail complet", "Sur site", "Hybride"]


def test_secteur_non_renseigne_reste_vide():
    df = pd.DataFrame({"Industry": ["Software development", None, "Healthcare"]})
    secteurs = regrouper_secteur(df)["SecteurGroupe"].tolist()
    assert secteurs[0] == EDITEURS
    assert pd.isna(secteurs[1])
    assert secteurs[2] == AUTRES
