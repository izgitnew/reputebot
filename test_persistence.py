#!/usr/bin/env python3
"""
Test script to verify persistence between bot runs.
"""

import asyncio
from dotenv import load_dotenv
from bluesky import BlueskyClient

# Load environment variables
load_dotenv()

async def test_persistence():
    """Test that the bot loads saved state correctly."""
    print("🧪 Testing Persistence...")
    
    bluesky_client = BlueskyClient()
    
    try:
        # Check what was loaded
        print(f"📅 Last processed timestamp: {bluesky_client.last_processed_timestamp}")
        print(f"📋 Processed notifications count: {len(bluesky_client.processed_notifications)}")
        
        if bluesky_client.processed_notifications:
            print("📋 Processed notifications:")
            for uri in list(bluesky_client.processed_notifications)[:3]:  # Show first 3
                print(f"  - {uri[:50]}...")
        
        # Test filtering logic
        print("\n🔍 Testing filtering logic...")
        
        # Simulate the notifications we know exist
        test_notifications = [
            {"uri": "at://did:plc:pawi7pfhupvfbpc3y5ynjgmk/app.bsky.feed.post/3lvfioihug42o", "indexed_at": "2025-08-02T06:05:22.032Z"},
            {"uri": "at://did:plc:pawi7pfhupvfbpc3y5ynjgmk/app.bsky.feed.post/3lvfhydfmjm2o", "indexed_at": "2025-08-02T05:52:58.519Z"},
        ]
        
        for notification in test_notifications:
            notification_uri = notification["uri"]
            notification_time = notification["indexed_at"]
            
            print(f"\n--- Testing Notification ---")
            print(f"URI: {notification_uri[:50]}...")
            print(f"Timestamp: {notification_time}")
            
            # Check if already processed
            if notification_uri in bluesky_client.processed_notifications:
                print("⏭️ Would skip (already processed)")
            elif bluesky_client.last_processed_timestamp and notification_time < bluesky_client.last_processed_timestamp:
                print("⏭️ Would skip (too old)")
            else:
                print("✅ Would process (new)")
        
        print("\n✅ Persistence test completed!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_persistence()) 