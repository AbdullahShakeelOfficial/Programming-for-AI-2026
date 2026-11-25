# Part A: Problem Definition, Requirements & Stakeholder Analysis

## 1. Main Decision Question
Does segmenting identified UK online retail customers using scaled RFM k-Means clustering produce a contact priority list that captures higher subsequent monthly purchasing and behavioral diversity than a simple top-Monetary baseline within the strict capacity limit of $B = \min(200, \lfloor 0.10 \times N \rfloor)$ contacts (at £2 per contact, max £400)?

## 2. Customer Eligibility, Objective & Acceptance Criteria
* **Customer Eligibility:** Identified customers (`CustomerID` not null) with `Country == 'United Kingdom'` who have at least one valid positive purchase (`Quantity > 0`, `UnitPrice > 0`, and `InvoiceNo` not starting with `'C'`) dated strictly prior to the cutoff timestamp $C$ (midnight at the start of the cutoff date).
* **Measurable Objective:**
  * **Priority Metric:** Subsequent-month positive purchase value (GBP) per contacted customer and share of total eligible cohort spend captured.
  * **Coverage Metric:** Number of distinct behavioral clusters represented in the $B$ selected contacts (and minimum quota representation per active segment).
  * **Conflict Balance:** Allocate $B$ contact slots proportionally across discovered behavioral segments (with a minimum floor for viable segments) and rank customers within each segment by recent positive Monetary value to balance total revenue potential against segment diversity.
* **Acceptance Criteria:**
  1. Deterministic output: repeated runs produce the exact same ranked list of length $B$ (broken consistently by `CustomerID`).
  2. Zero duplicate `CustomerID` entries and 100% adherence to eligibility and budget rules ($\le B$ contacts, cost $\le £400$).
  3. Zero information leakage: all features, scalers, and clustering models at cutoff $C$ use only transactions `< C`.
  4. Reproducible serialization via `joblib` with schema validation checks.

## 3. Discovering Groups vs. Predicting a Known Label
Discovering groups (**unsupervised clustering**, such as k-Means) partitions unlabeled customers into segments based purely on structural similarity in RFM feature space without ground-truth outcome labels. In contrast, predicting a known label (**supervised classification/regression**) learns a mapping from input features to historical target labels (such as "responded to campaign = Yes/No"). Because this dataset contains no historical campaign contact or response labels, unsupervised grouping is used to uncover distinct purchasing behaviors rather than predicting a pre-defined response class.

## 4. Stakeholder Conflict & Resolution Table

| Stakeholder | Primary Goal / Need | Key Conflict | Design Resolution / Visibility |
| :--- | :--- | :--- | :--- |
| **Sales Team** | Maximize immediate revenue by contacting top historical spenders. | Conflicts with **Account Managers** (who want varied buying patterns, not just top whales) and **Finance** (budget cap). | Rank customers within clusters by Monetary value and weight quotas toward high-value clusters while reserving slots for secondary segments. |
| **Account Managers** | Engage diverse customer profiles (e.g., frequent mid-tier buyers, recent adopters) to build long-term relationships. | Conflicts with **Sales** (concentrating all $B$ slots on top spenders ignores emerging/frequent segments). | Enforce stratified cluster quotas so every non-trivial cluster receives representation, and report cluster coverage explicitly. |
| **Finance Department** | Enforce strict contact cap $B = \min(200, \lfloor 0.10 \times N \rfloor)$ (£2/contact, max £400) and verify ROI over a simple rule. | Conflicts with broad outreach desires of **Sales** and **Account Managers**. | Hard-code exact budget assertions ($\text{count} == B$, $\text{cost} = 2B \le £400$) and benchmark directly against a simple top-Monetary baseline. |
| **Customers** | Receive relevant communication without spam or over-contacting. | Conflicts with aggressive outreach quotas if inactive or single-item buyers are repeatedly targeted. | Restrict eligibility to valid UK buyers, cap outreach to $\le 10\%$ of active cohort ($B$), and log exclusion/selection reasons for auditability. |

## 5. Assumptions, Business Confirmation & Deployment Guardrails
* **What the Data Can Answer:** Historical UK purchasing distributions (Recency, Frequency, Monetary), cancellation/return rates, cluster separation stability, and organic repeat purchase behavior in the evaluation month.
* **What Requires Business Confirmation:** Actual customer contact fatigue, net profit margins (since Monetary measures gross positive revenue before returns/COGS), and true causal uplift from outreach.
* **When NOT to Use the System in Practice:**
  1. If clustering fails to produce stable, interpretable segments (e.g., collapsing into one dominant group and tiny outlier clusters).
  2. If the cluster-based contact policy fails to outperform or match the simple top-Monetary baseline during evaluation.
  3. Outside the UK customer base or if upstream invoice/cancellation definitions change.

## 6. End-to-End Workflow & Information Leakage Controls
1. **Raw Audit & Filtering:** Load `Online Retail.xlsx` $\rightarrow$ verify SHA256 $\rightarrow$ filter `Country == 'United Kingdom'` $\rightarrow$ separate cancellations (`C*`), missing `CustomerID`, duplicates, and non-positive values into `audit.csv`.
2. **Temporal Split (Cutoff $C$):** Strictly filter transactions with `InvoiceDate < C` (1 Aug 2011 for development; 1 Sept 2011 for final assessment). *Dependency:* RFM features cannot be computed until valid positive transactions `< C` are isolated.
3. **RFM Feature Engineering:** Aggregate `Recency` (days since last purchase before $C$), `Frequency` (distinct valid invoices), and `Monetary` (sum of positive GBP spend) per `CustomerID`.
4. **Preprocessing & Clustering (Fit on `< C` Only):** Fit `log1p` + `StandardScaler` and `KMeans` strictly on the training RFM table.
5. **Contact Policy Allocation:** Apply quota allocation and deterministic ranking to output exact $B$ unique `CustomerID`s.
6. **Out-of-Time Evaluation:** Evaluate selected list on `[C, C + 1 month)` transactions without feeding any evaluation metrics back into model/policy tuning.

**Information Leakage Guardrails:**
* Never fit `StandardScaler` or percentile caps across combined pre- and post-cutoff data.
* Never include transactions $\ge C$ when computing Recency, Frequency, or Monetary.
* Freeze all design choices (representation, $k$, quotas, tie-breakers) in Git before inspecting September 2011 evaluation outcomes.