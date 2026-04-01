import re
from typing import List, Tuple

def calculate_relevance_score(text: str, title: str, primary_keyword: str, secondary_keywords: List[str]) -> Tuple[float, List[str]]:
    """
    score = (exact_matches * 3) + (partial_matches * 1) + (keyword_frequency * 0.5)
    """
    score = 0.0
    matched_keywords = []
    
    all_target_keywords = [primary_keyword] + secondary_keywords
    text_lower = text.lower()
    title_lower = title.lower()
    
    # Combined search space
    search_space = f"{title_lower} {text_lower}"
    
    for kw in all_target_keywords:
        kw_lower = kw.lower()
        if not kw_lower:
            continue
            
        # Exact word match (using regex boundaries)
        exact_matches = len(re.findall(rf'\b{re.escape(kw_lower)}\b', search_space))
        score += exact_matches * 3
        
        # Partial match (if no exact matches found but substring exists)
        if exact_matches == 0 and kw_lower in search_space:
            score += 1.0
            
        # Keyword frequency (all occurrences, including overlapping ones if any)
        # Using a simpler count for frequency as per the formula suggestion
        frequency = search_space.count(kw_lower)
        score += frequency * 0.5
        
        if kw_lower in search_space:
            matched_keywords.append(kw)
            
    return round(score, 2), matched_keywords
