# Auto-generated from data_clean_notebook.ipynb
# Generated on 2026-03-04T23:41:19


# ---- Cell 1 ----
def run_data_quality_pipeline(path):
    import pandas as pd
    import numpy as np
    import ast, json, re

    NULL_LIKE = {"", " ", "na", "n/a", "nan", "none", "null", "nil", "undefined"}

    # ---------------- SAFE PARSE ----------------
    def safe_parse(val):
        if val is None:
            return {}
        if isinstance(val, (dict, list)):
            return val
        if isinstance(val, float) and pd.isna(val):
            return {}
        if isinstance(val, str):
            s = val.strip()
            if not s or s.lower() in NULL_LIKE:
                return {}
            try:
                return json.loads(s)
            except json.JSONDecodeError:
                pass
            try:
                return ast.literal_eval(s)
            except (ValueError, SyntaxError):
                return {}
        return {}

    # ---------------- BOOL CLEAN ----------------
    def to_bool(x):
        if isinstance(x, bool):
            return x
        if x is None or (isinstance(x, float) and np.isnan(x)):
            return np.nan
        if isinstance(x, (int, float)):
            return bool(x)
        if isinstance(x, str):
            s = x.strip().lower()
            if s in {"true","1","yes","y"}:
                return True
            if s in {"false","0","no","n"}:
                return False
        return np.nan

    # ---------------- CATEGORY CLEAN ----------------
    def clean_cat(cat):
        cat = (cat or "unknown").strip().lower()
        cat = re.sub(r"\s+", "_", cat)
        cat = re.sub(r"[^a-z0-9_]", "", cat)
        return cat or "unknown"

    # ---------------- SPENDING PARSER ----------------
    def parse_spending(val):
        items = val if isinstance(val, list) else safe_parse(val)
        if not isinstance(items, list):
            return {}

        out, amounts, cats = {}, [], set()

        for item in items:
            if not isinstance(item, dict):
                continue

            cat = clean_cat(item.get("category"))
            amt = item.get("amount", 0)

            try:
                amt = float(amt)
            except:
                amt = 0.0

            out[f"spend_{cat}"] = out.get(f"spend_{cat}", 0) + amt
            amounts.append(amt)
            cats.add(cat)

        out["spend_txn_count"] = len(amounts)
        out["spend_total"] = sum(amounts)
        out["spend_mean"] = np.mean(amounts) if amounts else 0
        out["spend_max"] = np.max(amounts) if amounts else 0
        out["spend_unique_cats"] = len(cats)

        return out

    # ---------------- LOAD DATA ----------------
    df = pd.read_json(path)

    # ---------------- FLATTEN JSON ----------------
    applicant_df = pd.json_normalize(df["applicant_info"].apply(safe_parse))
    applicant_df.columns = ["applicant_" + c for c in applicant_df.columns]

    financials_df = pd.json_normalize(df["financials"].apply(safe_parse))
    financials_df.columns = ["fin_" + c for c in financials_df.columns]

    decision_df = pd.json_normalize(df["decision"].apply(safe_parse))
    decision_df.columns = ["decision_" + c for c in decision_df.columns]
    decision_df = decision_df[["decision_loan_approved"]]

    spending_df = pd.DataFrame(
        list(df["spending_behavior"].apply(parse_spending))
    ).fillna(0)

    # ---------------- COMBINE ----------------
    df_clean = pd.concat(
        [
            applicant_df.reset_index(drop=True),
            financials_df.reset_index(drop=True),
            decision_df.reset_index(drop=True),
            spending_df.reset_index(drop=True),
        ],
        axis=1,
    )

    # ---------------- LABEL CLEAN ----------------
    df_clean["decision_loan_approved"] = df_clean["decision_loan_approved"].apply(to_bool)
    df_clean = df_clean.dropna(subset=["decision_loan_approved"])
    df_clean["decision_loan_approved"] = df_clean["decision_loan_approved"].astype(bool)

    # ---------------- NUMERIC CLEAN ----------------
    num_cols = [c for c in df_clean.columns if c.startswith(("fin_", "spend_"))]
    for c in num_cols:
        df_clean[c] = pd.to_numeric(df_clean[c], errors="coerce")

    if "fin_annual_income" in df_clean.columns:
        df_clean.loc[df_clean["fin_annual_income"] <= 0, "fin_annual_income"] = np.nan

    if "fin_credit_history_months" in df_clean.columns:
        df_clean.loc[df_clean["fin_credit_history_months"] < 0, "fin_credit_history_months"] = np.nan

    if "spend_total" in df_clean.columns:
        df_clean.loc[df_clean["spend_total"] < 0, "spend_total"] = np.nan

    # ---------------- REMOVE PII ----------------
    pii_cols = [
        "applicant_full_name",
        "applicant_email",
        "applicant_phone",
        "applicant_address",
        "applicant_ssn",
        "applicant_ip_address",
        "applicant_date_of_birth",
    ]
    df_clean.drop(columns=pii_cols, inplace=True, errors="ignore")

    print("Final dataset shape:", df_clean.shape)

    return df_clean
