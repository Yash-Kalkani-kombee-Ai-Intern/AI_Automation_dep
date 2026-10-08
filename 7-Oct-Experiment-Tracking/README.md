 # MLflow Experiment Tracking — Random Forest Classification

## 1. Project Overview

This project demonstrates how to use **MLflow** for machine learning experiment tracking, model comparison, artifact logging, and model version management.

A Random Forest Classifier is trained on the Iris dataset using different hyperparameters. MLflow records the experiment results, making it easier to compare model performance and identify the best configuration.

## 2. Objectives

- Understand the importance of experiment tracking in MLOps.
- Track machine learning hyperparameters and evaluation metrics.
- Log trained models and evaluation artifacts.
- Compare multiple experiments using the MLflow dashboard.
- Register the best-performing model using MLflow Model Registry.

## 3. Technologies Used

| Technology | Purpose |
|---|---|
| Python | Machine learning development |
| MLflow | Experiment tracking and model registry |
| Scikit-learn | Random Forest model training |
| Matplotlib | Confusion matrix visualization |
| Pandas | Data analysis |
| SQLite | Local MLflow tracking database |

## 4. Project Structure

```text
7-Oct-Experiment-Tracking/
│
├── train.py
├── requirements.txt
├── README.md
├── .gitignore
├── confusion_matrix.png
├── mlflow.db
├── mlruns/
└── venv/
```

**Note:** The virtual environment, local MLflow database, and tracking artifacts can be excluded from Git. Keep them locally or export experiment evidence separately.

## 5. Installation

### Step 1: Create Virtual Environment

```powershell
python -m venv venv
```

### Step 2: Activate Environment

```powershell
.\venv\Scripts\Activate.ps1
```

### Step 3: Install Dependencies

```powershell
pip install -r requirements.txt
```

## 6. Run Model Training

Execute the training script:

```powershell
python train.py
```

The script performs the following operations:

1. Loads the Iris dataset.
2. Splits data into training and testing sets.
3. Trains a Random Forest Classifier.
4. Calculates model accuracy.
5. Logs hyperparameters and metrics using MLflow.
6. Generates and logs a confusion matrix.
7. Saves the trained model as an MLflow artifact.

## 7. MLflow Experiment Tracking

Experiment Name:

```text
RandomForest-Experiment
```

Parameters tracked:

- `n_estimators`
- `max_depth`

Metrics tracked:

- `accuracy`

Artifacts tracked:

- `confusion_matrix.png`
- Trained Random Forest model

### Experiment Results

| Run | n_estimators | max_depth | Accuracy |
|---|---:|---:|---:|
| RandomForest-Run-1 | 100 | 5 | 93.33% |
| RandomForest-Run-2 | 50 | 5 | 90.00% |
| RandomForest-Run-3 | 200 | 5 | 90.00% |

The experiment history also contains duplicate runs and an earlier failed run during model serialization.

**Best-performing run:** RandomForest-Run-1

**Accuracy:** 93.33%

These results are based on the project's Iris test split.

## 8. Launch MLflow Dashboard

Start the MLflow tracking dashboard:

```powershell
python -m mlflow ui --backend-store-uri "sqlite:///mlflow.db" --host 127.0.0.1 --port 5000 --workers 1
```

Open the dashboard:

http://127.0.0.1:5000

Navigate to:

**Experiments → RandomForest-Experiment → Training runs**

The dashboard allows users to:

- View experiment history.
- Compare parameters and metrics.
- Inspect confusion matrix artifacts.
- Review trained models.
- Identify the best-performing experiment.

## 9. Model Registration

The best-performing model was successfully registered using MLflow Model Registry.

| Property | Value |
|---|---|
| Registered Model | RandomForest-Production |
| Version | 1 |
| Source Run | RandomForest-Run-1 |
| Model Status | Ready |
| Accuracy | 93.33% |

Model registration enables version management and supports future deployment workflows.

**Note:** The model has been registered, but it has not been deployed to a production server.

## 10. Key MLflow Functions

| Function | Description |
|---|---|
| `mlflow.set_experiment()` | Creates or selects an experiment |
| `mlflow.start_run()` | Starts a tracking run |
| `mlflow.log_param()` | Logs model parameters |
| `mlflow.log_metric()` | Logs evaluation metrics |
| `mlflow.log_artifact()` | Logs output files |
| `mlflow.sklearn.log_model()` | Saves a trained scikit-learn model |
| `mlflow.search_runs()` | Retrieves recorded experiment runs |

## 11. Acceptance Criteria

- [x] Understand experiment tracking and reproducibility.
- [x] Integrate MLflow into a Python training pipeline.
- [x] Log model parameters and evaluation metrics.
- [x] Save trained models and evaluation artifacts.
- [x] Execute multiple experiment runs.
- [x] Compare experiments using the MLflow dashboard.
- [x] Identify the best-performing model.
- [x] Register the selected model as Version 1.

## 12. Conclusion

Successfully implemented an MLflow-based experiment tracking workflow using a Random Forest Classifier.

The project demonstrates hyperparameter logging, accuracy tracking, artifact storage, model comparison, and model registration.

The best-performing experiment achieved **93.33% test accuracy**, and its trained model was registered as **RandomForest-Production Version 1**.

This project provides a practical introduction to experiment tracking and model lifecycle management in MLOps.
