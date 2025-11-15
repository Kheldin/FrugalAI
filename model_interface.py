import joblib
import numpy as np

# Charger le modèle au démarrage
print("📥 Chargement du modèle IA...")
model = joblib.load('exercise_classifier_balanced.pkl')
vectorizer = joblib.load('tfidf_vectorizer_balanced.pkl')
print(f"✅ Modèle IA chargé : {len(model.classes_)} classes")

def call_ai_model(message):
    """
    Utilise le modèle IA pour traiter les messages complexes
    Retourne une réponse intelligente basée sur la prédiction
    """
    # Vectoriser le message
    text_vec = vectorizer.transform([message])
    
    # Prédire la catégorie
    prediction = model.predict(text_vec)[0]
    probas = model.predict_proba(text_vec)[0]
    
    # Trouver la confiance
    proba_dict = dict(zip(model.classes_, probas))
    confidence = proba_dict[prediction]
    
    # Générer une réponse basée sur la prédiction
    if confidence > 0.7:  # Haute confiance
        response = f"I understand you're interested in {prediction}. How can I help you with that?"
    elif confidence > 0.4:  # Confiance moyenne
        response = f"It seems like you're asking about {prediction}. Could you provide more details?"
    else:  # Basse confiance
        response = "I'm not quite sure what you're asking. Could you rephrase your question?"
    
    return response