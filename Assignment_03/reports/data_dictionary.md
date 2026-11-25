# Data Dictionary & Feature Engineering Specification

## 1. Raw Dataset Fields (UCI Online Retail, DOI: 10.24432/C5BW33)
* **`InvoiceNo`** (`str`): 6-digit integral transaction identifier. Codes starting with `'C'` indicate cancellations and are excluded from positive RFM calculation (logged separately in `uk_cancellations_audit.csv`). Excluded from clustering because nominal IDs do not measure customer similarity.
* **`StockCode`** (`str`): 5-digit product code used for data inspection; excluded from RFM clustering features.
* **`Description`** (`str`): Product name text; excluded from RFM clustering features.
* **`Quantity`** (`int`): Units per transaction line. Only `Quantity > 0` lines qualify as valid positive purchases.
* **`InvoiceDate`** (`datetime64[ns]`): Timestamp of transaction; sorted chronologically and filtered strictly `< cutoff` to prevent future leakage.
* **`UnitPrice`** (`float`): Unit product price in Pounds Sterling (GBP, £). Only `UnitPrice > 0` lines qualify.
* **`CustomerID`** (`str`): 5-digit unique customer identifier. Rows with missing `CustomerID` are reported in `audit.csv` and excluded because they cannot be linked to a customer. Kept only as a table key and deterministic tie-breaker, never as a clustering feature.
* **`Country`** (`str`): Customer country. Filtered strictly to `'United Kingdom'`; constant across the cohort and excluded from clustering features.

## 2. Engineered Customer RFM Features (Computed `< Cutoff C`)
* **`Recency`** (`int`, unit: **days**): Number of calendar days elapsed from the customer's most recent valid positive purchase before cutoff $C$ up to cutoff date $C$ (`00:00:00`). Lower values indicate more recent activity.
* **`Frequency`** (`int`, unit: **distinct invoices**): Count of unique valid positive `InvoiceNo` values for the customer strictly prior to cutoff $C$.
* **`Monetary`** (`float`, unit: **GBP (£)**): Total gross positive purchase value (`sum(Quantity * UnitPrice)`) across all valid positive purchase lines prior to cutoff $C$. Represents gross positive spend, **not** net revenue or profit after returns/cancellations.