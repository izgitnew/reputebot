#!/usr/bin/env python3
"""
Vibe analyzer for determining the overall mood and tone of posts.
"""

import re
import string
from typing import Dict, List, Tuple
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

class VibeAnalyzer:
    """Analyzes the overall vibe/mood of posts."""
    
    def __init__(self):
        """Initialize the vibe analyzer."""
        self.sentiment_analyzer = SentimentIntensityAnalyzer()
        
        # Keywords that indicate different vibes
        self.vibe_keywords = {
            'positive': [
                'amazing', 'awesome', 'beautiful', 'brilliant', 'excellent', 'fantastic',
                'great', 'incredible', 'love', 'wonderful', 'perfect', 'happy', 'joy',
                'excited', 'thrilled', 'grateful', 'blessed', 'inspired', 'motivated'
            ],
            'negative': [
                'terrible', 'awful', 'horrible', 'disgusting', 'hate', 'angry',
                'frustrated', 'disappointed', 'sad', 'depressed', 'anxious', 'worried',
                'scared', 'terrified', 'devastated', 'heartbroken', 'miserable'
            ],
            'neutral': [
                'okay', 'fine', 'alright', 'normal', 'regular', 'standard', 'average',
                'decent', 'acceptable', 'reasonable', 'moderate', 'balanced'
            ],
            'intense': [
                'absolutely', 'completely', 'totally', 'extremely', 'incredibly',
                'massively', 'hugely', 'enormously', 'dramatically', 'radically'
            ],
            'casual': [
                'lol', 'haha', 'omg', 'wow', 'cool', 'nice', 'yeah', 'yep', 'nope',
                'idk', 'imo', 'tbh', 'btw', 'fyi', 'jk', 'smh', 'fml'
            ]
        }
    
    # TODO: Future enhancement: Use context window or co-occurrence with emojis for sarcasm detection
    def analyze_vibe(self, text: str) -> Dict[str, float]:
        """Analyze the overall vibe of a text."""
        # Clean the text
        cleaned_text = self._clean_text(text)
        
        # Get sentiment scores
        sentiment_scores = self.sentiment_analyzer.polarity_scores(cleaned_text)
        
        # Analyze keyword presence
        keyword_scores = self._analyze_keywords(cleaned_text)
        
        # Combine sentiment and keyword analysis
        vibe_score = self._combine_scores(sentiment_scores, keyword_scores)
        
        return {
            'overall_vibe': vibe_score,
            'sentiment': sentiment_scores,
            'keyword_analysis': keyword_scores,
            'text_length': len(cleaned_text),
            'hashtags': self._extract_hashtags(text),
            'mentions': self._extract_mentions(text)
        }
    
    def _clean_text(self, text: str) -> str:
        """Clean text for analysis."""
        # Remove URLs
        text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
        
        # Remove mentions but keep the text
        text = re.sub(r'@\w+', '', text)
        
        # Remove hashtags but keep the text
        text = re.sub(r'#(\w+)', r'\1', text)
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def _analyze_keywords(self, text: str) -> Dict[str, float]:
        """Analyze presence of vibe keywords."""
        text_lower = text.lower()
        scores = {}
        
        for vibe_type, keywords in self.vibe_keywords.items():
            count = sum(len(re.findall(rf'\\b{re.escape(keyword)}\\b', text_lower)) for keyword in keywords)
            scores[vibe_type] = count / len(keywords) if keywords else 0
        
        return scores
    
    def _combine_scores(self, sentiment_scores: Dict[str, float], keyword_scores: Dict[str, float]) -> float:
        """Combine sentiment and keyword scores into overall vibe."""
        # Base score from sentiment
        base_score = sentiment_scores['compound']
        
        # Adjust based on keyword presence
        if keyword_scores['positive'] > 0.1:
            base_score += 0.2
        if keyword_scores['negative'] > 0.1:
            base_score -= 0.2
        if keyword_scores['intense'] > 0.1:
            base_score *= 1.5  # Amplify the sentiment
        if keyword_scores['casual'] > 0.1:
            base_score *= 0.8  # Tone down the sentiment
        
        # Clamp to [-1, 1] range
        return max(-1.0, min(1.0, base_score))
    
    def _extract_hashtags(self, text: str) -> List[str]:
        """Extract hashtags from text."""
        return re.findall(r'#(\w+)', text)
    
    def _extract_mentions(self, text: str) -> List[str]:
        """Extract mentions from text."""
        return re.findall(r'@(\w+)', text)
    
    def get_vibe_description(self, vibe_score: float) -> str:
        """Get a human-readable description of the vibe."""
        if vibe_score >= 0.8:
            return "extremely positive"
        elif vibe_score >= 0.5:
            return "very positive"
        elif vibe_score >= 0.2:
            return "positive"
        elif vibe_score >= -0.2:
            return "neutral"
        elif vibe_score >= -0.5:
            return "negative"
        elif vibe_score >= -0.8:
            return "very negative"
        else:
            return "extremely negative" 
