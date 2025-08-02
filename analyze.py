#!/usr/bin/env python3
"""
Sentiment analyzer for detailed analysis of post sentiment.
"""

import re
from typing import Dict, List, Tuple
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

class SentimentAnalyzer:
    """Analyzes sentiment of posts in detail."""
    
    def __init__(self):
        """Initialize the sentiment analyzer."""
        self.analyzer = SentimentIntensityAnalyzer()
        
        # Custom sentiment words for social media context
        self.custom_words = {
            'positive': {
                'lol': 0.3,
                'haha': 0.3,
                'omg': 0.2,
                'wow': 0.2,
                'cool': 0.3,
                'nice': 0.3,
                'awesome': 0.8,
                'amazing': 0.8,
                'love': 0.8,
                'heart': 0.6,
                'fire': 0.7,
                'lit': 0.7,
                'slay': 0.6,
                'queen': 0.5,
                'king': 0.5,
                'goals': 0.4,
                'mood': 0.2,
                'vibes': 0.3,
                'blessed': 0.6,
                'grateful': 0.7
            },
            'negative': {
                'smh': -0.4,
                'fml': -0.8,
                'ugh': -0.5,
                'sigh': -0.4,
                'cringe': -0.6,
                'yikes': -0.3,
                'oof': -0.3,
                'bruh': -0.2,
                'wtf': -0.5,
                'omfg': -0.6,
                'kill': -0.8,
                'die': -0.8,
                'hate': -0.8,
                'terrible': -0.8,
                'awful': -0.8,
                'horrible': -0.8
            }
        }
        
        # Add custom words to the analyzer
        self._add_custom_words()
    
    def _add_custom_words(self):
        """Add custom sentiment words to the analyzer."""
        for sentiment, words in self.custom_words.items():
            for word, score in words.items():
                self.analyzer.lexicon[word] = score
    
    def analyze_sentiment(self, text: str) -> Dict[str, any]:
        """Analyze the sentiment of a text."""
        # Clean the text
        cleaned_text = self._clean_text(text)
        
        # Get VADER sentiment scores
        vader_scores = self.analyzer.polarity_scores(cleaned_text)
        
        # Get detailed analysis
        detailed_analysis = self._get_detailed_analysis(cleaned_text)
        
        # Get emotional indicators
        emotional_indicators = self._analyze_emotional_indicators(text)
        
        return {
            'overall_sentiment': self._get_overall_sentiment(vader_scores['compound']),
            'vader_scores': vader_scores,
            'detailed_analysis': detailed_analysis,
            'emotional_indicators': emotional_indicators,
            'text_length': len(cleaned_text),
            'word_count': len(cleaned_text.split()),
            'sentence_count': len(re.split(r'[.!?]+', cleaned_text)),
            'exclamation_count': text.count('!'),
            'question_count': text.count('?'),
            'capitalization_ratio': self._get_capitalization_ratio(text),
            'emoji_sentiment': self._analyze_emoji_sentiment(text)
        }
    
    def _clean_text(self, text: str) -> str:
        """Clean text for sentiment analysis."""
        # Remove URLs
        text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
        
        # Remove mentions but keep the text
        text = re.sub(r'@\w+', '', text)
        
        # Remove hashtags but keep the text
        text = re.sub(r'#(\w+)', r'\1', text)
        
        # Remove emojis (we'll analyze them separately)
        text = re.sub(r'[^\w\s.,!?]', '', text)
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def _get_detailed_analysis(self, text: str) -> Dict[str, any]:
        """Get detailed sentiment analysis."""
        words = text.lower().split()
        
        positive_words = []
        negative_words = []
        neutral_words = []
        
        for word in words:
            if word in self.analyzer.lexicon:
                score = self.analyzer.lexicon[word]
                if score > 0:
                    positive_words.append((word, score))
                elif score < 0:
                    negative_words.append((word, score))
                else:
                    neutral_words.append(word)
            else:
                neutral_words.append(word)
        
        return {
            'positive_words': sorted(positive_words, key=lambda x: x[1], reverse=True),
            'negative_words': sorted(negative_words, key=lambda x: x[1]),
            'neutral_words': neutral_words,
            'positive_word_count': len(positive_words),
            'negative_word_count': len(negative_words),
            'neutral_word_count': len(neutral_words)
        }
    
    def _analyze_emotional_indicators(self, text: str) -> Dict[str, int]:
        """Analyze emotional indicators in the text."""
        indicators = {
            'exclamations': text.count('!'),
            'questions': text.count('?'),
            'ellipsis': text.count('...'),
            'all_caps_words': len(re.findall(r'\b[A-Z]{2,}\b', text)),
            'repeated_letters': len(re.findall(r'(\w)\1{2,}', text)),
            'emoticons': len(re.findall(r'[:;=]-?[)(/\\|pPoO]', text))
        }
        
        return indicators
    
    def _get_capitalization_ratio(self, text: str) -> float:
        """Get the ratio of capitalized letters to total letters."""
        if not text:
            return 0.0
        
        total_letters = len(re.findall(r'[a-zA-Z]', text))
        if total_letters == 0:
            return 0.0
        
        capital_letters = len(re.findall(r'[A-Z]', text))
        return capital_letters / total_letters
    
    def _analyze_emoji_sentiment(self, text: str) -> Dict[str, any]:
        """Analyze emoji sentiment."""
        # Common emoji sentiment mappings
        emoji_sentiment = {
            '😀😃😄😁😆😅😂🤣😊😇': 0.8,  # Very positive
            '🙂🙃😉😌😍🥰😘😗😙😚': 0.6,  # Positive
            '😋😛😝😜🤪🤨🧐🤓😎': 0.4,  # Slightly positive
            '😐😑😶😏😒🙄😬🤥': 0.0,  # Neutral
            '😔😟😕🙁☹️😣😖😫😩': -0.4,  # Negative
            '🥺😢😭😤😠😡🤬🤯😳': -0.6,  # Very negative
            '😱😨😰😥😓🤗🤔🤭🤫🤥': -0.2,  # Slightly negative
            '😈👿👹👺💀☠️👻👽👾🤖': -0.3,  # Spooky/negative
            '💪👊👋👌👍👎👏🙌👐🤲': 0.3,  # Gestures
            '❤️💛💚💙💜🖤💔❣️💕💞': 0.7,  # Hearts
            '🔥💯✨🌟💫⭐💥💢💦💨': 0.5,  # Effects
            '🎉🎊🎈🎂🎁🎄🎃🎗️🎟️🎫': 0.6,  # Celebrations
        }
        
        found_emojis = []
        total_sentiment = 0
        emoji_count = 0
        
        for emoji_group, sentiment in emoji_sentiment.items():
            for emoji in emoji_group:
                if emoji in text:
                    count = text.count(emoji)
                    found_emojis.extend([emoji] * count)
                    total_sentiment += sentiment * count
                    emoji_count += count
        
        return {
            'found_emojis': found_emojis,
            'emoji_count': emoji_count,
            'average_emoji_sentiment': total_sentiment / emoji_count if emoji_count > 0 else 0,
            'total_emoji_sentiment': total_sentiment
        }
    
    def _get_overall_sentiment(self, compound_score: float) -> str:
        """Get overall sentiment label."""
        if compound_score >= 0.05:
            return 'positive'
        elif compound_score <= -0.05:
            return 'negative'
        else:
            return 'neutral' 


    def summarize_user(self, posts: List[str]) -> Dict[str, any]:
        """Summarize a user's sentiment and behavioral profile from their posts."""
        sentiments = [self.analyze_sentiment(p) for p in posts if p.strip()]
        if not sentiments:
            return {}

        avg = lambda key: sum(s[key] for s in sentiments) / len(sentiments)
        avg_emoji = lambda: sum(s['emoji_sentiment']['average_emoji_sentiment'] for s in sentiments) / len(sentiments)

        summary = {
            'avg_compound': avg('vader_scores')['compound'],
            'avg_pos': avg('vader_scores')['pos'],
            'avg_neg': avg('vader_scores')['neg'],
            'avg_caps': avg('capitalization_ratio'),
            'avg_exclamations': avg('exclamation_count'),
            'avg_questions': avg('question_count'),
            'avg_emoji_sentiment': avg_emoji(),
            'vibe': self._get_overall_sentiment(avg('vader_scores')['compound']),
            'archetype': self.detect_archetype(posts, avg),
        }
        return summary

    def detect_archetype(self, posts: List[str], avg_fn) -> str:
        """Identify user archetype based on behavior and tone."""
        avg_caps = avg_fn('capitalization_ratio')
        avg_pos = avg_fn('vader_scores')['pos']
        avg_neg = avg_fn('vader_scores')['neg']
        avg_exclamations = avg_fn('exclamation_count')
        avg_questions = avg_fn('question_count')

        if avg_neg > 0.4 and avg_caps > 0.2:
            return "Shitposter"
        if avg_pos > 0.5 and avg_questions > 1.5:
            return "Teacher"
        if avg_caps > 0.15 and avg_exclamations > 1:
            return "Builder"
        if avg_pos < 0.2 and avg_neg < 0.2:
            return "Observer"
        return "Explorer"

    def score_feeds(self, posts: List[str], feeds_dict: Dict[str, List[str]]) -> List[str]:
        """Rank feeds based on keyword relevance in user posts."""
        combined_text = " ".join(posts).lower()
        keywords = re.findall(r'\b\w+\b', combined_text)
        from collections import Counter
        word_counts = Counter(keywords)

        feed_scores = []
        for feed, terms in feeds_dict.items():
            score = sum(word_counts[t.lower()] for t in terms if t.lower() in word_counts)
            feed_scores.append((feed, score))

        ranked = sorted(feed_scores, key=lambda x: x[1], reverse=True)
        return [feed for feed, score in ranked if score > 0]
