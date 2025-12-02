# mlflow_tracking.py
import mlflow
import mlflow.sklearn
from sklearn.metrics import accuracy_score, classification_report
from model_pipeline import prepare_data, GaussianNB
import joblib
import os

def train_with_mlflow(data_path="data/drug200.csv", experiment_name="Drug_Classification_NB"):
    # Configuration MLflow
    mlflow.set_tracking_uri("http://127.0.0.1:5000")  # si MLflow UI est lancé
    mlflow.set_experiment(experiment_name)

    with mlflow.start_run(run_name="NaiveBayes_v1"):
        # 1. Préparation des données
        X_train, X_test, y_train, y_test, encoders = prepare_data(data_path)

        # 2. Log des paramètres
        mlflow.log_param("model_type", "GaussianNB")
        mlflow.log_param("test_size", 0.2)
        mlflow.log_param("random_state", 26)
        mlflow.log_param("dataset_rows", len(X_train) + len(X_test))

        # 3. Entraînement
        model = GaussianNB()
        model.fit(X_train, y_train)

        # 4. Prédictions & métriques
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)

        # 5. Log des métriques
        mlflow.log_metric("accuracy", accuracy)
        mlflow.log_metric("test_samples", len(X_test))

        # 6. Log du rapport de classification (comme artefact texte)
        report = classification_report(y_test, y_pred, output_dict=True)
        for label, metrics in report.items():
            if isinstance(metrics, dict):
                for metric_name, value in metrics.items():
                    mlflow.log_metric(f"{label}_{metric_name}", value)

        # 7. Sauvegarde locale + log du modèle dans MLflow
        model_info = {"model": model, "encoders": encoders}
        model_path = "models/nb_drug_model.joblib"
        os.makedirs("models", exist_ok=True)
        joblib.dump(model_info, model_path)

        # 8. Enregistrement du modèle dans MLflow
        mlflow.sklearn.log_model(
            sk_model=model,
            artifact_path="naive_bayes_model",
            registered_model_name="DrugClassifier_NB"
        )

        # 9. Log du modèle complet avec encodeurs (artefact personnalisé)
        mlflow.log_artifact(model_path, artifact_path="full_model")

        # 10. Tags pour la traçabilité
        mlflow.set_tag("project", "MLOps_ESPRIT_2025")
        mlflow.set_tag("author", "Mohamed_Amine_Maalej")
        mlflow.set_tag("status", "production_ready")

        print(f"\nRun terminé ! Accuracy: {accuracy:.4f}")
        print(f"Voir les résultats → http://127.0.0.1:5000")
        print(f"Modèle enregistré dans MLflow sous 'DrugClassifier_NB'")

        return model, accuracy
