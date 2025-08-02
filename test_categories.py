#!/usr/bin/env python3
"""
Test script to verify the improved category detection and activity levels.
"""

from responder import ResponseGenerator

def test_categories():
    """Test the category detection and activity levels."""
    print("🧪 Testing Category Detection and Activity Levels...")
    
    response_gen = ResponseGenerator()
    
    # Test different content types
    test_cases = [
        {
            "content": "The Falcons would have to pay an absurd price in a trade for this player. Looking at the stats and game film, this is a high-risk move.",
            "post_count": 10,
            "description": "Sports content (Falcons)"
        },
        {
            "content": "Just deployed the new API with improved database performance. The algorithm optimization reduced response time by 40%.",
            "post_count": 8,
            "description": "Tech content"
        },
        {
            "content": "Beautiful sunset at the beach today. Perfect weather for a relaxing evening walk.",
            "post_count": 3,
            "description": "Lifestyle content"
        },
        {
            "content": "Breaking news: Major announcement expected from the government today. Stay tuned for updates.",
            "post_count": 20,
            "description": "News content (high activity)"
        },
        {
            "content": "Bitcoin just hit a new all-time high! The crypto market is showing incredible momentum with Ethereum and other altcoins following suit.",
            "post_count": 15,
            "description": "Finance content (Crypto)"
        },
        {
            "content": "New research shows promising results in cancer treatment. The clinical trial data indicates a 60% improvement in patient outcomes.",
            "post_count": 12,
            "description": "Health/Science content"
        },
        {
            "content": "Climate change is accelerating faster than predicted. We need immediate action on renewable energy and carbon reduction.",
            "post_count": 7,
            "description": "Environment content"
        },
        {
            "content": "The new RPG game just launched and it's incredible! The graphics are stunning and the multiplayer features are revolutionary.",
            "post_count": 18,
            "description": "Gaming content"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n--- Test Case {i}: {test_case['description']} ---")
        print(f"Content: {test_case['content'][:60]}...")
        print(f"Post count: {test_case['post_count']}")
        
        # Test vibe description
        vibe_score = 0.25  # Positive vibe
        vibe_desc = response_gen._get_vibe_description(vibe_score)
        print(f"🔹 Vibes: {vibe_desc}")
        
        # Test persona
        persona = response_gen._get_persona(test_case['content'])
        print(f"🔹 Persona: {persona}")
        
        # Test activity level
        activity = response_gen._get_activity_level(test_case['post_count'])
        print(f"🔹 Activity: {activity}")
        
        # Test feed category
        feed_category = response_gen._get_feed_category(test_case['content'])
        print(f"🔹 Feed: {feed_category}")
        
        print(f"📌 Add to your {feed_category}")
    
    print("\n✅ Category testing completed!")

if __name__ == "__main__":
    test_categories() 