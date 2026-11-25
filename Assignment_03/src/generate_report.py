from pathlib import Path
import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, HRFlowable
)

# Resolve Assignment_03 directory cleanly whether run from src/ or notebooks/
HERE = Path(__file__).resolve().parent if "__file__" in globals() else Path.cwd()
BASE_DIR = HERE.parent if HERE.name in {"src", "notebooks"} else (HERE / "Assignment_03" if (HERE / "Assignment_03").exists() else HERE)

REPORTS_DIR = BASE_DIR / "reports"
FIGURES_DIR = BASE_DIR / "figures"
OUT_PDF = BASE_DIR / "report.pdf"

doc = SimpleDocTemplate(
    str(OUT_PDF),
    pagesize=A4,
    leftMargin=16 * mm,
    rightMargin=16 * mm,
    topMargin=15 * mm,
    bottomMargin=15 * mm,
)

styles = getSampleStyleSheet()
title_style = ParagraphStyle(
    "ReportTitle", parent=styles["Title"], fontName="Helvetica-Bold", fontSize=15,
    leading=19, textColor=colors.black, spaceAfter=4, alignment=0
)
subtitle_style = ParagraphStyle(
    "ReportSub", parent=styles["Normal"], fontName="Helvetica", fontSize=9.5,
    leading=13, textColor=colors.HexColor("#222222"), spaceAfter=8
)
h1_style = ParagraphStyle(
    "H1Custom", parent=styles["Heading1"], fontName="Helvetica-Bold", fontSize=12,
    leading=15, textColor=colors.black, spaceBefore=8, spaceAfter=4
)
h2_style = ParagraphStyle(
    "H2Custom", parent=styles["Heading2"], fontName="Helvetica-Bold", fontSize=10,
    leading=13, textColor=colors.black, spaceBefore=6, spaceAfter=3
)
body_style = ParagraphStyle(
    "BodyCustom", parent=styles["Normal"], fontName="Helvetica", fontSize=9,
    leading=12.5, textColor=colors.black, spaceAfter=5
)
bullet_style = ParagraphStyle(
    "BulletCustom", parent=body_style, leftIndent=12, firstLineIndent=-8, spaceAfter=3
)

def make_table(data, col_widths=None, font_size=7.8):
    tbl = Table(data, colWidths=col_widths, repeatRows=1)
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#EAEAEA")),
        ("TEXTCOLOR", (0, 0), (-1, -1), colors.black),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), font_size),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#444444")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 3.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3.5),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
    ]))
    return tbl

def df_to_table(df, round_digits=2, col_widths=None, font_size=7.5):
    df_disp = df.copy()
    for col in df_disp.select_dtypes(include="number").columns:
        df_disp[col] = df_disp[col].round(round_digits)
    rows = [list(df_disp.columns)] + df_disp.astype(str).values.tolist()
    return make_table(rows, col_widths=col_widths, font_size=font_size)

def add_image(img_path, width_mm=170, height_mm=78):
    if img_path.exists():
        img = Image(str(img_path), width=width_mm * mm, height=height_mm * mm)
        img.hAlign = "CENTER"
        return img
    return Paragraph(f"[Missing figure: {img_path.name}]", body_style)

story = []

# ==================== PAGE 1: MANAGEMENT SUMMARY ====================
story.append(Paragraph("Customer Segmentation and Contact Priorities for an Online Retailer", title_style))
story.append(Paragraph(
    "<b>Student:</b> Hafiz Abdullah Shakeel &nbsp;|&nbsp; <b>SAP ID:</b> 72405 &nbsp;|&nbsp; "
    "<b>Course:</b> Programming for AI (Assignment No. 3 — CCP)<br/>"
    "<b>Institution:</b> Riphah International University, Faculty of Computing &nbsp;|&nbsp; <b>Date:</b> 25 November 2026",
    subtitle_style
))
story.append(HRFlowable(width="100%", thickness=1, color=colors.black, spaceAfter=8))

