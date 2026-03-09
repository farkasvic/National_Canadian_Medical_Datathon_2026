# OncoSight: Multimodal pCR Prediction for Breast Cancer

**National Canadian Medical Datathon 2026** · Team 6

Predicting breast cancer response to Neoadjuvant Chemotherapy (NAC) using clinical data and digital pathology.

---

## Overview

We built an end-to-end multimodal deep learning pipeline to predict **pathologic complete response (pCR)** vs partial response in breast cancer patients undergoing NAC. By extracting spatial features (nuclear density, edge complexity, clump count) from Whole Slide Images (WSIs) and fusing them with clinical variables, our Keras neural network outperformed baseline models, demonstrating that integrating digital pathology with clinical history improves predictive accuracy.

### Key Results

| Metric | Value |
|--------|-------|
| **Overall Accuracy** | 78% |
| **Complete Response Precision** | 92% |
| **Partial Response Recall** | 93% |

The model favors sensitivity for partial responses—catching almost all non-responders while occasionally underestimating complete responders—an ideal balance for clinical triage.

---

## Team

Diana Dadkhah Tirani · Gurveer Madurai · Derrick Jaskiel · Rachel Chiu · **Victoria Farkas** · Nandini Krishnan

---

## Project Structure

```
├── app.py                 # Streamlit dashboard (OncoSight)
├── notebooks/
│   ├── eda.ipynb          # Exploratory data analysis & clinical preprocessing
│   ├── feature_extr.ipynb  # WSI patch sampling & OpenCV feature extraction
│   ├── model.ipynb        # Keras model training & evaluation
│   └── Meddata.ipynb      # Presentation & methodology report
├── data/
│   ├── gcs/               # Raw data (place Master_Data_Sheet.csv, T-CAIREM/ here)
│   ├── processed_data.csv # EDA output
│   ├── full_img_extract.* # Merged clinical + image features
│   └── README.md          # Data pipeline documentation
├── models/
│   └── artifacts.pkl      # Trained model + preprocessor
├── assets/                # Figures for reports
├── docs/                  # Exported HTML/PDF reports
├── requirements.txt
└── README.md
```

---

## Pipeline

```
Clinical Data (Master_Data_Sheet.csv)
        │
        ▼
   [EDA Notebook]  →  processed_data.csv
        │
        ├──────────────────────────────┐
        │                              │
        ▼                              ▼
WSI (.tif) paths              processed_data.csv
        │                              │
        ▼                              │
[Feature Extraction]  ←────────────────┘
  (patch sampling, OpenCV)
        │
        ▼
  full_img_extract.csv  (clinical + image features)
        │
        ▼
  [Model Notebook]  →  artifacts.pkl
        │
        ▼
  [OncoSight App]  →  Interactive pCR prediction
```

---

## Setup

### 1. Clone and install dependencies

```bash
git clone https://github.com/yourusername/National_Canadian_Medical_Datathon_2026.git
cd National_Canadian_Medical_Datathon_2026
pip install -r requirements.txt
```

### 2. Add raw data (not in repo)

Place datathon data in `data/gcs/`:

- `data/gcs/Master_Data_Sheet.csv` — Clinical data
- `data/gcs/T-CAIREM/` — Whole Slide Images (`.tif`), organized by NAC ID (e.g. `T-CAIREM/NAC-1/*.tif`)

### 3. Run the pipeline (optional)

To train the model from scratch:

1. **EDA:** Run `notebooks/eda.ipynb` → produces `data/processed_data.csv`
2. **Feature extraction:** Run `notebooks/feature_extr.ipynb` → produces `data/full_img_extract.csv`
3. **Model training:** Run `notebooks/model.ipynb` → produces `models/artifacts.pkl`

The repo includes sample data (`data/partial_img_extract.csv`, `data/full_img_extract.xlsx`) and a pre-trained `models/artifacts.pkl` for quick demos.

---

## Run the App

```bash
streamlit run app.py
```

**OncoSight** accepts:

- **Clinical inputs:** Age, tumor size (cT), ER%, PR%, HER2, cN, Grade, Histology
- **Histology patch:** Upload a biopsy image (`.png`, `.jpg`)

The app extracts image biomarkers (nuclear density, edge complexity, clump count) and predicts pCR probability. If `models/artifacts.pkl` exists, it uses the trained model; otherwise it runs in demo mode with a placeholder prediction.

---

## Tech Stack

- **Python:** pandas, numpy, scikit-learn, OpenCV
- **Deep learning:** TensorFlow/Keras
- **Image I/O:** tifffile, zarr (memory-efficient WSI loading)
- **Visualization:** matplotlib, seaborn, plotly
- **App:** Streamlit

---

## Reports

- **HTML:** [docs/Meddata.html](docs/Meddata.html)
- **PDF:** [docs/Meddata.pdf](docs/Meddata.pdf)

---

## License

MIT License — see [LICENSE](LICENSE).
