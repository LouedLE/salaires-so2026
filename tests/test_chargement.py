import pytest

from salaires.chargement import COLONNES_UTILES, charger_brut


def test_charger_brut_garde_les_colonnes_utiles():
    df = charger_brut(2026)
    assert set(df.columns) == set(COLONNES_UTILES)
    assert len(df) > 0


def test_charger_brut_erreur_claire_si_fichier_absent():
    with pytest.raises(FileNotFoundError, match="telecharger_donnees"):
        charger_brut(1900)