story.append(Paragraph("1. Executive Management Summary", h1_style))
story.append(Paragraph(
    "<b>Decision Question:</b> Does segmenting identified UK online retail customers via scaled RFM k-Means clustering "
    "produce a contact priority list that outperforms a simple top-Monetary baseline within the operational limit of "
    "<i>B</i> = min(200, floor(0.10 &times; <i>N</i>)) contacts (£2 per contact, £400 maximum budget) when evaluated on "
    "subsequent monthly purchasing?", body_style
))
story.append(Paragraph(
    "<b>Cohort &amp; Methodology:</b> Using the UCI Online Retail dataset (DOI: 10.24432/C5BW33), transactions were filtered "
    "strictly to identified United Kingdom customers with valid positive purchases (Quantity &gt; 0, UnitPrice &gt; 0, non-cancelled). "
    "All design choices—log1p transformation, StandardScaler, k-Means (<i>k</i> = 4, seed = 42), and stratified segment quotas—"
    "were developed exclusively on transactions prior to <b>1 August 2011</b> (<i>N</i> = 2,848, <i>B</i> = 200) and frozen in Git "
    "prior to refitting on transactions before <b>1 September 2011</b> (<i>N</i> = 2,989, <i>B</i> = 200).", body_style
))

summary_table_data = [
    ["Evaluation Stage & Policy", "Contacts (B)", "Cost (£)", "Repeat Rate", "Captured Spend (£)", "Spend / Contact", "Cohort Share", "Clusters"],
    ["Dev (Aug 2011): Top-Monetary Baseline", "200", "£400", "73.50%", "£226,249.94", "£1,131.25", "51.34%", "N/A"],
    ["Dev (Aug 2011): Cluster Policy (k=4)", "200", "£400", "55.00%", "£182,682.17", "£913.41", "41.46%", "4 / 4"],
    ["Final (Sept 2011): Top-Monetary Baseline", "200", "£400", "73.00%", "£336,982.52", "£1,684.91", "51.24%", "N/A"],
    ["Final (Sept 2011): Cluster Policy (k=4)", "200", "£400", "59.00%", "£319,367.13", "£1,596.84", "48.56%", "4 / 4"],
]
story.append(make_table(summary_table_data, font_size=7.6))
story.append(Spacer(1, 5))

story.append(Paragraph(
    "<b>Key Findings &amp; Management Recommendation:</b> While log1p + StandardScaler k-Means (<i>k</i> = 4) discovers four stable, "
    "interpretable UK customer segments (ARI &ge; 0.9801 across random seeds) and achieves 100% segment coverage (4/4 clusters), "
    "the simple <b>Top-Monetary baseline</b> outperforms the cluster-quota policy in both untouched September repeat purchase rate "
    "(<b>73.00% vs. 59.00%</b>) and captured cohort spend (<b>£336,982.52 vs. £319,367.13</b>; 51.24% vs. 48.56% share). "
    "<b>Recommendation:</b> Deploy the simple Top-Monetary rule for immediate monthly outreach to maximize revenue efficiency, "
    "and run a small randomized controlled A/B pilot on <i>At-Risk Established</i> customers (such as CustomerID 12749) to measure "
    "true causal contact uplift before deploying cluster-based outreach in production.", body_style
))
story.append(PageBreak())

# ==================== PAGE 2: PART A ====================
story.append(Paragraph("2. Part A: Problem Definition, Stakeholders &amp; Workflow", h1_style))
story.append(Paragraph(
    "<b>Customer Eligibility &amp; Acceptance Criteria:</b> Eligible customers must have Country == 'United Kingdom', a non-null "
    "CustomerID, and at least one non-cancelled positive purchase line (Quantity &gt; 0, UnitPrice &gt; 0) strictly before cutoff <i>C</i>. "
    "Acceptance requires deterministic ranking (CustomerID tie-breaker), zero duplicates, strict capacity compliance (<i>B</i> &le; 200, "
    "cost &le; £400), zero future data leakage, and a verified joblib workflow bundle.", body_style
))
story.append(Paragraph(
    "<b>Unsupervised Grouping vs. Supervised Prediction:</b> Unsupervised clustering (k-Means) partitions unlabeled customers by "
    "geometric similarity in scaled RFM space because the dataset contains no historical contact treatment or response labels. "
    "Supervised classification requires known target labels to learn a predictive mapping.", body_style
))

stakeholder_data = [
    ["Stakeholder", "Primary Objective", "Conflict Identified", "Design Resolution"],
    ["Sales Team", "Prioritize highest historical spenders for immediate revenue.", "Conflicts with Account Managers (diversity) and Finance (£400 cap).", "Rank within clusters by Monetary descending; weight Core Champions at 50%."],
    ["Account Managers", "Cover diverse buying behaviors (emerging & at-risk buyers).", "Conflicts with Sales' concentration on top spenders.", "Enforce stratified quotas across all 4 clusters and track cluster coverage."],
    ["Finance Dept.", "Enforce B <= 200 (£400 cap) and verify ROI over simple rules.", "Limits total outreach slots available to Sales & Account Managers.", "Hard-assert exact budget limits and benchmark head-to-head vs. baseline."],
    ["Customers", "Avoid spam and receive relevant, timely communication.", "Over-contacting low-intent or inactive buyers causes fatigue.", "Cap outreach at <= 10% of active cohort and log explicit selection reasons."],
]
story.append(make_table(stakeholder_data, col_widths=[28*mm, 45*mm, 48*mm, 55*mm], font_size=7.6))
story.append(Spacer(1, 5))

