#!/usr/bin/env python3
"""
Debug script to test bot components individually.
"""

import asyncio
from dotenv import load_dotenv
from bluesky import BlueskyClient
from vibe import VibeAnalyzer
from analyze import SentimentAnalyzer
from responder import ResponseGenerator

# Load environment variables
load_dotenv()

async def test_bot_components():
    """Test individual bot components."""
    print("🔧 Testing Bot Components...")
    
    # Initialize components
    sentiment_analyzer = SentimentAnalyzer()
    vibe_analyzer = VibeAnalyzer()
    response_generator = ResponseGenerator()
    bluesky_client = BlueskyClient()
    
    # Set up the processing pipeline
    bluesky_client.sentiment_analyzer = sentiment_analyzer
    bluesky_client.vibe_analyzer = vibe_analyzer
    bluesky_client.response_generator = response_generator
    
    try:
        # Test login
        print("\n1️⃣ Testing login...")
        await bluesky_client.login()
        print("✅ Login successful")
        
        # Test notifications fetch
        print("\n2️⃣ Testing notifications fetch...")
        notifications = await bluesky_client.get_notifications(limit=5)
        print(f"✅ Found {len(notifications)} notifications")
        
        # Test response generation
        print("\n3️⃣ Testing response generation...")
        test_content = "This is a test post about technology and innovation. #tech #ai #future"
        sentiment = sentiment_analyzer.analyze_sentiment(test_content)
        vibe = vibe_analyzer.analyze_vibe(test_content)
        response = response_generator.generate_response(sentiment, vibe, test_content, "testuser.bsky.social")
        
        print(f"📝 Generated response ({len(response)} chars):")
        print(response[:200] + "..." if len(response) > 200 else response)
        
        # Test truncation
        print(f"\n4️⃣ Testing truncation...")
        if len(response) > 280:
            truncated = response[:277] + "..."
            print(f"📝 Would truncate to {len(truncated)} chars")
        else:
            print("✅ Response fits within limit")
            
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_bot_components()) 