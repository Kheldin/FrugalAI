"""
ULTIMATE TYPO DETECTION SYSTEM
================================
Combines multiple algorithms for the most reliable typo detection:
- Levenshtein distance (edit distance)
- Keyboard proximity (QWERTY + AZERTY)
- Phonetic similarity
- Common typo patterns
- Length-aware scoring
- Smart weighting system
"""

# ============================================================================
# KEYBOARD LAYOUT DEFINITIONS
# ============================================================================

# QWERTY keyboard neighbors (most common)
QWERTY_NEIGHBORS = {
    'a': 'qwszx', 'b': 'vghn', 'c': 'xdfv', 'd': 'erfcxs', 'e': 'wrdsf',
    'f': 'rtgvcd', 'g': 'tyhbvf', 'h': 'yujnbg', 'i': 'uojkl', 'j': 'uikmnh',
    'k': 'iolmj', 'l': 'opkm', 'm': 'njkl', 'n': 'bhjm', 'o': 'iplk',
    'p': 'ol', 'q': 'wa', 'r': 'etdf', 's': 'wedxza', 't': 'ryfg',
    'u': 'yihj', 'v': 'cfgb', 'w': 'qeas', 'x': 'zsdc', 'y': 'tugh',
    'z': 'asx'
}

# AZERTY keyboard neighbors (for French users)
AZERTY_NEIGHBORS = {
    'a': 'qzse', 'b': 'vghn', 'c': 'xdfv', 'd': 'erfcs', 'e': 'zsdr',
    'f': 'rtgvcd', 'g': 'tyhbvf', 'h': 'yujnbg', 'i': 'uojk', 'j': 'uikmnh',
    'k': 'iolmj', 'l': 'opm', 'm': 'njkl', 'n': 'bhjm', 'o': 'iplk',
    'p': 'ol', 'q': 'azw', 'r': 'etdf', 's': 'edxzqa', 't': 'ryfg',
    'u': 'yihj', 'v': 'cfgb', 'w': 'qxs', 'x': 'wsdc', 'y': 'tugh',
    'z': 'aeqs'
}

# ============================================================================
# PHONETIC SIMILARITY (sounds alike)
# ============================================================================

PHONETIC_GROUPS = [
    {'c', 'k', 's'},           # Similar sounds
    {'f', 'ph'},                # 'f' sound
    {'i', 'y'},                 # 'i' sound
    {'u', 'ou', 'w'},          # 'u' sound
    {'s', 'z'},                 # 's' sound
    {'g', 'j'},                 # soft 'g'
    {'c', 'q', 'k'},           # hard 'c'
]

# Common letter substitutions
COMMON_SUBSTITUTIONS = {
    'u': 'you',
    'r': 'are',
    '2': 'to',
    '4': 'for',
    'b': 'be',
    'c': 'see',
}

# ============================================================================
# CORE ALGORITHMS
# ============================================================================

def levenshtein_distance(s1, s2):
    """
    Calculate Levenshtein distance (minimum edit operations)
    """
    len1, len2 = len(s1), len(s2)
    
    # Create matrix
    matrix = [[0 for _ in range(len2 + 1)] for _ in range(len1 + 1)]
    
    # Initialize first column and row
    for i in range(len1 + 1):
        matrix[i][0] = i
    for j in range(len2 + 1):
        matrix[0][j] = j
    
    # Fill matrix
    for i in range(1, len1 + 1):
        for j in range(1, len2 + 1):
            cost = 0 if s1[i-1] == s2[j-1] else 1
            matrix[i][j] = min(
                matrix[i-1][j] + 1,      # Deletion
                matrix[i][j-1] + 1,      # Insertion
                matrix[i-1][j-1] + cost  # Substitution
            )
    
    return matrix[len1][len2]


def damerau_levenshtein_distance(s1, s2):
    """
    Enhanced distance that includes transpositions (swap adjacent chars)
    Example: "teh" -> "the" is distance 1 (not 2)
    """
    len1, len2 = len(s1), len(s2)
    max_dist = len1 + len2
    
    # Create matrix with extra row/column
    H = {}
    H[-1, -1] = max_dist
    
    for i in range(0, len1 + 1):
        H[i, -1] = max_dist
        H[i, 0] = i
    for j in range(0, len2 + 1):
        H[-1, j] = max_dist
        H[0, j] = j
    
    for i in range(1, len1 + 1):
        DB = 0
        for j in range(1, len2 + 1):
            k = DB
            l = 0 if s1[i-1] == s2[j-1] else 1
            if s1[i-1] == s2[j-1]:
                DB = j
            
            H[i, j] = min(
                H[i-1, j] + 1,           # Deletion
                H[i, j-1] + 1,           # Insertion
                H[i-1, j-1] + l,         # Substitution
                H[k-1, l-1] + (i-k-1) + 1 + (j-l-1)  # Transposition
            )
    
    return H[len1, len2]


