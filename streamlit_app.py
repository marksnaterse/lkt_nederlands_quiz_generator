"""Streamlit entry point voor de quiz generator."""

import streamlit as st

from src.quiz_generator import load_quiz, run_quiz


def main() -> None:
    st.set_page_config(page_title="Quiz Generator", layout="wide")
    st.title("Quiz Generator")

    # Kies een JSON-bestand uit de data-folder
    import glob
    from pathlib import Path

    data_dir = Path("data")
    files = sorted([p.name for p in data_dir.glob("*.json")])

    if not files:
        st.error("Geen JSON-bestanden gevonden in de data-map.")
        return

    # Gebruik standaard alle data-bestanden, of kies één bestand
    single_file = st.checkbox(
        "Gebruik slechts één bestand",
        value=False,
        help="Laat uitgevinkt voor gebruik van alle JSON-bestanden in de data-map.",
    )

    if single_file:
        chosen_file = st.selectbox("Kies quizbestand", options=files)
        quiz = load_quiz(data_dir / chosen_file)
    else:
        quiz = []
        for file in files:
            quiz.extend(load_quiz(data_dir / file))

    # Optie: vaste volgorde of random
    fixed_order = st.checkbox("Vaste volgorde (geen shuffle)", value=False)

    # Extract available domeinen (as strings) from de quiz data
    domains = sorted({str(q.get("domain")) for q in quiz if q.get("domain") is not None})
    selected_domains = st.multiselect(
        "Domeinen (optioneel)",
        options=domains,
        help="Laat leeg om alle vragen te gebruiken",
    )

    if selected_domains:
        quiz = [q for q in quiz if str(q.get("domain")) in selected_domains]
        if not quiz:
            st.warning("Geen vragen gevonden voor de geselecteerde domeinen.")

    run_quiz(quiz, fixed_order=fixed_order)


if __name__ == "__main__":
    main()