story.append(Paragraph("<b>Assumptions, Scope Limits &amp; Information Leakage Guardrails:</b>", h2_style))
story.append(Paragraph("&bull; <b>Scope &amp; Assumptions:</b> Conclusions apply strictly to UK customers. Monetary measures gross positive spend in GBP, not net profit after returns or COGS. System deployment is contraindicated if clusters collapse into outlier micro-groups or fail to beat the baseline.", bullet_style))
story.append(Paragraph("&bull; <b>End-to-End Dependency &amp; Leakage Prevention:</b> Raw Audit &rarr; UK &amp; Cutoff Filter (&lt; <i>C</i>) &rarr; RFM Aggregation &rarr; Fit log1p + StandardScaler + KMeans (&lt; <i>C</i> only) &rarr; Quota Allocation &rarr; Out-of-Time Evaluation [<i>C</i>, <i>C</i>+1m). Scalers, percentile caps, and model parameters are never fit on post-cutoff data, and all design choices were committed to Git before viewing September 2011 transactions.", bullet_style))
story.append(PageBreak())

# ==================== PAGE 3: PART B ====================
story.append(Paragraph("3. Part B: Data Audit, RFM Engineering &amp; Manual Verification", h1_style))
story.append(Paragraph(
    "A sequential waterfall audit reconciled all 541,909 raw transaction rows so multi-rule rows were counted once without double-counting. "
    "Cancellations ('C*') and negative returns were preserved separately in <i>reports/uk_cancellations_audit.csv</i>. "
    "InvoiceNo, CustomerID, and Country were excluded from clustering features because identifiers carry no behavioral distance and Country is constant.", body_style
))

audit_path = REPORTS_DIR / "audit.csv"
if audit_path.exists():
    audit_df = pd.read_csv(audit_path)
    story.append(df_to_table(audit_df, round_digits=2, font_size=7.4))
story.append(Spacer(1, 5))

story.append(Paragraph(
    "<b>RFM Definitions &amp; Assertions:</b> For eligible UK customers before cutoff <i>C</i>: <b>Recency</b> = calendar days from latest "
    "valid purchase to cutoff midnight; <b>Frequency</b> = distinct valid positive InvoiceNo count; <b>Monetary</b> = gross positive spend (£). "
    "Assertions verified unique CustomerID rows, zero timestamps &ge; <i>C</i>, and finite non-negative RFM values across both cutoffs "
    "(Development <i>N</i> = 2,848; Final <i>N</i> = 2,989). Two individual customer histories (one with a cancelled invoice and one clean) "
    "were manually audited line-by-line and confirmed to match <i>build_rfm_features()</i> identically.", body_style
))
story.append(add_image(FIGURES_DIR / "part_b_rfm_distributions.png", width_mm=172, height_mm=84))
story.append(PageBreak())

# ==================== PAGES 4-5: PART C ====================
story.append(Paragraph("4. Part C: Clustering Investigation &amp; Model Selection", h1_style))
story.append(Paragraph(
    "We compared <b>Raw + StandardScaler</b> against <b>log1p + StandardScaler</b> across <i>k</i> &in; {2, 3, 4, 5, 6} (random_state=42, n_init=10) "
    "on the 2,848 Development customers. Raw Euclidean scaling allows extreme spenders (&gt;£35,000) to dominate distances, isolating 24 whales "
    "into a tiny cluster while lumping 2,824 customers into two coarse groups. Applying <i>log1p</i> compresses right-skewness so all three RFM "
    "dimensions contribute proportionally.", body_style
))

cand_path = REPORTS_DIR / "candidate_results.csv"
if cand_path.exists():
    cand_df = pd.read_csv(cand_path)
    story.append(df_to_table(cand_df, round_digits=4, font_size=7.2))
story.append(Spacer(1, 5))

prof_path = REPORTS_DIR / "shortlisted_profiles.csv"
if prof_path.exists():
    prof_df = pd.read_csv(prof_path)
    story.append(Paragraph("<b>Shortlisted Original-Unit Profiles (Means &amp; Medians):</b>", h2_style))
    story.append(df_to_table(prof_df, round_digits=2, font_size=7.0))
