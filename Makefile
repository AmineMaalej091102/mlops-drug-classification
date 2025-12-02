# Makefile - Projet Classification de Medicaments

#  Variables
DATA_PATH = data/drug200.csv
PYTHON = python
PIP = pip

# ---------------------------------
# 1. Installation des dependances
# ---------------------------------
.PHONY: install
install:
	@echo "Installation des dependances..."
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

# ---------------------------------
# 2. Qualite du code (CI)
# ---------------------------------
.PHONY: lint
lint:
	@echo "Verification du formatage (black)..."
	black --check .
	@echo "Verification de la qualite du code (flake8)..."
	flake8 model_pipeline.py main.py tests/

.PHONY: format
format:
	@echo "Formatage automatique du code (black)..."
	black model_pipeline.py main.py tests/

# ---------------------------------
# 3. Tests unitaires
# ---------------------------------
.PHONY: test
test:
	@echo "Execution des tests..."
	$(PYTHON) -m pytest tests/ -v

# ---------------------------------
# 4. Pipeline ML complet
# ---------------------------------
.PHONY: train
train: install
	@echo "Entrainement du modele..."
	$(PYTHON) main.py $(DATA_PATH) --train --evaluate

.PHONY: evaluate
evaluate: install
	@echo "Evaluation avec modele sauvegarde..."
	$(PYTHON) main.py $(DATA_PATH) --load models/nb_drug_model.joblib

# ---------------------------------
# 5. Pipeline complet (tout en une commande)
# ---------------------------------
.PHONY: all
all: install format test train
	@echo "Pipeline complet execute avec succes !"

# ---------------------------------
# 6. Nettoyage
# ---------------------------------
.PHONY: clean
clean:
	@echo "Nettoyage des fichiers temporaires..."
	rm -rf __pycache__
	rm -rf tests/__pycache__
	rm -rf models/*.joblib

# ---------------------------------
# 7. Aide
# ---------------------------------
.PHONY: help
help:
	@echo "Commandes disponibles :"
	@echo "    make install    -> Installer les dependances"
	@echo "    make format     -> Formater le code (black)"
	@echo "    make lint       -> Verifier la qualite du code"
	@echo "    make test       -> Lancer les tests"
	@echo "    make train      -> Entrainer + evaluer + sauvegarder"
	@echo "    make evaluate   -> Evaluer avec modele existant"
	@echo "    make all        -> Tout faire (install + format + test + train)"
	@echo "    make clean      -> Nettoyer les fichiers temporaires"

# ---------------------------------
# 8. Lancer l'API FastAPI
# ---------------------------------
.PHONY: api
api: install
	@echo "Demarrage de l'API FastAPI..."
	uvicorn app:app --reload --host 0.0.0.0 --port 8000

.PHONY: docs
docs:
	@echo "Ouverture de la documentation Swagger..."
	python -c "import webbrowser; webbrowser.open('http://127.0.0.1:8000/docs')"

# -----------------------------
#          MLflow
# -----------------------------
.PHONY: mlflow-ui
mlflow-ui:
	@echo "Lancement de l'interface MLflow (SQLite backend)"
	mlflow ui --backend-store-uri sqlite:///mlflow.db --host 0.0.0.0 --port 5000

.PHONY: mlflow-train
mlflow-train: install
	@echo "Entrainement avec tracking MLflow..."
	python mlflow_tracking.py

.PHONY: mlflow-all
mlflow-all: mlflow-ui
	@sleep 3
	@make mlflow-train
