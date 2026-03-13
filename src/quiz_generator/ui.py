"""Streamlit UI voor de quiz."""

import random

import streamlit as st


def _init_quiz_state(quiz: list[dict], fixed_order: bool) -> None:
    """Initialiseer state voor een nieuwe quiz (shuffle, per-vraag data)."""

    st.session_state["_quiz_data"] = quiz
    st.session_state["_fixed_order"] = fixed_order

    order = list(range(len(quiz)))
    if not fixed_order:
        random.shuffle(order)

    st.session_state["_quiz_order"] = order
    st.session_state["_quiz_pos"] = 0
    st.session_state["_quiz_done"] = False
    st.session_state["_quiz_state"] = {}


def _ensure_quiz_state(quiz: list[dict], fixed_order: bool) -> None:
    """Zorg dat quiz state bestaat en opnieuw wordt gegenereerd bij nieuw quiz-bestand of order-keuze."""

    if (
        "_quiz_data" not in st.session_state
        or st.session_state.get("_quiz_data") != quiz
        or st.session_state.get("_fixed_order") != fixed_order
    ):
        _init_quiz_state(quiz, fixed_order)


def _get_question_state(index: int, question: dict) -> dict:
    """Haal of maak het UI-state-object voor een vraag."""

    state = st.session_state["_quiz_state"].get(index)
    if state is not None:
        return state

    raw_choices = question.get("choices") or []
    raw_answer = question.get("answer")

    if not isinstance(raw_choices, list):
        raw_choices = []

    # Bepaal correct antwoord (oude index) en zorg dat we kunnen shufflen
    if isinstance(raw_answer, int) and 0 <= raw_answer < len(raw_choices):
        correct_choice = raw_choices[raw_answer]
    else:
        correct_choice = None

    choices = list(raw_choices)
    random.shuffle(choices)

    state = {
        "choices": choices,
        "correct_choice": correct_choice,
        "answered": False,
        "correct": False,
    }

    st.session_state["_quiz_state"][index] = state
    return state


def run_quiz(quiz: list[dict], fixed_order: bool = False) -> None:
    """Voer de quiz uit in Streamlit."""

    if not quiz:
        st.warning("Geen vragen geladen")
        return

    _ensure_quiz_state(quiz, fixed_order)

    total = len(quiz)
    position = st.session_state["_quiz_pos"]

    # Wanneer alle vragen zijn beantwoord, toon de eindscore + samenvatting
    if st.session_state.get("_quiz_done"):
        _show_summary(quiz)
        if st.button("Opnieuw starten"):
            _init_quiz_state(quiz, fixed_order)
        return

    question_index = st.session_state["_quiz_order"][position]
    question = quiz[question_index]
    question_state = _get_question_state(question_index, question)

    st.markdown(f"### Vraag {position + 1}/{total}")
    st.write(question.get("question", "(geen vraag)"))

    choices = question_state["choices"]
    if not choices:
        st.error("Ongeldige keuzes voor deze vraag")
        return

    # Voeg placeholder toe zodat er geen antwoord vooraf geselecteerd is
    placeholder = "-- kies een antwoord --"
    options = [placeholder] + choices
    select_key = f"select_{question_index}"
    selected = st.radio("Kies een antwoord", options, key=select_key)

    # Zodra er een echte selectie is gemaakt, wordt het antwoord automatisch gecontroleerd
    if selected != placeholder:
        question_state["answered"] = True
        question_state["correct"] = selected == question_state["correct_choice"]

    if question_state["answered"]:
        if question_state["correct"]:
            st.success("✅ Correct!")
        else:
            correct = question_state["correct_choice"] or "(onbekend)"
            st.error(f"❌ Fout. Het juiste antwoord is: {correct}")

    # Volgende knop (of afronden als laatste vraag)
    can_continue = question_state["answered"]

    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if position + 1 < total:
            if st.button("Volgende vraag", disabled=not can_continue):
                st.session_state["_quiz_pos"] = position + 1
                st.rerun()
        else:
            if st.button("Voltooien", disabled=not can_continue):
                st.session_state["_quiz_done"] = True
                st.rerun()
    with col2:
        if st.button("Sla over"):
            st.session_state["_quiz_pos"] = position + 1
            st.rerun()
    with col3:
        if st.button("Stop quiz"):
            st.session_state["_quiz_done"] = True
            st.rerun()
    # Toon voortgang onderaan
    st.markdown("---")
    st.write(f"**Voortgang:** {position + 1}/{total} vragen")


def _show_summary(quiz: list[dict]) -> None:
    """Toon totaalscore en samenvatting per domein."""

    score = 0
    total = len(quiz)

    domain_total: dict[str, int] = {}
    domain_correct: dict[str, int] = {}

    wrong_answers = []

    for idx, question in enumerate(quiz):
        domain = question.get("domain")
        domain_key = str(domain) if domain is not None else "onbekend"
        domain_total[domain_key] = domain_total.get(domain_key, 0) + 1

        state = st.session_state["_quiz_state"].get(idx)
        if state and state.get("answered"):
            if state.get("correct"):
                score += 1
                domain_correct[domain_key] = domain_correct.get(domain_key, 0) + 1
            else:
                wrong_answers.append({
                    "question": question.get("question", "(geen vraag)"),
                    "correct_answer": state.get("correct_choice", "(onbekend)"),
                    "domain": domain_key,
                })

    st.markdown("---")
    st.write(f"**Totaalscore:** {score} / {total}")

    if domain_total:
        rows = []
        for domain_key, total_q in sorted(domain_total.items(), key=lambda item: item[0]):
            correct = domain_correct.get(domain_key, 0)
            pct = (correct / total_q) * 100 if total_q else 0
            rows.append({
                "Domein": domain_key,
                "Score": f"{correct} / {total_q}",
                "%": f"{pct:.0f}%",
            })

        st.subheader("Samenvatting per domein")
        st.table(rows)

    if wrong_answers:
        st.subheader("Foute antwoorden")
        for i, wrong in enumerate(wrong_answers, 1):
            st.write(f"**{i}.** {wrong['question']}")
            st.write(f"   Juiste antwoord: {wrong['correct_answer']}")
            st.write("---")
