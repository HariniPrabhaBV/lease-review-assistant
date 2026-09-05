TRACK_ID=PS05

# Lease Agreement Review Assistant

An intelligent, full-stack legal assistant built with **FastAPI** and **Google Gemini 2.5 Flash**. The application automates lease agreement analysis by combining deterministic rule-based checks with AI-powered plain-language summaries to assist non-lawyer signers and legal teams.

---

## Key Features

- **Deterministic Rule Engine:** Automatically evaluates key parameters like Security Deposit limits, Notice Periods, and Renewal Terms against standard policy baselines.
- **Missing Clause Detection:** Identifies missing standard legal safeguards (e.g., maintenance responsibility, deposit return timeline).
- **Prohibited Term Flagging:** Detects illegal or non-compliant clauses (e.g., non-refundable deposits).
- **Clause Status Dashboard:** Displays an intuitive, color-coded summary table highlighting matches, deviations, and missing items.
- **Gemini AI Plain-Language Summaries:** Generates concise 3-to-4 bullet-point summaries translating complex legal jargon into plain language.
- **Human-in-the-Loop Safeguards:** Strictly provides advisory findings with mandatory legal disclaimers, requiring final human review.

---

## Tech Stack

- **Backend:** Python 3.10+, FastAPI, Uvicorn
- **AI Integration:** Google GenAI SDK (`google-genai`), Gemini 2.5 Flash
- **Frontend & UI:** Jinja2 Templates, HTML5, Bootstrap 5
- **Environment Management:** `python-dotenv`

---

## Project Structure

```text
lease-review-assistant/
├── .env                  #Environmentvariables (GEMINI_API_KEY)
├── app.py                # FastAPI server and routes
├── requirements.txt      # Dependencies
├── README.md             # Project documentation
├── src/
│   └── rule_engine.py    # Rule-based policy checker logic
└── templates/
    ├── index.html        # Upload home page
    └── report.html       # Visual analysis report dashboard