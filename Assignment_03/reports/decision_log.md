# Decision Log — Assignment 3 (CCP)

## Entry 1: Pre-Modeling Problem Framing & Design Commitments
* **Date:** 2026-11-25
* **Stage:** Part A (Prior to data modeling and candidate comparison)
* **Decision:**
  1. Restrict analysis strictly to `Country == 'United Kingdom'` records with valid `CustomerID`, `Quantity > 0`, `UnitPrice > 0`, and non-cancelled invoices (`not InvoiceNo.startswith('C')`), logging all excluded rows in `reports/audit.csv` rather than silently dropping them.
  2. Define two strict temporal cutoffs: **2011-08-01 00:00:00** (Development) and **2011-09-01 00:00:00** (Final Assessment), prohibiting any use of October–December 2011 records.
  3. Benchmark `StandardScaler` (raw RFM) vs. `log1p` + `StandardScaler` across $k \in \{2, 3, 4, 5, 6\}$ using silhouette score, inertia (within-representation only), cluster size balance, and business interpretability rather than optimizing a single metric.
  4. Resolve Sales vs. Account Manager tension by designing a quota-allocated cluster contact policy and comparing it directly against a pure top-Monetary baseline within $B = \min(200, \lfloor 0.10 \times N \rfloor)$.