story.append(Spacer(1, 4))
story.append(add_image(FIGURES_DIR / "part_c_candidate_metrics.png", width_mm=172, height_mm=54))
story.append(PageBreak())

story.append(Paragraph("4.2 Seed Stability, Sensitivity Study &amp; PCA Visualization", h1_style))
story.append(Paragraph(
    "<b>Selection Justification &amp; Stability:</b> We selected <b>Log1p_StandardScaler with <i>k</i> = 4</b> (Silhouette = 0.3717, higher than "
    "<i>k</i> = 3 at 0.3553) because it separates four actionable segments: Core Champions (<i>n</i>=377, Med M=£2,997.75), Dormant/One-Time "
    "(<i>n</i>=1,224, Med R=130d), Recent Promising (<i>n</i>=453, Med R=13d, F=2), and At-Risk Established (<i>n</i>=794, Med R=63d, F=3). "
    "Across seeds {1, 10, 21, 100} vs. seed 42, Adjusted Rand Index (ARI) remained &ge; 0.9801 (though seed agreement alone only confirms "
    "optimization stability on fixed data, not external validity). Capping Monetary at the 99th percentile confirmed robust segment structure "
    "without distorting high-value rankings. The 2D PCA display below explains <b>93.2%</b> of variance (PC1 = 73.5%, PC2 = 19.7%); k-Means was "
    "fit in full 3D standardized log-RFM space, with PCA used strictly for visualization.", body_style
))
story.append(add_image(FIGURES_DIR / "part_c_pca_clusters.png", width_mm=160, height_mm=98))
story.append(PageBreak())

# ==================== PAGE 6: PART D ====================
story.append(Paragraph("5. Part D: Contact Policy, Out-of-Time Evaluation &amp; Causal Limits", h1_style))
story.append(Paragraph(
    "<b>Frozen Policy Design:</b> Prior to inspecting September outcomes, the procedure was committed to Git. Within <i>B</i> = 200 slots (£400 cost), "
    "clusters are mapped dynamically by median profile role and allocated fixed quotas: <b>Core Champions (50%, 100 slots)</b>, "
    "<b>At-Risk Established (25%, 50 slots)</b>, <b>Recent Promising (20%, 40 slots)</b>, and <b>Dormant/One-Time (5%, 10 slots)</b>, "
    "with unused-slot redistribution and deterministic tie-breaking by (Monetary desc, Recency asc, Frequency desc, CustomerID asc).", body_style
))

final_path = REPORTS_DIR / "final_outcomes.csv"
if final_path.exists():
    final_df = pd.read_csv(final_path)
    story.append(df_to_table(final_df, round_digits=4, font_size=7.1))
story.append(Spacer(1, 5))

story.append(Paragraph(
    "<b>Policy Tradeoff Example (CustomerID 12749):</b> In the untouched September assessment, CustomerID 12749 (Recency = 31 days, "
    "Frequency = 3, Monetary = £2,755.23) is selected at Rank #127 under the Cluster Policy (<i>At-Risk Established</i> quota) but missed "
    "by the pure Monetary baseline. Retaining mid-high tier repeat buyers at risk of lapse trades £88.07 in spend per contact (£1,596.84 vs. "
    "£1,684.91) to achieve 4/4 segment coverage.", body_style
))
story.append(Paragraph(
    "<b>Causal Interpretation Limits &amp; Controlled Pilot Design:</b> Higher next-month purchasing among selected customers reflects historical "
    "organic repeat buying, <b>not</b> causal campaign lift, because no customers were randomly assigned to contact vs. holdout groups. "
    "To test true incremental ROI, management should run a randomized controlled pilot splitting each segment 50/50 into Treatment (contacted, "
    "£2/customer) and Control (uncontacted) groups and measure net incremental margin minus outreach cost.", body_style
))

