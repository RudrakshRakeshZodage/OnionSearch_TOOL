import re
from typing import List, Tuple

def calculate_relevance_score(text: str, title: str, primary_keyword: str, secondary_keywords: List[str]) -> Tuple[float, List[str]]:
    """
    Calculates a ranking score based on user-provided weights:
    score = (exact_matches * 3) + (partial_matches * 1) + (keyword_frequency * 0.5)
    
    - Exact Match: Whole word matches (e.g. 'paypal' in 'paypal site')
    - Partial Match: Substring matches (e.g. 'pay' in 'paypal')
    - Frequency: Total occurrences of the keyword in the document.
    """
    score = 0.0
    matched_keywords = []
    
    all_target_keywords = [primary_keyword] + [s for s in secondary_keywords if s]
    # Clean text to avoid regex issues
    text_clean = text.lower()
    title_clean = title.lower()
    search_space = f"{title_clean} {text_clean}"
    
    for kw in all_target_keywords:
        kw_lower = kw.lower()
        if not kw_lower:
            continue
            
        found_in_doc = False
        
        # 1. Exact matches (Whole Word) -> Weight: 3
        # We use \b boundary to ensure it's an exact word match
        exact_count = len(re.findall(rf'\b{re.escape(kw_lower)}\b', search_space))
        score += exact_count * 3.0
        if exact_count > 0:
            found_in_doc = True
            
        # 2. Partial matches (Substring) -> Weight: 1
        # Only counted if it's NOT an exact match but exists as part of another word
        if exact_count == 0 and kw_lower in search_space:
            score += 1.0
            found_in_doc = True
            
        # 3. Keyword Frequency -> Weight: 0.5
        # Total count of the string appearing in the text
        freq_count = search_space.count(kw_lower)
        score += freq_count * 0.5
        
        if found_in_doc:
            matched_keywords.append(kw)
            
    return round(score, 2), matched_keywords
