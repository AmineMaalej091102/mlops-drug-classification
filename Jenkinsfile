// Jenkinsfile (Declarative Pipeline)
pipeline {
    agent any

    environment {
        PROJECT_DIR = 'MohamedAmine-Maalej-4DS8-ml_project'
        DATA_PATH = "${PROJECT_DIR}/data/drug200.csv"
    }

    stages {
        // Étape 1 : Nettoyage + Récupération du code
        stage('Checkout & Clean') {
            steps {
                echo "Nettoyage de l’espace de travail..."
                cleanWs()
                checkout scm
                sh 'ls -la'
            }
        }

        // Étape 2 : Création d’un environnement virtuel + Installation
        stage('Setup Environment') {
            steps {
                dir(PROJECT_DIR) {
                    echo "Création de l’environnement virtuel..."
                    sh '''
                        python3 -m venv venv
                        . venv/bin/activate
                        pip install --upgrade pip
                        pip install -r requirements.txt
                        pip install black flake8 pytest
                    '''
                }
            }
        }

        // Étape 3 : Qualité du code (Linting & Formatting)
        stage('Code Quality') {
            steps {
                dir(PROJECT_DIR) {
                    sh '''
                        . venv/bin/activate
                        echo "Formatage automatique avec Black..."
                        black model_pipeline.py main.py tests/ --verbose
                        
                        echo "Vérification du style (Black check)..."
                        black --check model_pipeline.py main.py tests/
                        
                        echo "Analyse statique avec Flake8..."
                        flake8 model_pipeline.py main.py tests/ --max-line-length=88
                    '''
                }
            }
        }

        // Étape 4 : Tests unitaires
        stage('Tests') {
            steps {
                dir(PROJECT_DIR) {
                    sh '''
                        . venv/bin/activate
                        echo "Exécution des tests unitaires..."
                        pytest tests/ -v
                    '''
                }
            }
        }

        // Étape 5 : Entraînement du modèle
        stage('Train Model') {
            steps {
                dir(PROJECT_DIR) {
                    sh '''
                        . venv/bin/activate
                        echo "Entraînement du modèle Naive Bayes..."
                        python main.py data/drug200.csv --train --evaluate
                    '''
                }
            }
        }

        // Étape 6 : Archivage du modèle entraîné
        stage('Archive Model') {
            steps {
                dir(PROJECT_DIR) {
                    archiveArtifacts artifacts: 'models/*.joblib', fingerprint: true
                    echo "Modèle sauvegardé et archivé dans Jenkins !"
                }
            }
        }
    }

    post {
        always {
            echo "Pipeline terminé."
        }
        success {
            echo "TOUT EST VERT ! Modèle entraîné avec succès"
            // Optionnel : envoyer un mail, Slack, etc.
        }
        failure {
            echo "ÉCHEC du pipeline. Vérifie les logs !"
        }
        cleanup {
            cleanWs()  // Nettoie après chaque exécution
        }
    }
}
