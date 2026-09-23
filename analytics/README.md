# Analytics Pipeline

## Execution order

Run `01_eda.ipynb` first, then `02_modeling.ipynb`.

`01_eda.ipynb` contains the only `sns.load_dataset("titanic")` call in the module. It immediately writes the loaded data to `titanic.csv`. The notebook also contains an offline fallback to the committed CSV if the Seaborn network fetch is unavailable.

`02_modeling.ipynb` reads `titanic.csv` with pandas and never reloads the raw online dataset.

## Cleaning strategy

The notebook prints missing percentages before handling them.

The percentage rule is:

- under 5%: drop affected rows;
- 5%–30%: impute;
- above 30%: explicitly decide whether to drop the column or treat missingness as a category.

The standard Titanic dataset has substantial missingness in `deck`, so the notebook treats that high-missing categorical field as a `"missing"` category rather than imputing a fabricated deck. Other features used for modeling are handled by the modeling pipeline itself.

## EDA

Age and fare receive histograms and boxplots. IQR outlier counts are calculated using the exact 1.5×IQR rule. Fare's mean, median and mode are reported and used to describe skewness.

Survival rates are calculated for sex, passenger class, and sex×class using boolean masks.

The correlation matrix contains exactly:

`survived, pclass, age, sibsp, parch, fare`

`adult_male` and `alone` are deliberately excluded because they are derived/redundant flags.

At least four multivariate charts are generated, each followed by a written interpretation in the notebook.

## Modeling

A stratified train/test split is performed before preprocessing because the target is binary and its class proportions should remain comparable between train and test.

Preprocessing is implemented with `ColumnTransformer` and fitted only through the training split:

- numeric: median imputation + StandardScaler;
- categorical: most-frequent imputation + OneHotEncoder.

The same split is used for Logistic Regression, Decision Tree and Random Forest.

The imbalance section compares:

1. baseline;
2. `class_weight="balanced"`;
3. SMOTE applied only to the training fold.

Random Forest tuning uses `GridSearchCV`. The final OOB score is obtained from a `RandomForestClassifier(oob_score=True, ...)` fitted using the selected hyperparameters.

The regression side-task predicts fare from the other available features and reports MAE, RMSE, R² and adjusted R², plus a residual plot and a written heteroscedasticity assessment.

The final classifier recommendation is written from the observed metric values rather than from a single metric alone.

## Artifact

The complete preprocessing + estimator pipeline is saved to:

```text
analytics/artifacts/best_pipeline.joblib
```

The final notebook reloads this combined object and predicts on raw rows to demonstrate end-to-end usability.
