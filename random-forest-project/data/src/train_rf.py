from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split

data_file = Path(__file__).resolve().parent.parent / "DED Dataset.xlsx"
output_file = Path(__file__).resolve().parent.parent / "Top_Factors_Influencing_DED"".png"
sheet_name = "DED Dataset"
target_col = "Dry Eye Disease"
feature_cols = [
    "Gender",
    "Age",
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

feature_importance = pd.DataFrame({
    "Feature": X.columns,
    "Importance": model.feature_importances_
}).sort_values(by="Importance", ascending=False)

top_features = feature_importance.head(10)


def format_feature_label(feature_name: str) -> str:
    label = feature_name.replace("_", " ")
    parts = label.split()

    if parts and parts[-1] in {"Y", "N"}:
        label = f"{' '.join(parts[:-1])}: {'Yes' if parts[-1] == 'Y' else 'No'}"

    if label.startswith("Average screen time "):
        label = label.replace("Average screen time ", "Screen time: ")
    elif label.startswith("Stress level "):
        label = label.replace("Stress level ", "Stress level: ")
    elif label.startswith("Sleep duration "):
        label = label.replace("Sleep duration ", "Sleep duration: ")
    elif label.startswith("Sleep quality "):
        label = label.replace("Sleep quality ", "Sleep quality: ")
    elif label.startswith("Age "):
        label = label.replace("Age ", "Age: ")
    elif label.startswith("Gender "):
        label = label.replace("Gender ", "Gender: ")

    return label.title()


top_features = top_features.assign(
    DisplayFeature=top_features["Feature"].map(format_feature_label),
    ImportancePct=top_features["Importance"] * 100,
)

print("\nTop 10 Feature Importances:")
print(top_features[["DisplayFeature", "ImportancePct"]].rename(
    columns={"DisplayFeature": "Feature", "ImportancePct": "Importance (%)"}
))

fig, ax = plt.subplots(figsize=(11, 6.5))
bars = ax.barh(
    top_features["DisplayFeature"],
    top_features["Importance"],
    color="#2F6B7A",
    edgecolor="#1E4650",
)
ax.invert_yaxis()
ax.xaxis.set_major_formatter(PercentFormatter(xmax=1, decimals=1))
ax.set_xlabel("Influence on Prediction (%)")
ax.set_ylabel("")
ax.set_title("Top Factors Influencing Dry Eye Disease", fontsize=14, pad=15)
ax.grid(axis="x", linestyle="--", linewidth=0.7, alpha=0.4)
ax.set_axisbelow(True)

for bar, importance_pct in zip(bars, top_features["ImportancePct"]):
    ax.text(
        bar.get_width() + 0.002,
        bar.get_y() + bar.get_height() / 2,
        f"{importance_pct:.1f}%",
        va="center",
        fontsize=9,
    )

plt.tight_layout()
plt.savefig(output_file, dpi=300, bbox_inches="tight")
print(f"\nSaved chart to: {output_file}")
plt.show()
