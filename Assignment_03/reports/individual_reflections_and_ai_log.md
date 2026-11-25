# Individual Reflections & AI Assistance Log (SAP ID: 72405)

## Part 1: Own Words Questions (40–60 Words Each)

* **Question A (Why highest past spending may not be best to contact):**
  Contacting only top past spenders satisfies Sales' short-term revenue goal but violates Account Managers' need to retain emerging or at-risk segments. In our September cohort, top-200 Monetary selection ignores accounts like `CustomerID 12749` (£2,755.23 spend, 31-day recency), risking preventable churn among mid-tier repeat buyers while over-concentrating outreach on organic repeaters. *(53 words)*

* **Question B (How removing cancellations affects Monetary & why state it):**
  Excluding `'C*'` cancellation rows defines `Monetary` strictly as gross positive purchase value (`Quantity > 0`, `UnitPrice > 0`) rather than net revenue or profit after returns. Stating this explicitly in our report prevents Finance from mistaking gross positive spend for net cash collected, especially since UK cancellations/returns totaled substantial negative value in `uk_cancellations_audit.csv`. *(54 words)*

* **Question C (Choosing between highest silhouette vs. actionable lower-score design):**
  We rejected `Raw_StandardScaler` at $k=3$ despite its higher silhouette (`0.5070`) because extreme spenders isolated 24 whales (`£35,154.66` median spend) while lumping 2,824 customers into two coarse groups. Instead, we selected `Log1p_StandardScaler` at $k=4$ (`0.3717` silhouette, `ARI >= 0.9801`), giving Account Managers four balanced, actionable behavioral segments. *(51 words)*

* **Question D (Why higher next-month buying does not prove causal policy impact):**
  Because the UCI Online Retail dataset contains no randomized treatment or control assignments, September purchases reflect natural organic repeat behavior rather than campaign-induced demand. Even though our selected customers spent `£319,367.13` (`59.0%` repeat rate), high-value buyers frequently reorder unprompted; proving incremental sales lift requires a randomized holdout A/B test. *(52 words)*

* **Question E (Why saved k-Means assigns wrong groups if scaler or RFM definitions change):**
  Saved k-Means centroids live in the exact standardized `log1p` coordinate space learned during fitting. If `Monetary` changes from gross positive spend to net spend, or `StandardScaler` means/variances shift, a customer's transformed coordinates move relative to frozen centroids, causing `predict()` to assign distorted or mismatched cluster labels. *(51 words)*

## Part 2: Contribution Statement
* **Author:** Hafiz Abdullah Shakeel (SAP ID: 72405) — Individual submission (100% contribution across problem framing, data audit, RFM pipeline, clustering experiments, out-of-time evaluation, `joblib` serialization, and report).

## Part 3: AI Assistance Log
* **AI Tool & Date:** Gemini (2026-11-25)
* **Purpose:** Clarifying CCP rubric sequencing, debugging `openpyxl`/`uv` environment setup, structuring clean sequential audit/RFM functions, and verifying `joblib` schema checks.
* **Summary & Verification:** Used AI to structure modular pandas/scikit-learn code blocks and markdown templates. Verified every calculation independently via two manual customer transaction audits (`CustomerID` checks), strict unit assertions (unique keys, cutoff timestamps, budget caps), and a full top-to-bottom notebook restart.
* **Key Correction / Investigation:** Investigated a `MatplotlibDeprecationWarning` (`vert=False` deprecated in Matplotlib 3.11) and corrected it to `orientation="horizontal"`, and verified why `Raw_StandardScaler` yielded a higher silhouette (`0.5070`) yet failed business usability due to 24-customer whale isolation.