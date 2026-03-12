# Dry Eye Disease (DED) Data Analysis

A data analysis project exploring behavioral, physiological, and demographic factors associated with Dry Eye Disease across a dataset of 20,000 patients. Built in Excel using pivot tables, calculated fields, and charts.

---

## Overview

Dry Eye Disease is a chronic condition where the eyes fail to produce sufficient tears or where tears evaporate too quickly, leading to discomfort, inflammation, and impaired vision. With 65.2% of the study population testing positive, this project investigates what lifestyle and physical factors most correlate with a DED diagnosis.

---

## Dataset

| Detail | Info |
|---|---|
| Source | https://www.kaggle.com/datasets/dakshnagra/dry-eye-disease/data |
| Rows | 20,000 patients |
| Columns | 26 features |
| Age Range | 18 to 45 |
| Gender Split | ~50/50 (M/F) |

**Key columns used:**
- `Dry Eye Disease` — Primary outcome variable (Y/N)
- `Average screen time` — Daily device usage in hours
- `Physical activity` — Weekly activity in minutes
- `Height` / `Weight` — Used to derive BMI
- `Stress level` — Self-reported scale of 1 to 5
- `Age` — Grouped into 18-25, 26-35, 36-45

---

## Focus Areas

This analysis was scoped to four key components:

### 1. DED Prevalence & Demographics
- 13,037 out of 20,000 patients diagnosed (65.2%)
- Female patients show a slightly higher rate (66.0%) compared to males (64.4%)
- DED occurrence is consistent across all age groups, suggesting lifestyle factors outweigh age as a driver

### 2. Screen Time & Digital Habits
- Patients using screens 8-10 hours daily show the highest DED occurrence
- The gap between positive and negative cases widens at heavier screen usage levels
- Blue-light filter adoption and smart device use before bed were also examined

### 3. Physical Activity & BMI
- BMI was derived using the formula: `Weight (kg) / (Height (cm) / 100)²`
- DED positive patients in the 26-35 age group averaged the highest BMI at 25.12
- Both underweight and obese BMI categories showed elevated DED rates compared to the normal range
- Physical activity levels showed minimal variation between positive and negative cases

### 4. Stress & Mental Wellbeing
- Stress level 5 (Very High) corresponded with the highest DED rate at 65.9%
- Stress level 2 (Low) showed the lowest at 64.4%
- While variation is modest, the upward trend at higher stress levels is consistent

---

## Tools Used

- **Microsoft Excel** — Pivot tables, calculated columns, and charting
- **Random Forest (Planned)** — Predictive modeling to classify DED likelihood based on behavioral and physiological features

---

## Key Calculated Fields

| Field | Formula |
|---|---|
| BMI | `=Weight / (Height/100)^2` |
| DED Rate per Group | `DED Positive Count / Total in Group` |
| Share of Total DED | `DED Positive Count / 13,037` |

> Note: Rates are calculated against the **total patients within each group**, not the full 20,000, to accurately reflect risk within each segment.

---

## Charts

| Chart | Type | X Axis | Y Axis |
|---|---|---|---|
| DED Rate by Age Group | Bar | Age Group | Count of DED Positive |
| DED by Daily Screen Time | Grouped Bar | Screen Time Bucket | Count (Positive & Negative) |
| Average BMI by Age Group and DED Status | Grouped Bar | Age Group | Average BMI |
| DED by Stress Level | Bar | Stress Level (1-5) | Count |

---

## Findings Summary

- Screen time is the strongest behavioral indicator, with the 8-10 hour group consistently showing the widest gap between positive and negative cases
- BMI extremes (underweight and obese) are associated with higher DED occurrence than the normal range
- Stress level has a moderate upward relationship with DED, most notable at level 5
- Age alone does not appear to be a strong predictor within the 18-45 range studied

---

## Planned: Random Forest Model

A Random Forest classifier will be trained on the dataset to predict DED likelihood based on the key features identified in this analysis. Expected inputs include screen time, BMI, stress level, physical activity, age, and gender. The goal is to move beyond descriptive statistics and build a model that can flag high-risk individuals based on their behavioral and physiological profile.

---

## Notes

- The dataset reflects a snapshot in time and is not longitudinal
- DED diagnosis (Y/N) is binary; severity levels are not captured
- Correlation observed in this analysis does not imply causation
