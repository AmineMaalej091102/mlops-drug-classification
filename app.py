# app.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd
import os
from model_pipeline import prepare_data, train_model, save_model

# Chargement du modele au demarrage
MODEL_PATH = "models/nb_drug_model.joblib"

if not os.path.exists(MODEL_PATH):
	raise FileNotFoundError(f"Modele non trouve ! Execute d'abord : make train")

loaded = joblib.load(MODEL_PATH)
model = loaded["model"]
encoders = loaded["encoders"]

app = FastAPI(
	title="Drug Classification API",
	description="Prediction du type de medicament avec Naive Bayes",
	version="1.0"
)

# Modele d'entree pour la prediction
class PatientFeatures(BaseModel):
	Age: int
	Sex: str		# "M" ou "F"
	BP: str 		# "HIGH", "NORMAL", "LOW"
	Cholesterol: str	# "HIGH", "NORMAL"
	Na_to_K: float

@app.get("/")
def root():
	return {"message": "API Drug Classification - Naive Bayes", "docs": "/docs"}

@app.post("/predict")
def predict(patient: PatientFeatures):
	try:
		# Creer un DataFrame avec les donnees du patient
		data = {
			"Age": [patient.Age],
			"Sex": [patient.Sex],
			"BP": [patient.BP],
			"Cholesterol": [patient.Cholesterol],
			"Na_to_K": [patient.Na_to_K]
		}
		df = pd.DataFrame(data)

		# Appliquer les memes encodeurs que pendant l'entrainement
		for col, encoder in encoders.items():
			if col in df.columns:
				df[col] = encoder.transform(df[col])

		# Prediction
		prediction = model.predict(df)[0]
		probability = float(model.predict_proba(df).max())

		return {
			"predicted_drug": prediction,
			"confidence": round(probability, 4),
			"patient_data": patient.dict()
		}
	except Exception as e:
		raise HTTPException(status_code=400, detail=str(e))

# Excellence : endpoint pour reentrainer le modele
@app.post("/retrain")
def retrain(data_path: str = "data/drug200.csv"):
	if not os.path.exists(data_path):
		raise HTTPException(status_code=404, detail="Fichier de donnees introuvable")

	try:
		X_train, X_test, y_train, y_test, new_encoders = prepare_data(data_path)
		new_model = train_model(X_train, y_train)
		save_model(new_model, new_encoders, filename="nb_drug_model.joblib")

		# Recharger le nouveau modele
		global model, encoders
		loaded = joblib.load(MODEL_PATH)
		model = loaded["model"]
		encoders = loaded["encoders"]

		return {
			"status": "success",
			"message": "Modele reentraine et recharge avec succes !",
			"data_used": data_path
		}
	except Exception as e:
		raise HTTPException(status_code=500, detail=f"Erreur lors du reentrainement : {str(e)}")

