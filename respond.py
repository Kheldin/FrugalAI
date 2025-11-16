import random
import readline
from is_similar import is_similar


def load_replies_from_file(filename): 
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            replies = [line.strip() for line in f.readlines() if line.strip()]
            return replies if replies else ["You're welcome!"] 
    except FileNotFoundError:
        print(f"Warning: {filename} not found. Using default replies.")
        return ["You're welcome!", "No problem!", "My pleasure!"]

replies_thanks = load_replies_from_file('answer_txt/replies_thanks.txt')
replies_greeting = load_replies_from_file('answer_txt/replies_greeting.txt')
replies_goodbye = load_replies_from_file('answer_txt/replies_goodbye.txt')
replies_how_are_you = load_replies_from_file('answer_txt/replies_how_are_you.txt')

responses = {
    "reply_thanks": replies_thanks,            
    "reply_greeting": replies_greeting,      
    "reply_goodbye": replies_goodbye,        
    "reply_how_are_you": replies_how_are_you,
}

keywords = {
    "reply_thanks": [
        "thanks",
        "thank",
        "ty",
        "thx",
        "cheers",
    ],
    "reply_greeting": [
        "hi",
        "hey", 
        "hello",
        "yo",
    ],
    "reply_goodbye": [
        "goodbye",
        "see you",
        "see u",
        "bye",
        "quit",
        "exit",
        "close",
        "later",
        "farewell",
    ],
    "reply_how_are_you": [
        "how are you",
        "what's up",
        "how r u",
        "how are u",
    ]
}

def normalize_message(message):
    """
    Remplace les abréviations courantes
    """
    message = message.lower()
    # Remplacer les abréviations
    message = message.replace(" u ", " you ")
    message = message.replace(" r ", " are ")
    message = message.replace("u ", "you ")
    message = message.replace(" u?", " you?")
    return message

def is_valid_message(message):
    
    message = message.strip()
    
    if len(message) == 0:
        return False
    
    # DÉPLACÉ APRÈS detect_category - ne plus vérifier ici
    if len(message) <= 2 and message not in ["?", "!!"]:
        return False
    
    if not any(c.isalnum() for c in message):
        return False
    
    if len(set(message.replace(" ", ""))) <= 2 and len(message) > 5:
        return False
    
    return True

def detect_category(message):
    """
    Détecte la catégorie du message
    Utilise le système de détection de typos avancé
    """
    message = normalize_message(message)
    message = message.strip()
    message_words = message.split()
    
    # VÉRIFICATION LONGUEUR DÉPLACÉE ICI (après normalisation)
    # Si le message est trop court (≤ 2 caractères) et n'est pas dans les exceptions
    if len(message) <= 2 and message not in ["?", "!!", "hi", "yo", "ok", "ty"]:
        return None
    
    # Si le message est trop long (> 5 mots), rediriger vers l'IA
    if len(message_words) > 5:
        return None
    
    # ÉTAPE 1 : Chercher des PHRASES complètes (pour "how are you", etc.)
    for category, keyword_list in keywords.items():
        for keyword in keyword_list:
            # Si le keyword contient un espace, c'est une phrase
            if " " in keyword:
                if keyword in message:
                    return category
    
    # ÉTAPE 2 : Correspondance exacte MOT PAR MOT
    for category, keyword_list in keywords.items():
        for keyword in keyword_list:
            # Seulement les keywords d'un seul mot
            if " " not in keyword:
                for word in message_words:
                    if word == keyword:
                        if len(message_words) <= 2:
                            return category
    
    # ÉTAPE 3 : Détection de TYPOS avec le super algorithme
    # Seulement pour messages courts (2 mots max)
    if len(message_words) <= 2:
        for category, keyword_list in keywords.items():
            for keyword in keyword_list:
                # Seulement keywords simples (pas de phrases)
                if " " not in keyword:
                    for word in message_words:
                        # UTILISE LE SUPER ALGORITHME ICI
                        if is_similar(word, keyword):
                            return category
    
    return None

def respond(message):
    category = detect_category(message)
    if category:
        return random.choice(responses[category])
    return "You will be redirected shortly..."