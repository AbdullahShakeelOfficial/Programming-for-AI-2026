# Debugging Record

## E3. Leakage
* **Problem**: Validation test sets mein data leakage hona aur optimistic scores aana.
* **Cause**: StandardScaler ko CV (Cross-Validation) se pehle poore dataset par fit kar dena[cite: 21, 24].
* **Correction**: StandardScaler ko scikit-learn ki `Pipeline` ke andar rakha gaya. Is tarah scaler sirf har CV fold ke training portion par fit hota hai, aur validation/test rows par sirf learned transformation apply hoti hai[cite: 21, 24].

## E4. Unfair comparison
* **Problem**: Models ke darmiyan comparison fair na hona.
* **Cause**: Alag alag splits, folds, ya `X_test` ko algorithm choose karne ke liye use karna.
* **Correction**: `X_dev` aur `y_dev` ko tamam candidates ke liye use kiya gaya aur identical folds pass kiye gaye. `X_test` ko strictly hide kar ke rakha gaya aur sirf selected model ki final evaluation ke liye ek baar use kiya gaya[cite: 18, 24].

## E5. Metric meaning
* **Problem**: False Positives (FP) aur False Negatives (FN) ke impact ko galat samajhna.
* **Cause**: Class 1 (Spam) aur Class 0 (Legitimate) ki misinterpretation[cite: 24].
* **Correction**: Confirm kiya gaya ke Class 1 ka matlab Spam hai. Is context mein, False Positive ka matlab hai ke ek legitimate (asli) email ko spam samajh kar block kar diya gaya (jo nuksan deh hai), jabke False Negative ka matlab hai ke spam email inbox mein aa gayi[cite: 22, 23, 24].

## E6. Schema mismatch
* **Problem**: Naye data par predict karte waqt errors aana ya galat predictions aana.
* **Cause**: Features ki tarteeb (order) badal jana ya koi column missing hona[cite: 24].
* **Correction**: Model ke sath feature names (57 features) ko bhi joblib file mein save kiya gaya. Predict karne se pehle `aligned = new_email[loaded["features"]]` use kar ke exact training wala order restore kiya gaya[cite: 23, 24].