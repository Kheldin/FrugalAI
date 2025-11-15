#!/usr/bin/env python
# coding: utf-8

# In[9]:


import joblib
import numpy as np

# Monter Drive

# ===== 1. CHARGER LE MODÈLE =====
print("📥 Chargement du modèle...")

SAVE_PATH = ""
model = joblib.load(SAVE_PATH + 'exercise_classifier_balanced.pkl')
vectorizer = joblib.load(SAVE_PATH + 'tfidf_vectorizer_balanced.pkl')

print(f"✅ Modèle chargé : {len(model.classes_)} classes")

# ===== 2. FONCTION DE PRÉDICTION =====
def predict_exercise(text, show_top_n=5):
    text_vec = vectorizer.transform([text])

    prediction = model.predict(text_vec)[0]
    probas = model.predict_proba(text_vec)[0]

    proba_dict = dict(zip(model.classes_, probas))

    sorted_probas = sorted(proba_dict.items(), key=lambda x: x[1], reverse=True)

    print("\n" + "="*70)
    print(f"📝 Texte : {text[:150]}{'...' if len(text) > 150 else ''}")
    print("="*70)
    print(f"\n🎯 PRÉDICTION : {prediction}")
    print(f"🔥 Confiance   : {proba_dict[prediction]:.1%}\n")

    print(f"📊 Top {show_top_n} prédictions :")
    for i, (exercise, prob) in enumerate(sorted_probas[:show_top_n], 1):
        bar_length = int(prob * 40)
        bar = "█" * bar_length + "░" * (40 - bar_length)
        marker = "👈" if exercise == prediction else "  "
        print(f"  {i}. {exercise:35s} │ {bar} │ {prob:6.2%} {marker}")

    print("="*70)

    return prediction, proba_dict


# ===== 3. FONCTION POUR TESTER PLUSIEURS PROMPTS =====
def test_multiple_prompts(prompts_list):
    print("\n" + "="*70)
    print(f"        TEST DE {len(prompts_list)} PROMPTS")
    print("="*70)

    results = []

    for i, prompt in enumerate(prompts_list, 1):
        print(f"\n{'─'*70}")
        print(f"PROMPT {i}/{len(prompts_list)}")
        print(f"{'─'*70}")

        prediction, probas = predict_exercise(prompt)
        results.append({
            'prompt': prompt[:100],
            'prediction': prediction,
            'confidence': probas[prediction]
        })

    print("\n" + "="*70)
    print("                    RÉSUMÉ DES PRÉDICTIONS")
    print("="*70)

    for i, result in enumerate(results, 1):
        print(f"\n{i}. {result['prompt']}...")
        print(f"   → {result['prediction']} ({result['confidence']:.1%})")

    return results

# ===== 5. MODE INTERACTIF =====
def interactive_mode():
    print("\n" + "="*70)
    print("            MODE INTERACTIF - TEST DE PROMPTS")
    print("="*70)
    print("\nEntrez vos prompts (tapez 'quit' ou 'exit' pour arrêter)")
    print("Tapez 'batch' pour entrer plusieurs prompts d'un coup\n")

    while True:
        user_input = input("\n💬 Votre prompt : ").strip()

        if user_input.lower() in ['quit', 'exit', 'q']:
            print("\n👋 Au revoir !")
            break

        if user_input.lower() == 'batch':
            print("\n📝 Mode batch : entrez vos prompts (ligne vide pour terminer)")
            batch_prompts = []
            while True:
                line = input(f"  Prompt {len(batch_prompts)+1} : ").strip()
                if not line:
                    break
                batch_prompts.append(line)

            if batch_prompts:
                test_multiple_prompts(batch_prompts)
            continue

        if not user_input:
            print("⚠️  Prompt vide, réessayez")
            continue

        predict_exercise(user_input)

# ===== 7. FONCTION POUR TESTER AVEC UN FICHIER =====
def test_from_file(file_path):
    print(f"\n📂 Lecture du fichier : {file_path}")

    with open(file_path, 'r', encoding='utf-8') as f:
        prompts = [line.strip() for line in f if line.strip()]

    print(f"✅ {len(prompts)} prompts trouvés\n")

    return test_multiple_prompts(prompts)

# ===== 8. FONCTION POUR COMPARER PLUSIEURS TEXTES =====
def compare_texts(text1, text2, text3=None):
    print("\n" + "="*70)
    print("              COMPARAISON DE TEXTES")
    print("="*70)

    texts = [text1, text2]
    if text3:
        texts.append(text3)

    predictions = []
    for i, text in enumerate(texts, 1):
        print(f"\n📝 TEXTE {i} :")
        pred, probas = predict_exercise(text, show_top_n=3)
        predictions.append((pred, probas[pred]))

    print("\n" + "="*70)
    print("                  RÉSUMÉ COMPARATIF")
    print("="*70)

    for i, (pred, conf) in enumerate(predictions, 1):
        print(f"\nTexte {i} : {pred} ({conf:.1%})")


# ===== 9. ANALYSE DE TEXTE DÉTAILLÉE =====
def detailed_analysis(text):
    text_vec = vectorizer.transform([text])
    prediction = model.predict(text_vec)[0]
    probas = model.predict_proba(text_vec)[0]

    proba_dict = dict(zip(model.classes_, probas))
    sorted_probas = sorted(proba_dict.items(), key=lambda x: x[1], reverse=True)

    print("\n" + "="*70)
    print("              ANALYSE DÉTAILLÉE")
    print("="*70)

    print(f"\n📝 Texte : {text}\n")
    print(f"🎯 Prédiction principale : {prediction} ({proba_dict[prediction]:.2%})\n")

    # Statistiques
    probas_array = np.array(probas)
    print(f"📊 Statistiques des probabilités :")
    print(f"   Moyenne    : {probas_array.mean():.4f}")
    print(f"   Médiane    : {np.median(probas_array):.4f}")
    print(f"   Max        : {probas_array.max():.4f}")
    print(f"   Écart-type : {probas_array.std():.4f}")

    # Entropie (mesure d'incertitude)
    entropy = -np.sum(probas_array * np.log(probas_array + 1e-10))
    print(f"   Entropie   : {entropy:.4f} (plus bas = plus certain)")

    print(f"\n📋 Toutes les probabilités (top 20) :")
    for i, (exercise, prob) in enumerate(sorted_probas[:20], 1):
        print(f"  {i:2d}. {exercise:40s} : {prob:6.2%}")

    print("="*70)

    return sorted_probas

predict_exercise("Imagine a creative story")

