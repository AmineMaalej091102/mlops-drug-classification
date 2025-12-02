# prediction_app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('predict/', views.predict_drug, name='predict'),
    path('retrain/', views.retrain_model, name='retrain'),
]
