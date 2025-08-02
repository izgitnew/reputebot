#!/usr/bin/env python3
"""
Test script to verify pagination-based post fetching.
"""

import asyncio
from dotenv import load_dotenv
from bluesky import BlueskyClient
from responder import ResponseGenerator

# Load environment variables
load_dotenv()

async def test_pagination():
    """Test the new pagination-based post fetching."""
    print("🔍 Testing Pagination-Based Post Fetching...")
    
    bluesky_client = BlueskyClient()
    response_generator = ResponseGenerator()
    
    try:
        # Login
        await bluesky_client.login()
        print("✅ Login successful")
        
        # Fetch posts from The Athletic using pagination
        posts = await bluesky_client.get_author_posts("theathletic.com", days_back=30)
        
        if not posts:
            print("❌ No posts found")
            return
        
        print(f"📊 Found {len(posts)} posts from @theathletic.com")
        
        # Test the calculation
        posts_per_day = response_generator._calculate_posts_per_day(posts)
        print(f"📊 Posts per day (30-day average): {posts_per_day}")
        
        # Show some timestamps for verification
        from datetime import datetime, timedelta, timezone
        now = datetime.now(timezone.utc)
        thirty_days_ago = now - timedelta(days=30)
        
        print(f"\n📅 Current time: {now}")
        print(f"📅 30 days ago: {thirty_days_ago}")
        
        print(f"\n📝 Recent posts:")
        for i, post in enumerate(posts[:5]):
            if hasattr(post, 'post') and hasattr(post.post, 'record') and hasattr(post.post.record, 'created_at'):
                timestamp = post.post.record.created_at
                post_time = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                days_ago = (now - post_time).total_seconds() / 86400
                print(f"  {i+1}. {timestamp} ({days_ago:.1f} days ago)")
        
        print(f"\n📝 Oldest posts:")
        for i, post in enumerate(posts[-5:]):
            if hasattr(post, 'post') and hasattr(post.post, 'record') and hasattr(post.post.record, 'created_at'):
                timestamp = post.post.record.created_at
                post_time = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                days_ago = (now - post_time).total_seconds() / 86400
                print(f"  {len(posts)-4+i}. {timestamp} ({days_ago:.1f} days ago)")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_pagination()) 