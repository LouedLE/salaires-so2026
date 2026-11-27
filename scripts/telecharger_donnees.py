"""Télécharge les fichiers de l'enquête Stack Overflow dans data/raw/<année>/.

Usage :
    uv run python scripts/telecharger_donnees.py            # 2026
    uv run python scripts/telecharger_donnees.py --annee 2025

Les fichiers passent par media.githubusercontent.com (Git LFS).
Le lien "raw" classique renvoie un pointeur LFS, pas le CSV.
"""

import argparse
import sys
import urllib.request
from pathlib import Path

BASE = "https://media.githubusercontent.com/media/StackExchange/Survey/main/packages/archive"

FICHIERS = {
    2026: ["survey_results_public.csv", "survey_results_schema.csv"],
    2025: ["results.csv", "schema.csv"],
}

RACINE = Path(__file__).resolve().parents[1]


def telecharger(annee: int, forcer: bool = False) -> None:
    dossier = RACINE / "data" / "raw" / str(annee)
    dossier.mkdir(parents=True, exist_ok=True)
    for nom in FICHIERS[annee]:
        cible = dossier / nom
        if cible.exists() and not forcer:
            print(f"Déjà présent : {cible.relative_to(RACINE)}")
            continue
        url = f"{BASE}/{annee}/{nom}"
        print(f"Téléchargement : {url}")
        temporaire = cible.with_suffix(".part")
        urllib.request.urlretrieve(url, temporaire)
        with open(temporaire, "rb") as f:
            debut = f.read(100)
        if debut.startswith(b"version https://git-lfs"):
            temporaire.unlink()
            sys.exit(f"Erreur : {nom} est un pointeur Git LFS, pas le fichier.")
        temporaire.rename(cible)
        taille = cible.stat().st_size / 1e6
        print(f"OK : {cible.relative_to(RACINE)} ({taille:.1f} Mo)")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--annee", type=int, choices=sorted(FICHIERS), default=2026)
    parser.add_argument("--forcer", action="store_true", help="retélécharge même si présent")
    args = parser.parse_args()
    telecharger(args.annee, args.forcer)


if __name__ == "__main__":
    main()
