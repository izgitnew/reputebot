#!/usr/bin/env python3
"""
Test script to verify posting functionality.
"""

import asyncio
from dotenv import load_dotenv
from bluesky import BlueskyClient
from vibe import VibeAnalyzer
from analyze import SentimentAnalyzer
from responder import ResponseGenerator

# Load environment variables
load_dotenv()

async def test_posting():
    """Test the posting functionality."""
    print("📝 Testing Posting Functionality...")
    
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
        # Login
        await bluesky_client.login()
        print("✅ Login successful")
        
        # Generate a test response
        test_content = "This is a test post about technology and innovation. #tech #ai #future"
        sentiment = sentiment_analyzer.analyze_sentiment(test_content)
        vibe = vibe_analyzer.analyze_vibe(test_content)
        response = response_generator.generate_response(sentiment, vibe, test_content, "testuser.bsky.social")
        
        print(f"📝 Generated response ({len(response)} chars):")
        print(response[:100] + "..." if len(response) > 100 else response)
        
        # Test truncation
        if len(response) > 280:
            response = response[:277] + "..."
            print(f"📝 Truncated to {len(response)} chars")
        
        # Test posting (we'll use a dummy URI/CID for testing)
        print("\n🧪 Testing post_reply method...")
        test_uri = "at://did:plc:test/app.bsky.feed.post/test"
        test_cid = "test_cid_123"
        
        # This should fail gracefully since we're using dummy data
        try:
            await bluesky_client.post_reply(response, test_uri, test_cid)
        except Exception as e:
            print(f"❌ Expected error with dummy data: {e}")
            print("✅ This is expected since we used dummy URI/CID")
            
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_posting()) 