"""
Rugby Atlas - Text Normalization Utilities
Handles text normalization for team names, fuzzy matching, etc.
"""
import re
from typing import List, Optional, Tuple
from difflib import SequenceMatcher

from ..core.logging import get_logger

logger = get_logger(__name__)


class TextNormalizer:
    """
    Utility class for text normalization and fuzzy matching.
    Useful for matching team names from different sources.
    """
    
    # Common abbreviations and their expansions
    TEAM_ALIASES = {
        "all blacks": "new zealand",
        "springboks": "south africa",
        "wallabies": "australia",
        "england": "england",
        "wales": "wales",
        "scotland": "scotland",
        "ireland": "ireland",
        "france": "france",
        "italy": "italy",
    }
    
    @staticmethod
    def normalize_text(text: str) -> str:
        """
        Normalize text by converting to lowercase, removing extra spaces, etc.
        
        Args:
            text: Input text
        
        Returns:
            Normalized text
        """
        if not text:
            return ""
        
        # Convert to lowercase
        normalized = text.lower()
        
        # Remove special characters except spaces and hyphens
        normalized = re.sub(r'[^a-z0-9\s\-]', '', normalized)
        
        # Replace multiple spaces with single space
        normalized = re.sub(r'\s+', ' ', normalized)
        
        # Strip leading/trailing spaces
        normalized = normalized.strip()
        
        return normalized
    
    @staticmethod
    def remove_common_words(text: str) -> str:
        """
        Remove common words that don't add meaning for matching.
        
        Args:
            text: Input text
        
        Returns:
            Text with common words removed
        """
        common_words = {'the', 'a', 'an', 'rugby', 'fc', 'rfc', 'club', 'team'}
        words = text.split()
        filtered = [w for w in words if w not in common_words]
        return ' '.join(filtered)
    
    @classmethod
    def normalize_team_name(cls, name: str) -> str:
        """
        Normalize a team name for matching purposes.
        
        Args:
            name: Team name
        
        Returns:
            Normalized team name
        """
        normalized = cls.normalize_text(name)
        normalized = cls.remove_common_words(normalized)
        
        # Check for known aliases
        for alias, official in cls.TEAM_ALIASES.items():
            if alias in normalized:
                normalized = normalized.replace(alias, official)
        
        return normalized
    
    @staticmethod
    def calculate_similarity(text1: str, text2: str) -> float:
        """
        Calculate similarity between two strings.
        
        Args:
            text1: First string
            text2: Second string
        
        Returns:
            Similarity score between 0 and 1
        """
        return SequenceMatcher(None, text1, text2).ratio()
    
    @classmethod
    def fuzzy_match_team(
        cls,
        query: str,
        candidates: List[str],
        threshold: float = 0.7
    ) -> List[Tuple[str, float]]:
        """
        Fuzzy match a team name against a list of candidates.
        
        Args:
            query: Team name to search for
            candidates: List of candidate team names
            threshold: Minimum similarity threshold (0-1)
        
        Returns:
            List of (candidate, score) tuples sorted by score
        """
        normalized_query = cls.normalize_team_name(query)
        
        matches = []
        for candidate in candidates:
            normalized_candidate = cls.normalize_team_name(candidate)
            score = cls.calculate_similarity(normalized_query, normalized_candidate)
            
            if score >= threshold:
                matches.append((candidate, score))
        
        # Sort by score descending
        matches.sort(key=lambda x: x[1], reverse=True)
        
        return matches
    
    @staticmethod
    def extract_year(text: str) -> Optional[int]:
        """
        Extract a year from text (useful for season parsing).
        
        Args:
            text: Input text
        
        Returns:
            Extracted year or None
        """
        match = re.search(r'\b(19|20)\d{2}\b', text)
        if match:
            return int(match.group())
        return None


def normalize_team_name(name: str) -> str:
    """
    Convenience function for normalizing team names.
    
    Args:
        name: Team name
    
    Returns:
        Normalized team name
    """
    return TextNormalizer.normalize_team_name(name)
