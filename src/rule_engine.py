import json
import re

def load_rules():
    with open("data/company_rules.json", "r") as f:
        return json.load(f)

def extract_sentence(text, target):
    """Utility to extract the surrounding sentence containing a keyword."""
    sentences = re.split(r'\.\s+|\n+', text)
    for s in sentences:
        if target.lower() in s.lower():
            return s.strip()
    return "Clause found in document"

def analyze_lease(text):
    rules = load_rules()

    matches = []
    deviations = []
    missing = []
    prohibited = []

    # 1. Security Deposit Check
    deposit_match = re.search(r'(\d+)\s*months', text.lower())
    if deposit_match:
        deposit = int(deposit_match.group(1))
        evidence = extract_sentence(text, "months")
        
        if deposit <= rules["max_deposit_months"]:
            matches.append({
                "finding": f"Deposit ({deposit} months) is within limit",
                "evidence": evidence
            })
        else:
            deviations.append({
                "finding": f"Deposit ({deposit} months) exceeds limit ({rules['max_deposit_months']})",
                "evidence": evidence
            })

    # 2. Notice Period Check (Step 1)
    notice_match = re.search(r'(\d+)\s*days', text.lower())
    if notice_match:
        days = int(notice_match.group(1))
        evidence = extract_sentence(text, "days")
        min_days = rules.get("notice_period_min", 30)
        max_days = rules.get("notice_period_max", 60)

        if min_days <= days <= max_days:
            matches.append({
                "finding": f"Notice Period ({days} days) is within company standard ({min_days}-{max_days} days)",
                "evidence": evidence
            })
        else:
            deviations.append({
                "finding": f"Notice Period ({days} days) is outside company standard ({min_days}-{max_days} days)",
                "evidence": evidence
            })

    # 3. Required Clauses Check
    for clause in rules["required_clauses"]:
        if clause.lower() not in text.lower():
            missing.append({
                "finding": f"Missing required clause: '{clause}'",
                "evidence": "N/A (Clause not found in lease)"
            })

    # 4. Prohibited Terms Check
    for term in rules["prohibited_terms"]:
        if term.lower() in text.lower():
            evidence = extract_sentence(text, term)
            prohibited.append({
                "finding": f"Prohibited term detected: '{term}'",
                "evidence": evidence
            })

    # Recommendation Logic
    recommendation = "Human legal review required." if (deviations or missing or prohibited) else "Agreement matches standards."

    return {
        "matches": matches,
        "deviations": deviations,
        "missing": missing,
        "prohibited": prohibited,
        "recommendation": recommendation
    }