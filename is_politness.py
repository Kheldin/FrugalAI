POLITESSE = [
    "merci",
    "merci beaucoup",
    "thx",
    "thanks",
    "ok merci",
    "bonne journée",
    "bonne soirée",
    "salut",
    "hello",
    "yo",
    "cc",
    "coucou",
    "ok",
    "daccord",
    "d'accord",
]


def is_politeness(message: str) -> bool:
    msg = message.lower().strip()
    if len(msg) < 20 and any(p in msg for p in POLITESSE):
        return True
    return False
