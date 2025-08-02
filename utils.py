#!/usr/bin/env python3
"""
Utility functions for the ReputeBot.
"""

import datetime
import re
from typing import List, Dict, Any

def truncate_text(text: str, max_length: int = 280) -> str:
    """Truncate text to a specific length with ellipsis if needed."""
    return text if len(text) <= max_length else text[:max_length - 3] + "..."

def get_current_time_iso() -> str:
    """Return the current time in ISO format."""
    return datetime.datetime.utcnow().isoformat() + "Z"

def extract_hashtags(text: str) -> List[str]:
    """Extract hashtags from text."""
    return re.findall(r"#(\w+)", text)

def extract_mentions(text: str) -> List[str]:
    """Extract mentions from text."""
    return re.findall(r"@(\w+)", text)

def clean_text_for_analysis(text: str) -> str:
    """Clean text for sentiment analysis by removing URLs, mentions, and extra whitespace."""
    # Remove URLs
    text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
    
    # Remove mentions but keep the text
    text = re.sub(r'@\w+', '', text)
    
    # Remove hashtags but keep the text
    text = re.sub(r'#(\w+)', r'\1', text)
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()

    # Normalize to lowercase for consistency
    text = text.lower()
    return text

def get_word_count(text: str) -> int:
    """Get the word count of a text."""
    return len(text.split())

def get_sentence_count(text: str) -> int:
    """Get the sentence count of a text."""
    return len(re.split(r'[.!?]+', text))

def get_capitalization_ratio(text: str) -> float:
    """Get the ratio of capitalized letters to total letters."""
    if not text:
        return 0.0
    
    total_letters = len(re.findall(r'[a-zA-Z]', text))
    if total_letters == 0:
        return 0.0
    
    capital_letters = len(re.findall(r'[A-Z]', text))
    return capital_letters / total_letters

def is_valid_post(text: str, min_length: int = 10, max_length: int = 300) -> bool:
    """Check if a post is valid for analysis."""
    if not text or len(text.strip()) < min_length:
        return False
    
    if len(text) > max_length:
        return False
    
    return True

def format_timestamp(timestamp: str) -> str:
    """Format a timestamp for display."""
    try:
        dt = datetime.datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        return dt.strftime('%Y-%m-%d %H:%M:%S UTC')
    except Exception as e:
        print(f"Timestamp formatting error: {e}")
        return timestamp

def safe_get_nested(data: Dict[str, Any], *keys, default=None) -> Any:
    """Safely get nested dictionary values."""
    current = data
    for key in keys:
        if isinstance(current, dict) and key in current:
            current = current[key]
        else:
            return default
    return current 


# Emoji extraction utility
def extract_emojis(text: str) -> List[str]:
    """Extract emojis from the text."""
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags
        u"\U00002700-\U000027BF"  # dingbats
        u"\U0001F900-\U0001F9FF"  # supplemental symbols
        u"\U00002600-\U000026FF"  # miscellaneous symbols
        u"\U0001FA70-\U0001FAFF"  # extended symbols
        "]+", flags=re.UNICODE)
    return emoji_pattern.findall(text)
