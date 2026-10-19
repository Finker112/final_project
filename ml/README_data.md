Dataset Description
Data Source
Simulated New York taxi trip dataset for demonstrating the full MLOps workflow.
Version Notes
v1
Content: Raw dataset with a total of 2000 samples
Features: Contains outliers such as zero-distance and ultra-long trips; missing values exist; no engineered features
Corresponding Git commit: [68bf5e4]
v2
Changes:
Filter out outlier samples where trip distance ≤ 0 or > 30 km
Filter out outlier samples where trip duration < 60 seconds or > 3 hours
Impute missing distance values with median
Add new features: hour and weekday
Corresponding Git commit: [6520796]
Remote Storage
DVC Remote Storage: Azure Blob Storage
Raw data will not be committed to GitHub; only .dvc pointer files are tracked.