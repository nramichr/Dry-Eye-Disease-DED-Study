from pathlib import Path

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split

data_file = Path(__file__).resolve().parent.parent / "DED Dataset.xlsx"
sheet_name = "DED Dataset"
target_col = "Dry Eye Disease"
feature_cols = [
    "Gender",
    "Age",
    "Height",
    "Weight",
    "Blood pressure",
    "Heart rate",
    "Sleep duration",
    "Sleep quality",
    "Sleep disorder",
    "Wake up during night",
    "Feel sleepy during day",
    "Stress level",
    "Daily steps",
    "Physical activity",
    "Caffeine consumption",
    "Alcohol consumption",
    "Smoking",
    "Medical issue",
    "Ongoing medication",
    "Smart device before bed",
    "Average screen time",
    "Blue-light filter",
    "Discomfort Eye-strain",
    "Redness in eye",
    "Itchiness/Irritation in eye",
]

try:
    df = pd.read_excel(data_file, sheet_name=sheet_name)
except ValueError:
    workbook = pd.ExcelFile(data_file)
    print(f"Sheet '{sheet_name}' not found.")
    print("Available sheets:", workbook.sheet_names)
    raise

missing_cols = [col for col in [target_col, *feature_cols] if col not in df.columns]
if missing_cols:
    print("Missing columns:", missing_cols)
    print("Available columns:", df.columns.tolist())
    raise KeyError("One or more required columns were not found in the dataset.")

model_df = df[[*feature_cols, target_col]].dropna().copy()

X = pd.get_dummies(model_df[feature_cols], drop_first=True)
y = model_df[target_col].astype(str).str.strip()

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y,
)

model = RandomForestClassifier(
    n_estimators=300,
    random_state=42,
    class_weight="balanced",
    n_jobs=-1,
)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

print(f"Rows used: {len(model_df)}")
print(f"Training rows: {len(X_train)}")
print(f"Test rows: {len(X_test)}")
print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
print("\nConfusion matrix:")
print(confusion_matrix(y_test, y_pred))
print("\nClassification report:")
print(classification_report(y_test, y_pred))

import matplotlib.pyplot as plt

feature_importance = pd.DataFrame({
    "Feature": X.columns,
    "Importance": model.feature_importances_
}).sort_values(by="Importance", ascending=False)

top_features = feature_importance.head(10)

print("\nTop 10 Feature Importances:")
print(top_features)

plt.figure(figsize=(10, 6))
plt.barh(top_features["Feature"], top_features["Importance"])
plt.gca().invert_yaxis()
plt.xlabel("Importance")
plt.ylabel("Feature")
plt.title("Top 10 Feature Importances for Dry Eye Disease Prediction")
plt.tight_layout()
plt.show()