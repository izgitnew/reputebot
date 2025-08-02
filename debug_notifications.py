#!/usr/bin/env python3
"""
Debug script to understand notification structure and behavior.
"""

import asyncio
from dotenv import load_dotenv
from bluesky import BlueskyClient

# Load environment variables
load_dotenv()

async def debug_notifications():
    """Debug notification structure and behavior."""
    print("🔍 Debugging Notifications...")
    
    bluesky_client = BlueskyClient()
    
    try:
        # Login
        await bluesky_client.login()
        print("✅ Login successful")
        
        # Get notifications
        notifications = await bluesky_client.get_notifications(limit=5)
        print(f"📬 Found {len(notifications)} notifications")
        
        for i, notification in enumerate(notifications):
            print(f"\n--- Notification {i+1} ---")
            print(f"Type: {type(notification)}")
            print(f"Reason: {getattr(notification, 'reason', 'N/A')}")
            print(f"URI: {getattr(notification, 'uri', 'N/A')}")
            print(f"CID: {getattr(notification, 'cid', 'N/A')}")
            print(f"IndexedAt: {getattr(notification, 'indexed_at', 'N/A')}")
            print(f"IsRead: {getattr(notification, 'is_read', 'N/A')}")
            
            # Check if it has a post
            if hasattr(notification, 'post'):
                print(f"Post URI: {getattr(notification.post, 'uri', 'N/A')}")
                print(f"Post CID: {getattr(notification.post, 'cid', 'N/A')}")
            
            # Check if it has an author
            if hasattr(notification, 'author'):
                print(f"Author: {getattr(notification.author, 'handle', 'N/A')}")
            
            print(f"All attributes: {[attr for attr in dir(notification) if not attr.startswith('_')]}")
        
        # Try marking as read
        print("\n📝 Attempting to mark notifications as read...")
        await bluesky_client.mark_notification_read("")
        
        # Get notifications again
        print("\n📬 Getting notifications again...")
        notifications2 = await bluesky_client.get_notifications(limit=5)
        print(f"📬 Found {len(notifications2)} notifications after marking as read")
        
        # Compare
        if len(notifications) == len(notifications2):
            print("⚠️ Same number of notifications found")
            for i, (n1, n2) in enumerate(zip(notifications, notifications2)):
                if getattr(n1, 'uri', None) == getattr(n2, 'uri', None):
                    print(f"  Notification {i+1}: Same URI")
                else:
                    print(f"  Notification {i+1}: Different URIs")
        else:
            print("✅ Different number of notifications found")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(debug_notifications()) 