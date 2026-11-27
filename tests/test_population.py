import pandas as pd

from salaires.population import ajouter_niveau, definir_population

CODE = "I create code as a primary part of my job"


def ligne(**modifs):
    """Un répondant qui passe tous les filtres, sauf ce qu'on modifie."""
    base = {
        "Country": "France",
        "CodeMain": CODE,
        "Employment": "Employed",
        "Currency": "EUR European Euro",
        "Compensation": 50_000.0,
    }
    base.update(modifs)
    return base


def test_definir_population_filtres_et_bornes():
    df = pd.DataFrame(
        [
            ligne(),                                     # gardé
            ligne(Compensation=15_000.0),                # gardé : borne basse incluse
            ligne(Compensation=200_000.0),               # gardé : borne haute incluse
            ligne(Country="Germany"),                    # autre pays
            ligne(CodeMain="I create code occasionally"),
            ligne(Employment="Student"),
            ligne(Currency="USD United States dollar"),
            ligne(Currency=None),                        # devise manquante
            ligne(Compensation=None),                    # salaire manquant
            ligne(Compensation=54.0),                    # sous la borne basse
            ligne(Compensation=320_000.0),               # au-dessus de la borne haute
        ]
    )

    pop = definir_population(df)

    assert len(pop) == 3
    assert sorted(pop["SalaireEUR"]) == [15_000.0, 50_000.0, 200_000.0]
    assert (pop["SalaireEUR"] == pop["Compensation"]).all()
    assert "SalaireEUR" not in df.columns  # le DataFrame d'origine n'est pas modifié


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