# ==================== PAGE 7: PART E & REFERENCES ====================
story.append(Paragraph("6. Part E: Prototype Verification &amp; References", h1_style))
story.append(Paragraph(
    "<b>Serialization &amp; Validation Checks:</b> The fitted StandardScaler, KMeans (<i>k</i>=4) model, ordered feature schema ['Recency', 'Frequency', 'Monetary'], "
    "cutoff date ('2011-09-01'), and library versions were saved to <i>models/rfm_segmentation_bundle.joblib</i>. Reloading verified 100% identical "
    "cluster labels on all 2,989 final customers. Scoring a new customer profile (Recency=14d, Frequency=5, Monetary=£1,450.00) assigned Cluster 2 "
    "without retraining, while invalid inputs (missing 'Monetary' column and negative Recency = -5) cleanly raised descriptive ValueErrors.", body_style
))
story.append(Paragraph("<b>References:</b>", h2_style))
story.append(Paragraph("1. Seoul Accord (2026). <i>Section D Graduate Attributes, D.4.1 Complex Computing Problems</i>.", bullet_style))
story.append(Paragraph("2. Chen, D. (2015). <i>Online Retail</i>. UCI Machine Learning Repository. https://doi.org/10.24432/C5BW33 (CC BY 4.0).", bullet_style))
story.append(Paragraph("3. Pedregosa et al. (2011). <i>Scikit-learn: Machine Learning in Python</i> (KMeans, StandardScaler, PCA, silhouette_score, adjusted_rand_score).", bullet_style))
story.append(PageBreak())

# ==================== PAGE 8: INDIVIDUAL REFLECTIONS & AI LOG ====================
story.append(Paragraph("7. Individual Reflections &amp; AI Assistance Log (Excluded from Page Limit)", h1_style))
reflections = [
    ("Question A (Why highest past spending may not be best):",
     "Contacting only top past spenders satisfies Sales' short-term revenue goal but violates Account Managers' need to retain emerging or at-risk segments. In our September cohort, top-200 Monetary selection ignores accounts like CustomerID 12749 (£2,755.23 spend, 31-day recency), risking preventable churn among mid-tier repeat buyers while over-concentrating outreach on organic repeaters."),
    ("Question B (How removing cancellations affects Monetary & why state it):",
     "Excluding 'C*' cancellation rows defines Monetary strictly as gross positive purchase value (Quantity > 0, UnitPrice > 0) rather than net revenue or profit after returns. Stating this explicitly in our report prevents Finance from mistaking gross positive spend for net cash collected, especially since UK cancellations/returns totaled substantial negative value in uk_cancellations_audit.csv."),
    ("Question C (Choosing between highest silhouette vs. actionable lower-score design):",
     "We rejected Raw_StandardScaler at k=3 despite its higher silhouette (0.5070) because extreme spenders isolated 24 whales (£35,154.66 median spend) while lumping 2,824 customers into two coarse groups. Instead, we selected Log1p_StandardScaler at k=4 (0.3717 silhouette, ARI >= 0.9801), giving Account Managers four balanced, actionable behavioral segments."),
    ("Question D (Why higher next-month buying does not prove causal policy impact):",
     "Because the UCI Online Retail dataset contains no randomized treatment or control assignments, September purchases reflect natural organic repeat behavior rather than campaign-induced demand. Even though our selected customers spent £319,367.13 (59.0% repeat rate), high-value buyers frequently reorder unprompted; proving incremental sales lift requires a randomized holdout A/B test."),
    ("Question E (Why saved k-Means assigns wrong groups if scaler or RFM definitions change):",
     "Saved k-Means centroids live in the exact standardized log1p coordinate space learned during fitting. If Monetary changes from gross positive spend to net spend, or StandardScaler means/variances shift, a customer's transformed coordinates move relative to frozen centroids, causing predict() to assign distorted or mismatched cluster labels."),
]
for q_title, q_ans in reflections:
    story.append(Paragraph(f"<b>{q_title}</b> {q_ans}", body_style))

story.append(Spacer(1, 4))
story.append(Paragraph("<b>Contribution &amp; AI Assistance Log:</b>", h2_style))
story.append(Paragraph(
    "<b>Author:</b> Hafiz Abdullah Shakeel (SAP ID: 72405) — 100% individual contribution across problem definition, audit, RFM engineering, "
    "clustering evaluation, out-of-time policy testing, joblib verification, and report writing.<br/>"
    "<b>AI Tool &amp; Verification:</b> Gemini (2026-11-25) was used to structure modular pandas/scikit-learn blocks, debug environment setup "
    "(openpyxl/uv), and format report tables. Every calculation was independently verified via two manual customer transaction audits, automated "
    "unit assertions, and a clean top-to-bottom notebook restart. Key correction: resolved a Matplotlib 3.11 deprecation warning (vert=False &rarr; "
    "orientation='horizontal') and rejected high-silhouette raw scaling due to 24-customer whale isolation.", body_style
))

doc.build(story)
print(f"Successfully generated: {OUT_PDF} ({OUT_PDF.stat().st_size / 1024:.1f} KB)")