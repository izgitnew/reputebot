#!/usr/bin/env python3
"""
Response generator for the Bluesky sentiment analysis bot.
"""

import random
from typing import Dict, Any

class ResponseGenerator:
    """Generates responses based on sentiment and vibe analysis."""
    
    def __init__(self):
        """Initialize the response generator."""
        # Vibe descriptions for the new format
        self.vibe_descriptions = {
            'positive': ['Positive', 'Optimistic', 'Uplifting', 'Encouraging'],
            'negative': ['Critical', 'Skeptical', 'Concerned', 'Cautious'],
            'neutral': ['Balanced', 'Thoughtful', 'Measured', 'Analytical'],
            'mixed': ['Complex', 'Nuanced', 'Varied', 'Dynamic']
        }
        
        # Persona mappings
        self.personas = {
            'tech': ['Builder', 'Innovator', 'Creator', 'Developer', 'Architect', 'Engineer'],
            'business': ['Leader', 'Strategist', 'Entrepreneur', 'Executive', 'Manager', 'Consultant'],
            'creative': ['Artist', 'Designer', 'Storyteller', 'Visionary', 'Creator', 'Craftsman'],
            'academic': ['Teacher', 'Researcher', 'Scholar', 'Educator', 'Professor', 'Mentor'],
            'social': ['Connector', 'Community Builder', 'Networker', 'Influencer', 'Organizer', 'Advocate'],
            'news': ['Reporter', 'Journalist', 'Analyst', 'Commentator', 'Correspondent', 'Editor'],
            'lifestyle': ['Enthusiast', 'Curator', 'Guide', 'Inspirer', 'Coach', 'Wellness Expert'],
            'sports': ['Fan', 'Analyst', 'Commentator', 'Enthusiast', 'Coach', 'Player'],
            'entertainment': ['Actor', 'Director', 'Producer', 'Performer', 'Host', 'Critic'],
            'gaming': ['Gamer', 'Streamer', 'Developer', 'Analyst', 'Commentator', 'Pro Player'],
            'finance': ['Investor', 'Analyst', 'Advisor', 'Trader', 'Planner', 'Expert'],
            'education': ['Teacher', 'Professor', 'Mentor', 'Trainer', 'Coach', 'Educator'],
            'health': ['Doctor', 'Nurse', 'Therapist', 'Coach', 'Specialist', 'Practitioner'],
            'environment': ['Activist', 'Scientist', 'Advocate', 'Researcher', 'Conservationist', 'Expert'],
            'politics': ['Politician', 'Analyst', 'Commentator', 'Activist', 'Reporter', 'Expert'],
            'science': ['Scientist', 'Researcher', 'Professor', 'Analyst', 'Expert', 'Scholar']
        }
        
        # Activity levels
        self.activity_levels = {
            'high': ['~3+ posts/day', '~4 posts/day', '~5 posts/day'],
            'medium': ['~1-2 posts/day', '~2 posts/day', '~1.5 posts/day'],
            'low': ['~0.5 posts/day', '~1 post/day', 'occasional posts']
        }
        
        # Feed categories
        self.feed_categories = {
            'tech': 'Tech Feed',
            'business': 'Business Feed', 
            'creative': 'Creative Feed',
            'academic': 'Academic Feed',
            'social': 'Social Feed',
            'news': 'News Feed',
            'lifestyle': 'Lifestyle Feed',
            'sports': 'Sports Feed',
            'entertainment': 'Entertainment Feed',
            'gaming': 'Gaming Feed',
            'finance': 'Finance Feed',
            'education': 'Education Feed',
            'health': 'Health Feed',
            'environment': 'Environment Feed',
            'politics': 'Politics Feed',
            'science': 'Science Feed',
            'general': 'General Feed'
        }
        
        # Content keywords for categorization
        self.content_keywords = {
            'tech': [
                'code', 'programming', 'software', 'ai', 'technology', 'startup', 'development', 'api', 'database', 'algorithm',
                'javascript', 'python', 'react', 'node', 'aws', 'cloud', 'devops', 'cybersecurity', 'blockchain', 'crypto',
                'machine learning', 'ml', 'data science', 'analytics', 'backend', 'frontend', 'mobile', 'ios', 'android',
                'web3', 'metaverse', 'vr', 'ar', 'iot', 'automation', 'scalability', 'microservices', 'kubernetes', 'docker',
                'git', 'github', 'stack', 'framework', 'library', 'package', 'deployment', 'testing', 'debugging', 'optimization',
                'server', 'client', 'protocol', 'interface', 'architecture', 'infrastructure', 'platform', 'service', 'application'
            ],
            'business': [
                'business', 'strategy', 'leadership', 'entrepreneur', 'marketing', 'finance', 'investment', 'revenue', 'growth',
                'startup', 'venture capital', 'vc', 'funding', 'pitch', 'pivot', 'scaling', 'acquisition', 'merger', 'ipo',
                'profit', 'loss', 'roi', 'kpi', 'metrics', 'analytics', 'sales', 'customer', 'product', 'market', 'competition',
                'brand', 'advertising', 'campaign', 'social media', 'content', 'seo', 'sem', 'conversion', 'retention', 'churn',
                'team', 'hiring', 'culture', 'remote', 'office', 'meeting', 'presentation', 'pitch deck', 'business plan'
            ],
            'creative': [
                'art', 'design', 'creative', 'music', 'film', 'photography', 'writing', 'poetry', 'illustration', 'animation',
                'painting', 'drawing', 'sculpture', 'digital art', 'graphic design', 'ui', 'ux', 'typography', 'color', 'composition',
                'cinematography', 'editing', 'directing', 'acting', 'screenplay', 'script', 'storyboard', 'visual effects', 'vfx',
                'composing', 'producing', 'recording', 'mixing', 'mastering', 'concert', 'performance', 'gallery', 'exhibition',
                'portfolio', 'commission', 'freelance', 'client', 'project', 'deadline', 'inspiration', 'muse', 'style', 'aesthetic'
            ],
            'academic': [
                'research', 'study', 'education', 'science', 'analysis', 'theory', 'paper', 'conference', 'journal', 'methodology',
                'phd', 'thesis', 'dissertation', 'peer review', 'citation', 'bibliography', 'hypothesis', 'experiment', 'data',
                'statistics', 'survey', 'interview', 'qualitative', 'quantitative', 'literature review', 'findings', 'conclusion',
                'university', 'college', 'professor', 'lecturer', 'student', 'course', 'curriculum', 'syllabus', 'assignment',
                'grading', 'academic', 'scholarly', 'intellectual', 'knowledge', 'learning', 'teaching', 'pedagogy', 'curriculum'
            ],
            'social': [
                'community', 'social', 'people', 'relationships', 'networking', 'friends', 'family', 'support', 'connection',
                'conversation', 'discussion', 'debate', 'dialogue', 'collaboration', 'partnership', 'alliance', 'coalition',
                'group', 'team', 'organization', 'association', 'society', 'club', 'meetup', 'event', 'gathering', 'celebration',
                'mentorship', 'coaching', 'guidance', 'advice', 'help', 'assistance', 'volunteer', 'charity', 'donation', 'cause',
                'advocacy', 'activism', 'movement', 'campaign', 'petition', 'protest', 'rally', 'demonstration', 'solidarity'
            ],
            'news': [
                'news', 'politics', 'current events', 'breaking', 'update', 'report', 'announcement', 'statement', 'official',
                'headline', 'story', 'article', 'coverage', 'investigation', 'exclusive', 'scoop', 'leak', 'source', 'anonymous',
                'government', 'policy', 'legislation', 'bill', 'law', 'regulation', 'election', 'vote', 'campaign', 'candidate',
                'democracy', 'republic', 'constitution', 'rights', 'freedom', 'justice', 'court', 'judge', 'lawyer', 'legal',
                'international', 'foreign', 'diplomacy', 'treaty', 'alliance', 'conflict', 'war', 'peace', 'negotiation', 'summit'
            ],
            'lifestyle': [
                'lifestyle', 'health', 'fitness', 'food', 'travel', 'wellness', 'recipe', 'workout', 'meditation', 'self-care',
                'nutrition', 'diet', 'organic', 'vegan', 'vegetarian', 'gluten-free', 'keto', 'paleo', 'supplements', 'vitamins',
                'exercise', 'training', 'gym', 'yoga', 'pilates', 'running', 'cycling', 'swimming', 'weightlifting', 'cardio',
                'mental health', 'therapy', 'counseling', 'mindfulness', 'stress', 'anxiety', 'depression', 'happiness', 'joy',
                'fashion', 'style', 'outfit', 'trend', 'beauty', 'skincare', 'makeup', 'hair', 'accessories', 'shopping'
            ],
            'sports': [
                'sports', 'basketball', 'football', 'soccer', 'baseball', 'athlete', 'team', 'coach',
                'falcons', 'nfl', 'nba', 'mlb', 'nhl', 'tennis', 'golf', 'olympics', 'championship', 'playoff',
                'season', 'draft', 'trade', 'injury', 'stats', 'score', 'win', 'loss', 'victory', 'defeat', 'price',
                'move', 'risk', 'quarterback', 'running back', 'wide receiver', 'defense', 'offense', 'touchdown', 'field goal',
                'home run', 'strikeout', 'basket', 'three pointer', 'free throw', 'rebound', 'assist', 'steal', 'block',
                'goalie', 'midfielder', 'forward', 'defender', 'goal', 'yellow card', 'red card', 'penalty',
                'ace', 'serve', 'volley', 'backhand', 'forehand', 'match point', 'set', 'tournament', 'grand slam',
                'putt', 'drive', 'iron', 'wood', 'par', 'birdie', 'eagle', 'bogey', 'course', 'green', 'fairway', 'rough'
            ],
            'entertainment': [
                'movie', 'film', 'tv', 'television', 'show', 'series', 'episode', 'season', 'premiere', 'finale',
                'actor', 'actress', 'director', 'producer', 'screenwriter', 'cinematographer', 'editor', 'composer',
                'award', 'oscar', 'emmy', 'grammy', 'tony', 'golden globe', 'nomination', 'winner', 'ceremony',
                'red carpet', 'premiere', 'screening', 'box office', 'revenue', 'budget', 'trailer', 'teaser',
                'comedy', 'drama', 'action', 'horror', 'thriller', 'romance', 'sci-fi', 'fantasy', 'documentary',
                'reality tv', 'game show', 'talk show', 'news', 'late night', 'morning show', 'streaming', 'netflix',
                'hulu', 'disney', 'amazon', 'hbo', 'apple', 'youtube', 'podcast', 'radio', 'broadcast', 'live'
            ],
            'gaming': [
                'game', 'gaming', 'video game', 'console', 'pc', 'playstation', 'xbox', 'nintendo', 'switch',
                'rpg', 'fps', 'mmo', 'moba', 'strategy', 'puzzle', 'platformer', 'adventure', 'simulation',
                'esports', 'tournament', 'competitive', 'ranked', 'matchmaking', 'leaderboard', 'achievement',
                'level', 'quest', 'mission', 'boss', 'enemy', 'weapon', 'armor', 'skill', 'ability', 'upgrade',
                'multiplayer', 'co-op', 'pvp', 'pve', 'guild', 'clan', 'team', 'squad', 'party', 'lobby',
                'stream', 'twitch', 'youtube gaming', 'speedrun', 'glitch', 'mod', 'dlc', 'expansion', 'update'
            ],
            'finance': [
                'finance', 'money', 'investment', 'stock', 'market', 'trading', 'portfolio', 'dividend', 'interest',
                'crypto', 'bitcoin', 'ethereum', 'blockchain', 'nft', 'defi', 'token', 'coin', 'wallet', 'exchange',
                'bank', 'account', 'credit', 'debit', 'loan', 'mortgage', 'insurance', 'retirement', '401k', 'ira',
                'tax', 'deduction', 'refund', 'income', 'salary', 'bonus', 'commission', 'profit', 'loss', 'revenue',
                'budget', 'expense', 'saving', 'spending', 'debt', 'credit score', 'fico', 'lending', 'borrowing'
            ],
            'education': [
                'education', 'learning', 'teaching', 'school', 'university', 'college', 'course', 'class', 'lecture',
                'student', 'teacher', 'professor', 'instructor', 'tutor', 'mentor', 'coach', 'trainer', 'educator',
                'curriculum', 'syllabus', 'assignment', 'homework', 'project', 'exam', 'test', 'quiz', 'grade',
                'degree', 'certificate', 'diploma', 'major', 'minor', 'concentration', 'specialization', 'field',
                'online', 'distance', 'virtual', 'hybrid', 'blended', 'traditional', 'classroom', 'campus', 'dorm'
            ],
            'health': [
                'health', 'medical', 'doctor', 'nurse', 'physician', 'surgeon', 'specialist', 'clinic', 'hospital',
                'diagnosis', 'treatment', 'therapy', 'medication', 'prescription', 'surgery', 'procedure', 'recovery',
                'symptom', 'condition', 'disease', 'illness', 'infection', 'injury', 'pain', 'fever', 'cough',
                'mental health', 'psychology', 'psychiatry', 'therapist', 'counselor', 'psychologist', 'psychiatrist',
                'anxiety', 'depression', 'stress', 'trauma', 'ptsd', 'ocd', 'adhd', 'autism', 'bipolar', 'schizophrenia'
            ],
            'environment': [
                'environment', 'climate', 'sustainability', 'green', 'eco', 'renewable', 'solar', 'wind', 'energy',
                'pollution', 'emissions', 'carbon', 'footprint', 'recycling', 'waste', 'plastic', 'ocean', 'forest',
                'wildlife', 'conservation', 'preservation', 'extinction', 'endangered', 'species', 'habitat', 'ecosystem',
                'global warming', 'climate change', 'temperature', 'weather', 'storm', 'hurricane', 'drought', 'flood',
                'agriculture', 'farming', 'organic', 'pesticide', 'fertilizer', 'soil', 'water', 'air', 'quality'
            ],
            'politics': [
                'politics', 'political', 'government', 'policy', 'legislation', 'law', 'bill', 'act', 'regulation',
                'election', 'vote', 'voting', 'campaign', 'candidate', 'politician', 'senator', 'representative',
                'president', 'vice president', 'governor', 'mayor', 'congress', 'senate', 'house', 'parliament',
                'democracy', 'republic', 'constitution', 'amendment', 'rights', 'freedom', 'liberty', 'justice',
                'liberal', 'conservative', 'progressive', 'moderate', 'independent', 'party', 'republican', 'democrat'
            ],
            'science': [
                'science', 'scientific', 'research', 'study', 'experiment', 'hypothesis', 'theory', 'discovery',
                'physics', 'chemistry', 'biology', 'astronomy', 'geology', 'meteorology', 'oceanography', 'ecology',
                'laboratory', 'lab', 'scientist', 'researcher', 'professor', 'phd', 'postdoc', 'fellowship',
                'publication', 'paper', 'journal', 'conference', 'presentation', 'poster', 'abstract', 'citation',
                'data', 'analysis', 'statistics', 'model', 'simulation', 'computation', 'algorithm', 'methodology'
            ]
        }
    
    def _get_vibe_description(self, vibe_score: float) -> str:
        """Get a vibe description based on the vibe score."""
        if vibe_score > 0.2:  # Lowered from 0.3
            return random.choice(self.vibe_descriptions['positive'])
        elif vibe_score < -0.2:  # Raised from -0.3
            return random.choice(self.vibe_descriptions['negative'])
        elif -0.05 <= vibe_score <= 0.05:  # Tightened neutral range
            return random.choice(self.vibe_descriptions['neutral'])
        else:
            return random.choice(self.vibe_descriptions['mixed'])
    
    def _get_persona(self, content: str) -> str:
        """Determine the persona based on content keywords."""
        content_lower = content.lower()
        content_words = set(content_lower.split())
        
        # Score each category based on keyword matches
        category_scores = {}
        
        for category, keywords in self.content_keywords.items():
            score = 0
            for keyword in keywords:
                if keyword in content_words or keyword in content_lower:
                    score += 1
            if score > 0:
                category_scores[category] = score
        
        # Return persona from category with highest score
        if category_scores:
            best_category = max(category_scores, key=category_scores.get)
            return random.choice(self.personas.get(best_category, ['Creator']))
        
        return random.choice(['Creator', 'Thinker', 'Builder'])
    
    def _get_activity_level(self, post_count: int) -> str:
        """Get activity level based on post count."""
        if post_count >= 10:  # High activity accounts (10+ posts/day)
            return random.choice(self.activity_levels['high'])
        elif post_count >= 3:  # Medium activity accounts (3-9 posts/day)
            return random.choice(self.activity_levels['medium'])
        else:  # Low activity accounts (<3 posts/day)
            return random.choice(self.activity_levels['low'])
    
    def _calculate_posts_per_day(self, posts_data: list) -> float:
        """Calculate actual posts per day by counting posts from the last 30 days."""
        if not posts_data:
            return 1.0  # Default if we can't calculate
        
        try:
            from datetime import datetime, timedelta, timezone
            
            # Get current time (timezone-aware)
            now = datetime.now(timezone.utc)
            # Calculate 30 days ago
            thirty_days_ago = now - timedelta(days=30)
            
            posts_in_last_30d = 0
            
            # Check if we're getting timestamps or full post objects
            if posts_data and isinstance(posts_data[0], str):
                # We have timestamps directly
                for timestamp in posts_data:
                    try:
                        post_time = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                        if post_time >= thirty_days_ago:
                            posts_in_last_30d += 1
                    except (ValueError, TypeError):
                        continue
            else:
                # We have full post objects, extract timestamps
                for post in posts_data:
                    # Extract timestamp
                    timestamp = None
                    if hasattr(post, 'post') and hasattr(post.post, 'record') and hasattr(post.post.record, 'created_at'):
                        timestamp = post.post.record.created_at
                    elif hasattr(post, 'post') and hasattr(post.post, 'record') and hasattr(post.post.record, 'createdAt'):
                        timestamp = post.post.record.createdAt
                    elif hasattr(post, 'record') and hasattr(post.record, 'createdAt'):
                        timestamp = post.record.createdAt
                    elif hasattr(post, 'createdAt'):
                        timestamp = post.createdAt
                    else:
                        continue
                    
                    # Parse timestamp
                    try:
                        post_time = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                        # Check if post is within last 30 days
                        if post_time >= thirty_days_ago:
                            posts_in_last_30d += 1
                    except (ValueError, TypeError):
                        continue
            
            # Calculate average posts per day over the last 30 days
            posts_per_day = posts_in_last_30d / 30.0
            
            print(f"📊 Found {posts_in_last_30d} posts in the last 30 days = {posts_per_day:.1f} posts/day average")
            return round(posts_per_day, 1)
                
        except Exception as e:
            print(f"❌ Error calculating posts per day: {e}")
            return 1.0
    
    def _get_feed_category(self, content: str) -> str:
        """Determine the appropriate feed category."""
        content_lower = content.lower()
        content_words = set(content_lower.split())
        
        # Score each category based on keyword matches
        category_scores = {}
        
        for category, keywords in self.content_keywords.items():
            score = 0
            for keyword in keywords:
                if keyword in content_words or keyword in content_lower:
                    score += 1
            if score > 0:
                category_scores[category] = score
        
        # Return feed category from category with highest score
        if category_scores:
            best_category = max(category_scores, key=category_scores.get)
            return self.feed_categories[best_category]
        
        return self.feed_categories['general']
    
    def _should_respond(self, sentiment_score: float, vibe_score: float) -> bool:
        """Determine if we should respond to this content."""
        # Always respond to mentions
        return True
    
    def generate_response(self, sentiment_result: Dict[str, Any], vibe_result: Dict[str, Any], content: str, handle: str, posts_data: list = None) -> str:
        """Generate a response based on sentiment and vibe analysis."""
        # Extract scores from the correct structure
        sentiment_score = sentiment_result['vader_scores']['compound']
        vibe_score = vibe_result['overall_vibe']
        
        if not self._should_respond(sentiment_score, vibe_score):
            return None
        
        # Calculate actual posts per day if posts data is provided
        if posts_data:
            posts_per_day = self._calculate_posts_per_day(posts_data)
            print(f"📊 Calculated posts per day: {posts_per_day}")
            # Convert to activity level description using the same thresholds as _get_activity_level
            if posts_per_day >= 10:  # High activity accounts (10+ posts/day)
                activity = random.choice(self.activity_levels['high'])
            elif posts_per_day >= 3:  # Medium activity accounts (3-9 posts/day)
                activity = random.choice(self.activity_levels['medium'])
            else:  # Low activity accounts (<3 posts/day)
                activity = random.choice(self.activity_levels['low'])
        else:
            # Fallback to estimated post count
            post_count = max(1, len(content.split()) // 20)
            activity = self._get_activity_level(post_count)
        
        # Generate components
        vibe_desc = self._get_vibe_description(vibe_score)
        persona = self._get_persona(content)
        feed_category = self._get_feed_category(content)
        
        # Determine recommendation
        if sentiment_score > 0.1 and vibe_score > 0.1:
            recommendation = "✅ Yes — here's why:"
        elif sentiment_score < -0.1 or vibe_score < -0.1:
            recommendation = "❌ No — here's why:"
        else:
            recommendation = "🤔 Maybe — here's why:"
        
        # Generate response
        response = f"""Should you follow @{handle}?
{recommendation}
🔹 Vibes: {vibe_desc}
🔹 Persona: {persona}
🔹 ~{posts_per_day:.0f} posts/day, mostly original
🔹 Posts on {feed_category.lower().replace(' feed', '')}
📌 Add to your {feed_category}."""
        
        return response
