import pandas as pd

from salaires.axes.axe2_metier_entreprise import (
    AUTRES_PROFILS,
    ajouter_groupes,
    groupes_sous_seuil,
)


def test_famille_de_role():
    df = pd.DataFrame(
        {
            "Role": ["Developer, full-stack", "Developer, mobile", None],
            "ICorPM": [None] * 3,
            "OrgSize": [None] * 3,
        }
    )
    familles = ajouter_groupes(df)["Famille"]
    assert familles.iloc[0] == "Développeur full-stack"
    assert familles.iloc[1] == AUTRES_PROFILS  # métier hors table : autres profils
    assert pd.isna(familles.iloc[2])  # réponse vide : pas rangée dans les autres


def test_managers_regroupes():
    df = pd.DataFrame(
        {
            "Role": [None] * 2,
            "ICorPM": ["People manager", "Both people manager and individual contributor"],
            "OrgSize": [None] * 2,
        }
    )
    assert ajouter_groupes(df)["Responsabilite"].tolist() == ["Manager", "Manager"]


def test_taille_exclut_inconnu_et_freelance():
    df = pd.DataFrame(
        {
            "Role": [None] * 4,
            "ICorPM": [None] * 4,
            "OrgSize": [
                "20 to 99 employees",
                "10,000 or more employees",
                "I don’t know",
                "Just me - I am a freelancer, sole proprietor, etc.",
            ],
        }
    )
    tailles = ajouter_groupes(df)["TailleEntreprise"]
    assert tailles.iloc[0] == "Moins de 100"
    assert tailles.iloc[1] == "10 000 et plus"
    assert tailles.iloc[2:].isna().all()
    assert len(tailles) == 4  # les lignes exclues restent dans le tableau


def test_ne_modifie_pas_le_tableau_d_origine():
    df = pd.DataFrame({"Role": ["Developer, back-end"], "ICorPM": [None], "OrgSize": [None]})
    ajouter_groupes(df)
    assert "Famille" not in df.columns


def test_groupes_sous_seuil():
    tailles = pd.Categorical(
        ["Moins de 100"] * 30 + ["100 à 999"] * 29,
        categories=["Moins de 100", "100 à 999", "10 000 et plus"],
    )
    df = pd.DataFrame({"TailleEntreprise": tailles})
    masques = groupes_sous_seuil(df, "TailleEntreprise")
    # 30 atteint le seuil, 29 non ; la classe à 0 répondant n'est pas signalée.
    assert masques.to_dict() == {"100 à 999": 29}