def are_keys_adjacent(char1, char2, layout='qwerty'):
    """
    Check if two characters are adjacent on keyboard
    Supports both QWERTY and AZERTY layouts
    """
    if char1 == char2:
        return True
    
    neighbors = QWERTY_NEIGHBORS if layout == 'qwerty' else AZERTY_NEIGHBORS
    
    # Check both directions
    return (char2 in neighbors.get(char1, '') or 
            char1 in neighbors.get(char2, ''))


def are_phonetically_similar(char1, char2):
    """
    Check if characters sound similar
    """
    if char1 == char2:
        return True
    
    for group in PHONETIC_GROUPS:
        if char1 in group and char2 in group:
            return True
    
    return False


def has_repeated_letters(word):
    """
    Detect if word has repeated letters (common typo: "heyy", "thankss")
    """
    if len(word) < 2:
        return False
    
    for i in range(len(word) - 1):
        if word[i] == word[i + 1]:
            return True
    return False


def remove_repeated_letters(word):
    """
    Remove consecutive duplicate letters
    Example: "heyy" -> "hey", "thankss" -> "thanks"
    """
    if len(word) < 2:
        return word
    
    result = [word[0]]
    for i in range(1, len(word)):
        if word[i] != word[i-1]:
            result.append(word[i])
    
    return ''.join(result)


# ============================================================================
# SCORING SYSTEM
# ============================================================================

def calculate_typo_score(user_word, keyword):
    """
    Calculate comprehensive similarity score (0.0 to 1.0)
    Higher score = more similar
    
    Combines multiple factors:
    - Edit distance
    - Keyboard proximity
    - Phonetic similarity
    - Length ratio
    - First letter match
    - Common patterns
    """
    user_word = user_word.lower()
    keyword = keyword.lower()
    
    # Exact match
    if user_word == keyword:
        return 1.0
    
    # Empty words
    if not user_word or not keyword:
        return 0.0
    
    score = 0.0
    max_score = 0.0
    
    # ========================================
    # FACTOR 1: First letter match (15 points)
    # ========================================
    max_score += 15
    if user_word[0] == keyword[0]:
        score += 15
    elif are_keys_adjacent(user_word[0], keyword[0]):
        score += 7  # Partial credit for adjacent keys
    
    # ========================================
    # FACTOR 2: Length similarity (10 points)
    # ========================================
    max_score += 10
    len_diff = abs(len(user_word) - len(keyword))
    if len_diff == 0:
        score += 10
    elif len_diff == 1:
        score += 6
    elif len_diff == 2:
        score += 2
    
    # ========================================
    # FACTOR 3: Damerau-Levenshtein (30 points)
    # ========================================
    max_score += 30
    distance = damerau_levenshtein_distance(user_word, keyword)
    max_len = max(len(user_word), len(keyword))
    
    if max_len > 0:
        similarity_ratio = 1 - (distance / max_len)
        score += similarity_ratio * 30
    
    # ========================================
    # FACTOR 4: Keyboard proximity (20 points)
    # ========================================
    max_score += 20
    if len(user_word) == len(keyword):
        adjacent_count = 0
        for i in range(len(user_word)):
            if user_word[i] == keyword[i]:
                adjacent_count += 1
            elif are_keys_adjacent(user_word[i], keyword[i]):
                adjacent_count += 0.5
        
        proximity_ratio = adjacent_count / len(keyword)
        score += proximity_ratio * 20
    
    # ========================================
    # FACTOR 5: Phonetic similarity (15 points)
    # ========================================
    max_score += 15
    if len(user_word) == len(keyword):
        phonetic_matches = sum(1 for i in range(len(user_word)) 
                              if are_phonetically_similar(user_word[i], keyword[i]))
        phonetic_ratio = phonetic_matches / len(keyword)
        score += phonetic_ratio * 15
    
    # ========================================
    # FACTOR 6: Repeated letters pattern (10 points)
    # ========================================
    max_score += 10
    user_normalized = remove_repeated_letters(user_word)
    keyword_normalized = remove_repeated_letters(keyword)
    
    if user_normalized == keyword_normalized:
        score += 10  # It's just repeated letters!
    elif user_normalized == keyword or user_word == keyword_normalized:
        score += 8
    
    # ========================================
    # Final score normalization
    # ========================================
    final_score = score / max_score if max_score > 0 else 0.0
    
    return final_score


# ============================================================================
# MAIN TYPO DETECTION FUNCTION
# ============================================================================

def is_similar(user_word, keyword, threshold=0.80):
    """
    Version simplifiée et efficace
    """
    user_word = user_word.lower().strip()
    keyword = keyword.lower().strip()
    
    # Exact match
    if user_word == keyword:
        return True
    
    # Empty check
    if not user_word or not keyword:
        return False
    
    # Première lettre DOIT matcher
    if user_word[0] != keyword[0]:
        return False
    
    # Différence de longueur max 2
    len_diff = abs(len(user_word) - len(keyword))
    if len_diff > 2:
        return False
    
    # Distance Levenshtein simple
    distance = levenshtein_distance(user_word, keyword)
    max_len = max(len(user_word), len(keyword))
    
    # Score simple : 1 - (distance / longueur)
    score = 1 - (distance / max_len)
    
    return score >= threshold