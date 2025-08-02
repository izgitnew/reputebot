#!/usr/bin/env python3
"""
Test script to demonstrate handling of multiple simultaneous notifications.
"""

import asyncio
from datetime import datetime, timezone
from dotenv import load_dotenv
from bluesky import BlueskyClient

# Load environment variables
load_dotenv()

async def test_simultaneous_notifications():
    """Test how the bot handles multiple notifications at the same time."""
    print("🧪 Testing Simultaneous Notifications...")
    
    bluesky_client = BlueskyClient()
    
    try:
        # Login
        await bluesky_client.login()
        print("✅ Login successful")
        
        # Simulate multiple notifications with the same timestamp
        current_time = datetime.now(timezone.utc).isoformat()
        
        print(f"\n📅 Current timestamp: {current_time}")
        print(f"📅 Last processed timestamp: {bluesky_client.last_processed_timestamp}")
        
        # Simulate processing multiple notifications
        test_notifications = [
            {"uri": "test1", "indexed_at": current_time},
            {"uri": "test2", "indexed_at": current_time},
            {"uri": "test3", "indexed_at": current_time},
        ]
        
        print(f"\n🔍 Processing {len(test_notifications)} notifications with same timestamp...")
        
        for i, notification in enumerate(test_notifications):
            notification_uri = notification["uri"]
            notification_time = notification["indexed_at"]
            
            print(f"\n--- Processing Notification {i+1} ---")
            print(f"URI: {notification_uri}")
            print(f"Timestamp: {notification_time}")
            
            # Check if already processed
            if notification_uri in bluesky_client.processed_notifications:
                print("⏭️ Already processed (by URI)")
                continue
            
            # Check if timestamp is too old
            if bluesky_client.last_processed_timestamp and notification_time < bluesky_client.last_processed_timestamp:
                print("⏭️ Too old (by timestamp)")
                continue
            
            # Process the notification
            print("✅ Processing notification...")
            bluesky_client.processed_notifications.add(notification_uri)
            
            # Update timestamp
            if not bluesky_client.last_processed_timestamp or notification_time >= bluesky_client.last_processed_timestamp:
                bluesky_client.last_processed_timestamp = notification_time
                print(f"📅 Updated timestamp to: {notification_time}")
        
        print(f"\n📊 Final state:")
        print(f"Processed notifications: {len(bluesky_client.processed_notifications)}")
        print(f"Last timestamp: {bluesky_client.last_processed_timestamp}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_simultaneous_notifications()) 