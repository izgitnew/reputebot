#!/usr/bin/env python3
"""
Test script to verify 24-hour post counting.
"""

import asyncio
from dotenv import load_dotenv
from bluesky import BlueskyClient
from responder import ResponseGenerator

# Load environment variables
load_dotenv()

async def test_24h_count():
    """Test the new 24-hour post counting logic."""
    print("🔍 Testing 24-Hour Post Counting...")
    
    bluesky_client = BlueskyClient()
    response_generator = ResponseGenerator()
    
    try:
        # Login
        await bluesky_client.login()
        print("✅ Login successful")
        
        # Fetch posts from The Athletic
        posts = await bluesky_client.get_author_posts("theathletic.com", limit=20)
        
        if not posts:
            print("❌ No posts found")
            return
        
        print(f"📊 Found {len(posts)} posts from @theathletic.com")
        
        # Test the new calculation
        posts_per_day = response_generator._calculate_posts_per_day(posts)
        print(f"📊 Posts per day (24h count): {posts_per_day}")
        
        # Show some timestamps for verification
        from datetime import datetime, timedelta, timezone
        now = datetime.now(timezone.utc)
        twenty_four_hours_ago = now - timedelta(hours=24)
        
        print(f"\n📅 Current time: {now}")
        print(f"📅 24 hours ago: {twenty_four_hours_ago}")
        
        print(f"\n📝 Recent posts:")
        for i, post in enumerate(posts[:5]):
            if hasattr(post, 'post') and hasattr(post.post, 'record') and hasattr(post.post.record, 'created_at'):
                timestamp = post.post.record.created_at
                post_time = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                hours_ago = (now - post_time).total_seconds() / 3600
                print(f"  {i+1}. {timestamp} ({hours_ago:.1f} hours ago)")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_24h_count()) 