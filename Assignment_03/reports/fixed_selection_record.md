# Fixed Selection & Decision Procedure Record (Committed Prior to Final Assessment)

* **Date Frozen:** 2026-11-25
* **Stage:** End of Part C / Pre-Final Assessment (Before inspecting September 2011 outcomes)
* **Data & Eligibility Rules:**
  * Cohort: `Country == 'United Kingdom'`, non-null `CustomerID` (cast to `str`), exact duplicates removed (`keep='first'`), cancelled invoices (`InvoiceNo.startswith('C')`) excluded, `Quantity > 0`, `UnitPrice > 0`, and `InvoiceDate < Cutoff`.
  * Features: `Recency` (calendar days from last valid purchase to cutoff midnight), `Frequency` (distinct valid positive `InvoiceNo`), `Monetary` (sum of positive `Quantity * UnitPrice` in GBP).
* **Chosen Representation & Clustering Model:**
  * Representation: `np.log1p` followed by `StandardScaler` fit strictly on the cutoff's RFM table.
  * Algorithm: `KMeans(n_clusters=4, random_state=42, n_init=10)`.
  * Rejected Alternatives: `Raw_StandardScaler` (rejected despite higher silhouette `0.5070` at $k=3$ because extreme spenders isolate 24 customers into a whale-only cluster, leaving 2,824 customers coarsely lumped); `Log1p_StandardScaler` at $k=3$ (rejected because $k=4$ improves silhouette from `0.3553` to `0.3717` and separates recent low-frequency buyers from at-risk multi-purchase buyers).
* **Contact Policy Allocation & Ranking Rules (`B = min(200, floor(0.10 * N))`):**
  * **Behavioral Role Mapping (Dynamic on Refit):** Identify segments by centroid/median profile order rather than arbitrary label index:
    1. *Core Champions* (highest median Monetary & Frequency, low Recency): **50% of B** (100 slots)
    2. *At-Risk Established Buyers* (moderate-high Monetary/Frequency, higher Recency): **25% of B** (50 slots)
    3. *Recent Promising Buyers* (low Recency, lower Frequency/Monetary): **20% of B** (40 slots)
    4. *Dormant / One-Time Buyers* (highest Recency, lowest Frequency/Monetary): **5% of B** (10 slots)
  * **Small-Group & Unused-Slot Redistribution:** If any cluster has fewer eligible customers than its quota, take all available customers from that cluster and redistribute unused slots sequentially to the remaining highest-priority segments (*Champions* $\rightarrow$ *At-Risk* $\rightarrow$ *Recent* $\rightarrow$ *Dormant*).
  * **Within-Cluster Ranking & Deterministic Tie-Breaker:** Rank customers within each cluster by `Monetary` descending, then `Recency` ascending, then `Frequency` descending, and finally `CustomerID` ascending as an exact deterministic tie-breaker.
* **Baseline & Main Evaluation Measures:**
  * **Baseline:** Top $B$ eligible customers ranked globally by `Monetary` descending, tie-broken by `CustomerID` ascending.
  * **Evaluation Metrics (Out-of-Time Next Month `[C, C + 1 month)`):** Repeat purchase rate (`%`), positive purchase value per contacted customer (`£`), share of total eligible cohort spend captured (`%`), cluster coverage count, and total contact cost (`£2 * B`).