# Data Directory

This directory contains processed datasets and intermediate outputs from the pipeline.

## Structure

- `gcs/` — Place raw data here (not in repo):
  - `Master_Data_Sheet.csv` — Clinical data from the datathon
  - `T-CAIREM/` — Whole Slide Images (`.tif` files) organized by NAC ID
- `processed_data.csv` — Output from EDA notebook (clinical data after imputation)
- `image_extr_df.csv` — Image features extracted from WSIs
- `full_img_extract.csv` — Merged clinical + image features (input to model)
- `partial_img_extract.csv` — Subset of image features (sample)
- `full_img_extract.xlsx` — Excel version of full merged dataset

## Pipeline Order

1. `Master_Data_Sheet.csv` → EDA → `processed_data.csv`
2. `processed_data.csv` + WSIs → Feature Extraction → `full_img_extract.csv`
3. `full_img_extract.csv` → Model Training → `models/artifacts.pkl`
