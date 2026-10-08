
import mlflow
import mlflow.sklearn
import matplotlib.pyplot as plt

from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, ConfusionMatrixDisplay

# 1. Load dataset
iris = load_iris()
X = iris.data
y = iris.target

# 2. Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# 3. Set experiment name
mlflow.set_experiment("RandomForest-Experiment")

# 4. Start MLflow run
with mlflow.start_run(run_name="RandomForest-Run-3"):

    # Model parameters
    n_estimators = 200
    max_depth = 5

    # 5. Create and train model
    model = RandomForestClassifier(
        n_estimators=n_estimators,
        max_depth=max_depth,
        random_state=42
    )

    model.fit(X_train, y_train)

    # 6. Predict
    predictions = model.predict(X_test)

    # 7. Calculate accuracy
    accuracy = accuracy_score(y_test, predictions)

    # 8. Log parameters
    mlflow.log_param("n_estimators", n_estimators)
    mlflow.log_param("max_depth", max_depth)

    # 9. Log metrics
    mlflow.log_metric("accuracy", accuracy)

    # 10. Generate confusion matrix
    cm = confusion_matrix(y_test, predictions)
    display = ConfusionMatrixDisplay(
        confusion_matrix=cm,
        display_labels=iris.target_names
    )

    display.plot()
    plt.title("Random Forest Confusion Matrix")
    plt.tight_layout()
    plt.savefig("confusion_matrix.png")
    plt.close()

    # 11. Log artifact
    mlflow.log_artifact("confusion_matrix.png")

    # 12. Save trained model
    mlflow.sklearn.log_model(
    sk_model=model,
    name="random_forest_model",
    skops_trusted_types=["sklearn.tree._tree.Tree"]
)

    print("Experiment completed successfully!")
    print("Accuracy:", accuracy)
    print("Parameters:", n_estimators, max_depth)
