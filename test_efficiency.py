#!/usr/bin/env python3
"""
Test script to compare efficiency of full posts vs timestamps.
"""

import asyncio
import time
from dotenv import load_dotenv
from bluesky import BlueskyClient
from responder import ResponseGenerator

# Load environment variables
load_dotenv()

async def test_efficiency():
    """Test the efficiency difference between full posts and timestamps."""
    print("🔍 Testing Efficiency: Full Posts vs Timestamps...")
    
    bluesky_client = BlueskyClient()
    response_generator = ResponseGenerator()
    
    try:
        # Login
        await bluesky_client.login()
        print("✅ Login successful")
        
        # Test 1: Full posts (current method)
        print("\n📊 Test 1: Full Posts Method")
        start_time = time.time()
        full_posts = await bluesky_client.get_author_posts("theathletic.com", days_back=30)
        full_posts_time = time.time() - start_time
        print(f"⏱️ Time to fetch full posts: {full_posts_time:.2f} seconds")
        print(f"📊 Posts fetched: {len(full_posts)}")
        
        # Calculate posts per day with full posts
        start_time = time.time()
        posts_per_day_full = response_generator._calculate_posts_per_day(full_posts)
        calc_time_full = time.time() - start_time
        print(f"📊 Posts per day (full posts): {posts_per_day_full}")
        print(f"⏱️ Time to calculate: {calc_time_full:.4f} seconds")
        
        # Test 2: Timestamps only (new method)
        print("\n📊 Test 2: Timestamps Only Method")
        start_time = time.time()
        timestamps = await bluesky_client.get_author_post_timestamps("theathletic.com", days_back=30)
        timestamps_time = time.time() - start_time
        print(f"⏱️ Time to fetch timestamps: {timestamps_time:.2f} seconds")
        print(f"📊 Timestamps fetched: {len(timestamps)}")
        
        # Calculate posts per day with timestamps
        start_time = time.time()
        posts_per_day_timestamps = response_generator._calculate_posts_per_day(timestamps)
        calc_time_timestamps = time.time() - start_time
        print(f"📊 Posts per day (timestamps): {posts_per_day_timestamps}")
        print(f"⏱️ Time to calculate: {calc_time_timestamps:.4f} seconds")
        
        # Compare results
        print(f"\n📊 Comparison:")
        print(f"  Full posts fetch time: {full_posts_time:.2f}s")
        print(f"  Timestamps fetch time: {timestamps_time:.2f}s")
        print(f"  Speed improvement: {full_posts_time/timestamps_time:.1f}x faster")
        print(f"  Posts per day (full): {posts_per_day_full}")
        print(f"  Posts per day (timestamps): {posts_per_day_timestamps}")
        print(f"  Results match: {posts_per_day_full == posts_per_day_timestamps}")
        
        # Show some sample timestamps
        print(f"\n📝 Sample timestamps:")
        for i, timestamp in enumerate(timestamps[:5]):
            print(f"  {i+1}. {timestamp}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_efficiency()) 