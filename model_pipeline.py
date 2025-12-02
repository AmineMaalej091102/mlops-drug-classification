# model_pipeline.py
import os
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score, classification_report
from sklearn.metrics import confusion_matrix


def prepare_data(data_path: str, test_size: float = 0.2, random_state: int = 26):
    """
    Charge et pretraite les donnees :
    - LabelEncoder sur Sex, BP, Cholesterol
    - Age et Na_to_K restent numeriques
    Parameters
    ----------
    data_path : str
            Chemin vers drug200.csv
    test_size : float
            Proportion du test set
    random_state : int
            Pour la reproducibilite
    Returns
    -------
    X_train, X_test, y_train, y_test, encoders (dict)
    """
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Fichier introuvable : {data_path}")

    df = pd.read_csv(data_path)

    # Encodage des variables categorielles
    encoders = {}
    for col in ["Sex", "BP", "Cholesterol"]:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])
        encoders[col] = le
    X = df.drop("Drug", axis=1)
    y = df["Drug"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )

    return X_train, X_test, y_train, y_test, encoders


def train_model(X_train, y_train):
    """
    Entraine un modele Gaussian Naive Bayes
    """
    model = GaussianNB()
    model.fit(X_train, y_train)
    print("Modele Gaussian Naive Bayes entraine avec succes!")
    return model


def evaluate_model(model, X_test, y_test):
    """
    Evalue le modele et affiche les metriques detaillees
    """
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    print("\n" + "=" * 55)
    print("           RESULTATS - Gaussian Naive Bayes")
    print("=" * 55)
    print(f"Accuracy : {accuracy:.4f}")
    print("\nClassification Report :\n")
    print(classification_report(y_test, y_pred))
    print("Matrice de confusion :\n")
    print(confusion_matrix(y_test, y_pred))

    return {"accuracy": accuracy}


def save_model(model, encoders, model_dir="models", filename="nb_drug_model.joblib"):
    """
    Sauvegarde le modele + les encodeurs avec joblib
    """
    os.makedirs(model_dir, exist_ok=True)
    path = os.path.join(model_dir, filename)
    joblib.dump({"model": model, "encoders": encoders}, path)
    print(f"Modele + encodeurs sauvegardes -> {path}")


def load_model(filepath: str):
    """
    Charge un modele et les encodeurs sauvegardes
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Modele non trouve : {filepath}")

    data = joblib.load(filepath)
    print(f"Modele Naive Bayes charge depuis {filepath}")
    return data["model"], data["encoders"]
