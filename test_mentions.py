#!/usr/bin/env python3
"""
Test script to check notifications and mentions.
"""

import asyncio
import os
from dotenv import load_dotenv
from atproto import Client

# Load environment variables
load_dotenv()

async def test_notifications():
    """Test what notifications we can see."""
    client = Client()
    username = os.getenv('BLUESKY_HANDLE')
    password = os.getenv('BLUESKY_PASSWORD')
    
    try:
        # Login
        client.login(username, password)
        print(f"✅ Logged in as {username}")
        
        # Get notifications
        response = client.app.bsky.notification.list_notifications({'limit': 50})
        notifications = response.notifications
        
        print(f"📬 Found {len(notifications)} notifications")
        
        for i, notification in enumerate(notifications):
            print(f"\n--- Notification {i+1} ---")
            print(f"Type: {type(notification)}")
            print(f"Attributes: {dir(notification)}")
            
            # Try to get reason
            if hasattr(notification, 'reason'):
                print(f"Reason: {notification.reason}")
            else:
                print("No reason attribute")
            
            # Try to get text
            if hasattr(notification, 'record') and hasattr(notification.record, 'text'):
                print(f"Text: {notification.record.text[:100]}...")
            elif hasattr(notification, 'post') and hasattr(notification.post, 'text'):
                print(f"Text: {notification.post.text[:100]}...")
            else:
                print("No text found")
            
            # Check if it's a mention
            if hasattr(notification, 'reason') and notification.reason == 'mention':
                print("🎯 This is a mention!")
            else:
                print("⏭️ Not a mention")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_notifications()) 