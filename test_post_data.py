#!/usr/bin/env python3
"""
Test script to examine what post data we're fetching.
"""

import asyncio
from dotenv import load_dotenv
from bluesky import BlueskyClient

# Load environment variables
load_dotenv()

async def test_post_data():
    """Test what post data we're actually fetching."""
    print("🔍 Testing Post Data Structure...")
    
    bluesky_client = BlueskyClient()
    
    try:
        # Login
        await bluesky_client.login()
        print("✅ Login successful")
        
        # Fetch just a few posts to examine the structure
        posts = await bluesky_client.get_author_posts("theathletic.com", days_back=1)
        
        if not posts:
            print("❌ No posts found")
            return
        
        print(f"📊 Found {len(posts)} posts")
        
        # Examine the first post structure
        post = posts[0]
        print(f"\n🔍 Post type: {type(post)}")
        print(f"🔍 Post size (rough estimate): {len(str(post))} characters")
        
        # Show what fields we're getting
        if hasattr(post, 'post') and hasattr(post.post, 'record'):
            record = post.post.record
            print(f"\n📝 Post record fields:")
            for field in dir(record):
                if not field.startswith('_'):
                    try:
                        value = getattr(record, field)
                        if field == 'text':
                            preview = str(value)[:50] + "..." if len(str(value)) > 50 else str(value)
                            print(f"  {field}: {preview}")
                        else:
                            print(f"  {field}: {value}")
                    except:
                        print(f"  {field}: <error>")
        
        # Check if there are other API methods that might be more efficient
        print(f"\n🔍 Looking for more efficient API methods...")
        
        # Try to see if there's a way to get just metadata
        try:
            # Check if there's a different endpoint for just post metadata
            print("📋 Available app.bsky methods:")
            app_methods = [attr for attr in dir(bluesky_client.client.app.bsky) if not attr.startswith('_')]
            for method in app_methods:
                print(f"  - {method}")
        except Exception as e:
            print(f"❌ Error checking methods: {e}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_post_data()) 