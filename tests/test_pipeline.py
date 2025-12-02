# tests/test_pipeline.py
import os
from model_pipeline import prepare_data


def test_prepare_data():
    # Verifie que la fonction prepare_data ne plante pas
    data_path = "data/drug200.csv"
    assert os.path.exists(data_path), "Fichier drug200.csv manquant !"
    X_train, X_test, y_train, y_test, encoders = prepare_data(data_path)
    assert X_train.shape[0] > 0
    assert X_test.shape[0] > 0
    print("Test prepare_data passe avec succes !")
