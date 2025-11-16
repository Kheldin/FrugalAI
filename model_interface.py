import joblib
import numpy as np
from rich.console import Console
from rich.panel import Panel

console = Console()

# Charger le modèle au démarrage
print("📥 Chargement du modèle IA...")
model = joblib.load('exercise_classifier_balanced.pkl')
vectorizer = joblib.load('tfidf_vectorizer_balanced.pkl')
print(f"✅ Modèle IA chargé : {len(model.classes_)} classes")

def get_difficulty_info(prediction):
    """
    Détermine la difficulté du prompt basée sur la catégorie prédite
    Retourne: (niveau, couleur, emoji)
    """
    # Dictionnaire des difficultés par catégorie
    difficulty_map = {
        # FACILE 🟢
        "memorization": ("FACILE", "green", "🟢"),
        "mcq": ("FACILE", "green", "🟢"),
        "cooking": ("FACILE", "green", "🟢"),
        
        # MOYEN 🟡
        "editing": ("MOYEN", "yellow", "🟡"),
        "math mcq": ("MOYEN", "yellow", "🟡"),
        
        # DIFFICILE 🟠
        "creative writing": ("DIFFICILE", "orange1", "🟠"),
        "constrained writing": ("DIFFICILE", "orange1", "🟠"),
        
        # TRÈS DIFFICILE 🔴
        "rag": ("TRÈS DIFFICILE", "red", "🔴"),
        "math exercise": ("TRÈS DIFFICILE", "red", "🔴"),

    }
    
    # Normaliser le nom de la catégorie (enlever espaces, mettre en minuscule)
    normalized = prediction.lower().strip()
    
    # Chercher la difficulté correspondante
    if normalized in difficulty_map:
        return difficulty_map[normalized]
    
    # Par défaut, considérer comme MOYEN si catégorie inconnue
    return "MOYEN", "yellow", "🟡"

def call_ai_model(message):
    """
    Utilise le modèle IA pour traiter les messages complexes
    Affiche la difficulté du prompt avec une couleur
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
    
    # Calculer l'entropie (mesure d'incertitude)
    probas_array = np.array(probas)
    entropy = -np.sum(probas_array * np.log(probas_array + 1e-10))
    
    # Obtenir les informations de difficulté (basé sur la catégorie)
    difficulty, color, emoji = get_difficulty_info(prediction)
    
    # Afficher la difficulté avec style
    console.print(Panel(
        f"[bold]{emoji} Difficulté: [{color}]{difficulty}[/{color}][/bold]\n"
        f"Confiance: [bold]{confidence:.1%}[/bold] | "
        f"Entropie: [bold]{entropy:.2f}[/bold]",
        title="📊 Analyse du Prompt",
        border_style=color,
        padding=(0, 1)
    ))
    
    # Afficher les top 3 prédictions
    sorted_probas = sorted(proba_dict.items(), key=lambda x: x[1], reverse=True)[:3]
    console.print("\n[bold cyan]Top 3 prédictions:[/bold cyan]")
    for i, (category, prob) in enumerate(sorted_probas, 1):
        bar_length = int(prob * 20)
        bar = "█" * bar_length + "░" * (20 - bar_length)
        marker = "👈" if category == prediction else ""
        console.print(f"  {i}. {category:30s} [{color}]{bar}[/{color}] {prob:5.1%} {marker}")
    
    console.print()  # Ligne vide pour l'espacement
    
    # Ne retourne rien (pas de "Bot: None")
    return None