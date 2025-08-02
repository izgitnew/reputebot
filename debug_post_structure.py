#!/usr/bin/env python3
"""
Debug script to examine post object structure.
"""

import asyncio
from dotenv import load_dotenv
from bluesky import BlueskyClient

# Load environment variables
load_dotenv()

async def debug_post_structure():
    """Debug the structure of post objects."""
    print("🔍 Debugging Post Structure...")
    
    bluesky_client = BlueskyClient()
    
    try:
        # Login
        await bluesky_client.login()
        print("✅ Login successful")
        
        # Fetch posts from The Athletic
        posts = await bluesky_client.get_author_posts("theathletic.com", limit=3)
        
        if not posts:
            print("❌ No posts found")
            return
        
        print(f"📊 Found {len(posts)} posts from @theathletic.com")
        
        # Examine the first post structure
        post = posts[0]
        print(f"\n🔍 Post type: {type(post)}")
        print(f"🔍 Post attributes: {dir(post)}")
        
        if hasattr(post, 'post'):
            print(f"\n🔍 post.post type: {type(post.post)}")
            print(f"🔍 post.post attributes: {dir(post.post)}")
            
            if hasattr(post.post, 'record'):
                print(f"\n🔍 post.post.record type: {type(post.post.record)}")
                print(f"🔍 post.post.record attributes: {dir(post.post.record)}")
                
                # Check for timestamp fields
                for attr in dir(post.post.record):
                    if 'time' in attr.lower() or 'date' in attr.lower() or 'created' in attr.lower():
                        try:
                            value = getattr(post.post.record, attr)
                            print(f"🔍 {attr}: {value}")
                        except:
                            pass
        
        # Also check the post object directly
        print(f"\n🔍 Direct post attributes:")
        for attr in dir(post):
            if 'time' in attr.lower() or 'date' in attr.lower() or 'created' in attr.lower():
                try:
                    value = getattr(post, attr)
                    print(f"🔍 {attr}: {value}")
                except:
                    pass
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(debug_post_structure()) 