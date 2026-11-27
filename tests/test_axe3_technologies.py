import pandas as pd

from salaires.axes.axe3_technologies import mediane_par_langage, population_langages
from salaires.logique import SEUIL_N


def repondants(langages, salaire, nombre):
    return [{"LanguagesHaveWorkedWith": langages, "SalaireEUR": salaire}] * nombre


def test_population_garde_ceux_qui_indiquent_un_langage():
    df = pd.DataFrame(repondants("Python;SQL", 50_000, 2) + repondants(None, 40_000, 1))
    assert len(population_langages(df)) == 2


def test_mediane_par_langage_compte_chaque_langage_coche():
    df = pd.DataFrame(
        repondants("Go;Python", 60_000, SEUIL_N)
        + repondants("Python", 40_000, SEUIL_N)
        + repondants("Rust", 90_000, 5)
    )
    tableau = mediane_par_langage(df).set_index("LanguagesHaveWorkedWith")

    assert list(tableau.index) == ["Go", "Python"]  # Rust, sous le seuil, est retiré
    assert tableau.loc["Python", "n"] == 2 * SEUIL_N  # compté dans ses deux groupes
    assert tableau.loc["Python", "mediane"] == 50_000
    # Médiane de l'axe : 60 000 € (65 répondants), donc Go à 0 % et Python à -16,7 %.
    assert tableau.loc["Go", "ecart_pct"] == 0
    assert round(tableau.loc["Python", "ecart_pct"], 1) == -16.7
