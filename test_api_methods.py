#!/usr/bin/env python3
"""
Test script to explore different API methods for getting posts.
"""

import asyncio
from dotenv import load_dotenv
from bluesky import BlueskyClient

# Load environment variables
load_dotenv()

async def test_api_methods():
    """Test different API methods for getting posts."""
    print("🔍 Testing Different API Methods...")
    
    bluesky_client = BlueskyClient()
    
    try:
        # Login
        await bluesky_client.login()
        print("✅ Login successful")
        
        # Test 1: Current method with higher limit
        print("\n📊 Test 1: get_author_feed with limit=500")
        posts = await bluesky_client.get_author_posts("theathletic.com", limit=500)
        print(f"📊 Found {len(posts)} posts")
        
        if posts:
            # Show oldest post timestamp
            oldest_post = posts[-1]
            if hasattr(oldest_post, 'post') and hasattr(oldest_post.post, 'record') and hasattr(oldest_post.post.record, 'created_at'):
                oldest_time = oldest_post.post.record.created_at
                print(f"📅 Oldest post: {oldest_time}")
        
        # Test 2: Try to see what other methods are available
        print("\n🔍 Available methods on client:")
        methods = [attr for attr in dir(bluesky_client.client) if not attr.startswith('_')]
        print(f"📋 Found {len(methods)} methods")
        
        # Look for feed-related methods
        feed_methods = [m for m in methods if 'feed' in m.lower()]
        print(f"📋 Feed methods: {feed_methods}")
        
        # Look for post-related methods
        post_methods = [m for m in methods if 'post' in m.lower()]
        print(f"📋 Post methods: {post_methods}")
        
        # Test 3: Try to get more posts using cursor pagination
        print("\n📊 Test 3: Pagination test")
        try:
            # Try to get posts with cursor
            response = await bluesky_client.client.app.bsky.feed.get_author_feed({
                'actor': 'theathletic.com',
                'limit': 100
            })
            print(f"📊 First batch: {len(response.feed)} posts")
            print(f"📋 Has cursor: {hasattr(response, 'cursor')}")
            if hasattr(response, 'cursor') and response.cursor:
                print(f"📋 Cursor: {response.cursor}")
                
                # Try to get more posts
                response2 = await bluesky_client.client.app.bsky.feed.get_author_feed({
                    'actor': 'theathletic.com',
                    'limit': 100,
                    'cursor': response.cursor
                })
                print(f"📊 Second batch: {len(response2.feed)} posts")
                print(f"📋 Total posts: {len(response.feed) + len(response2.feed)}")
                
        except Exception as e:
            print(f"❌ Pagination test failed: {e}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_api_methods()) 