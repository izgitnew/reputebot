#!/usr/bin/env python3
"""
Test script to examine timestamps from posts.
"""

import asyncio
from dotenv import load_dotenv
from bluesky import BlueskyClient

# Load environment variables
load_dotenv()

async def test_timestamps():
    """Test timestamp extraction from posts."""
    print("🔍 Testing Timestamp Extraction...")
    
    bluesky_client = BlueskyClient()
    
    try:
        # Login
        await bluesky_client.login()
        print("✅ Login successful")
        
        # Fetch posts from The Athletic
        posts = await bluesky_client.get_author_posts("theathletic.com", limit=10)
        
        if not posts:
            print("❌ No posts found")
            return
        
        print(f"📊 Found {len(posts)} posts from @theathletic.com")
        
        # Examine timestamps
        for i, post in enumerate(posts):
            print(f"\n--- Post {i+1} ---")
            
            # Try to extract timestamp
            timestamp = None
            if hasattr(post, 'post') and hasattr(post.post, 'record') and hasattr(post.post.record, 'created_at'):
                timestamp = post.post.record.created_at
                print(f"✅ Found timestamp in post.post.record.created_at: {timestamp}")
            elif hasattr(post, 'post') and hasattr(post.post, 'record') and hasattr(post.post.record, 'createdAt'):
                timestamp = post.post.record.createdAt
                print(f"✅ Found timestamp in post.post.record.createdAt: {timestamp}")
            elif hasattr(post, 'record') and hasattr(post.record, 'createdAt'):
                timestamp = post.record.createdAt
                print(f"✅ Found timestamp in post.record.createdAt: {timestamp}")
            elif hasattr(post, 'createdAt'):
                timestamp = post.createdAt
                print(f"✅ Found timestamp in post.createdAt: {timestamp}")
            else:
                print("❌ No timestamp found")
            
            # Show post text
            if hasattr(post, 'post') and hasattr(post.post, 'record') and hasattr(post.post.record, 'text'):
                text = post.post.record.text[:50] + "..." if len(post.post.record.text) > 50 else post.post.record.text
                print(f"📝 Text: {text}")
        
        # Calculate time difference
        if len(posts) >= 2:
            first_post = posts[0]
            last_post = posts[-1]
            
            first_time = None
            last_time = None
            
            # Extract timestamps
            for post in [first_post, last_post]:
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
                
                if first_time is None:
                    first_time = timestamp
                else:
                    last_time = timestamp
            
            if first_time and last_time:
                from datetime import datetime
                try:
                    first_dt = datetime.fromisoformat(first_time.replace('Z', '+00:00'))
                    last_dt = datetime.fromisoformat(last_time.replace('Z', '+00:00'))
                    
                    time_diff = abs((first_dt - last_dt).total_seconds() / 86400)
                    posts_per_day = len(posts) / time_diff if time_diff > 0 else len(posts)
                    
                    print(f"\n📊 Time Analysis:")
                    print(f"First post: {first_time}")
                    print(f"Last post: {last_time}")
                    print(f"Time difference: {time_diff:.2f} days")
                    print(f"Posts per day: {posts_per_day:.1f}")
                    
                except Exception as e:
                    print(f"❌ Error parsing timestamps: {e}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_timestamps()) 