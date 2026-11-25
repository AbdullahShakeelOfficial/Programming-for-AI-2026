# Outreach Contact Policy, Evaluation & Management Recommendation

## 1. Contact Allocation & Ranking Rule
* **Capacity & Budget:** At cutoff $C$, select $B = \min(200, \lfloor 0.10 \times N \rfloor)$ unique eligible UK customers ($B = 200$ at both August and September cutoffs; cost $= £2 \times 200 = £400$).
* **Segment Quotas:** Map k-Means clusters ($k=4$, fit on `log1p` + `StandardScaler` RFM) deterministically by median profile order:
  * **Core Champions** (highest median Monetary): **50%** ($100$ contacts)
  * **At-Risk Established Buyers** (mid-high Monetary/Frequency, longer Recency): **25%** ($50$ contacts)
  * **Recent Promising Buyers** (lowest Recency, lower Frequency/Monetary): **20%** ($40$ contacts)
  * **Dormant / One-Time Buyers** (highest Recency, lowest Frequency/Monetary): **5%** ($10$ contacts)
* **Within-Cluster Ranking & Tie-Breaking:** Rank descending by `Monetary`, ascending by `Recency`, descending by `Frequency`, and ascending by `CustomerID`. If any cluster contains fewer customers than its quota, redistribute unused slots sequentially (`Champions -> At-Risk -> Recent -> Dormant`).
* **Zero-Denominator Safeguard:** All rate and share ratios return `0.0` explicitly when the denominator (`Selected_Count` or `Total_Cohort_Spend`) equals zero.

## 2. Development (Aug 2011) & Untouched Final (Sept 2011) Results

| Stage & Policy | Selected ($B$) | Cost (£) | Repeat Buyers | Repeat Rate | Captured Spend (£) | Spend / Contact (£) | Cohort Spend Share | Clusters Covered |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Dev: Baseline (Top Monetary)** | 200 | £400 | 147 | 73.50% | £226,249.94 | £1,131.25 | 51.34% | N/A |
| **Dev: Cluster Policy ($k=4$)** | 200 | £400 | 110 | 55.00% | £182,682.17 | £913.41 | 41.46% | 4 / 4 |
| **Final: Baseline (Top Monetary)** | 200 | £400 | 146 | 73.00% | £336,982.52 | £1,684.91 | 51.24% | N/A |
| **Final: Cluster Policy ($k=4$)** | 200 | £400 | 118 | 59.00% | £319,367.13 | £1,596.84 | 48.56% | 4 / 4 |

## 3. Concrete Policy Tradeoff Example
* **`CustomerID 12749`** (`Recency = 31 days`, `Frequency = 3`, `Monetary = £2,755.23`, assigned to `At_Risk_Established` at September cutoff) is selected at **Rank #127** by the Cluster Policy because she is a high-value multi-order buyer whose 31-day inactivity places her at risk of churn, whereas the pure Monetary baseline excludes her in favor of higher-spend accounts above £2,755.23. This illustrates the core tradeoff: sacrificing immediate organic spend concentration (`£1,596.84` vs `£1,684.91` per contact) to cover all 4 behavioral segments.

## 4. Management Recommendation & Causal Interpretation Limits
* **Recommendation:** **Deploy the simple Top-Monetary baseline** for standard monthly outreach, paired with a **small controlled A/B pilot** on `At_Risk_Established` accounts. In untouched September evaluation, the Top-Monetary baseline achieved a higher repeat purchase rate (`73.0%` vs `59.0%`) and higher captured spend share (`51.24%` vs `48.56%`) with lower operational complexity.
* **Causal Limits & Controlled Pilot Design:** Because no customers were randomly assigned to receive or not receive contact in the UCI dataset, September purchasing reflects *organic baseline buying*, not causal campaign uplift (high-Monetary customers naturally buy again even without outreach). A valid pilot must randomly split eligible customers within each cluster into a **Treatment group** (contacted, £2/customer) and a **Holdout Control group** (not contacted) to measure net incremental revenue lift minus contact cost.