# web_flask/app.py
from flask import Flask, render_template, request, flash, redirect, url_for
import requests
import secrets
import os

app = Flask(__name__)
app.secret_key = secrets.token_hex(24)

# URL de ton API FastAPI (doit être lancée en parallèle)
API_URL = "http://127.0.0.1:8000"

@app.route("/", methods=["GET", "POST"])
def index():
    prediction = None
    confidence = None

    if request.method == "POST":
        action = request.form.get("action")

        if action == "predict":
            try:
                data = {
                    "Age": int(request.form["age"]),
                    "Sex": request.form["sex"],
                    "BP": request.form["bp"],
                    "Cholesterol": request.form["cholesterol"],
                    "Na_to_K": float(request.form["na_to_k"])
                }

                response = requests.post(f"{API_URL}/predict", json=data)
                
                if response.status_code == 200:
                    result = response.json()
                    prediction = result["predicted_drug"]
                    confidence = result["confidence"]
                    flash(f"Médicament prédit : {prediction}", "success")
                    flash(f"Confiance : {confidence*100:.2f}%", "info")
                else:
                    flash(f"Erreur API : {response.json().get('detail', 'Inconnue')}", "error")

            except Exception as e:
                flash(f"Erreur de saisie : {str(e)}", "error")

        elif action == "retrain":
            try:
                response = requests.post(f"{API_URL}/retrain")
                if response.status_code == 200:
                    flash("Modèle réentraîné avec succès !", "success")
                else:
                    flash("Échec du réentraînement", "error")
            except:
                flash("Impossible de contacter l'API pour le réentraînement", "error")

    return render_template("predict.html", prediction=prediction, confidence=confidence)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
