# prediction_app/views.py
from django.shortcuts import render
import requests
from django.contrib import messages

API_URL = "http://127.0.0.1:8000"  # Laisse comme ça si FastAPI tourne en local

def home(request):
    return render(request, 'predict.html')

def predict_drug(request):
    if request.method == "POST":
        try:
            data = {
                "Age": int(request.POST['age']),
                "Sex": request.POST['sex'],
                "BP": request.POST['bp'],
                "Cholesterol": request.POST['cholesterol'],
                "Na_to_K": float(request.POST['na_to_k'])
            }
            response = requests.post(f"{API_URL}/predict", json=data)
            result = response.json()

            if response.status_code == 200:
                messages.success(request, f"Médicament recommandé : {result['predicted_drug']}")
                messages.info(request, f"Confiance : {result['confidence']*100:.2f}%")
            else:
                messages.error(request, f"Erreur API : {result.get('detail', 'Inconnue')}")
        except Exception as e:
            messages.error(request, f"Erreur : {str(e)}")

    return render(request, 'predict.html')

def retrain_model(request):
    if request.method == "POST":
        response = requests.post(f"{API_URL}/retrain")
        if response.status_code == 200:
            messages.success(request, "Modèle réentraîné avec succès !")
        else:
            messages.error(request, "Échec du réentraînement")
    return render(request, 'predict.html')
