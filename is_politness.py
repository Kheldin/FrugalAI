POLITESSE = [
    "merci",
    "mrc",
    "merci beaucoup",
    "thx",
    "thanks",
    "ok merci",
    "bonne journée",
    "bonne soirée",
    "salut",
    "bonjour",
    "bjr",
    "hello",
    "hi",
    "yo",
    "cc",
    "coucou",
    "ok",
    "mdr",
    "lol",
    "daccord",
    "d'accord",
    "oui",
    "non",
    "nn",
    "yes",
    "no",
    "au revoir",
    "bye",
    "ciao",
    "à plus tard",
    "à demain",
    "à+",
    "a plus",
    "à toute",
]

def is_politeness(message: str) -> bool:
    msg = message.lower().strip()
    if len(msg) < 20 and any(p in msg for p in POLITESSE):
        return True
    return False
