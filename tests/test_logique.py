import pandas as pd

from salaires import logique
from salaires.population import DESCRIPTION


def test_mediane_par_groupe_exclut_les_groupes_sous_le_seuil():
    seuil = logique.SEUIL_N
    df = pd.DataFrame(
        {
            "Groupe": ["A"] * seuil + ["B"] * (seuil - 1),
            "SalaireEUR": list(range(1, seuil + 1)) + [100] * (seuil - 1),
        }
    )
    res = logique.mediane_par_groupe(df, "Groupe")
    assert list(res["Groupe"]) == ["A"]
    assert res.loc[0, "n"] == seuil
    assert res.loc[0, "mediane"] == 15.5


def test_legende_population_par_defaut():
    assert logique.legende_population(371) == (
        f"{DESCRIPTION}, enquête Stack Overflow 2026, n = 371 répondants"
    )


def test_legende_population_description_personnalisee():
    legende = logique.legende_population(
        257, description="Répondants qui renseignent leurs langages"
    )
    assert legende == (
        "Répondants qui renseignent leurs langages, "
        "enquête Stack Overflow 2026, n = 257 répondants"
    )


def test_eclater_choix_multiples_une_ligne_par_choix():
    df = pd.DataFrame(
        {
            "Langages": ["Python;SQL", "Python", None],
            "SalaireEUR": [50000, 40000, 30000],
        }
    )
    res = logique.eclater_choix_multiples(df, "Langages")
    assert list(res["Langages"]) == ["Python", "SQL", "Python"]
    assert list(res["SalaireEUR"]) == [50000, 50000, 40000]
