# Quiz Generator (Streamlit)

Een eenvoudige quiz generator die een quiz afneemt vanuit een JSON-bestand.

## 🚀 Gebruik

1. Installeer dependencies:

```bash
pip install -r requirements.txt
```

2. Start de app:

```bash
streamlit run streamlit_app.py
```

3. Upload je quiz JSON-bestand of gebruik het voorbeeld in `data/sample_quiz.json`.

4. Selecteer (optioneel) een of meerdere domeinen om mee te testen.

> De vragen en de antwoordopties worden bij elke run willekeurig geshuffled.

## 📄 JSON-formaat

Het JSON-bestand bevat een lijst met vragen. Elke vraag kan een `domain` bevatten. Het formaat kan één van de twee zijn:

### Nieuw (plaats in `choices` als lijst)

```json
[
  {
    "domain": 1,
    "question": "Wat is 2 + 2?",
    "choices": ["3", "4", "5"],
    "answer": 1
  }
]
```

## 🚀 Deployen

Om de app te deployen zodat anderen het kunnen gebruiken, kun je Streamlit Cloud gebruiken:

1. Zorg dat je repository op GitHub staat (zoals gedaan).
2. Ga naar [share.streamlit.io](https://share.streamlit.io).
3. Log in met je GitHub account.
4. Selecteer je repository: `marksnaterse/lkt_nederlands_quiz_generator`.
5. Kies de main branch en `streamlit_app.py` als entry point.
6. Klik op Deploy!

De app zal dan live zijn op een URL zoals `https://lkt-nederlands-quiz-generator.streamlit.app`.

### Oud (gebruik `options` + `correct_answer`)

```json
[
  {
    "domain": 1,
    "question": "Wat is 2 + 2?",
    "options": {"a": "3", "b": "4", "c": "5"},
    "correct_answer": "b"
  }
]
```
