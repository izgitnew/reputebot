#!/usr/bin/env python3
"""
Bluesky bot client for interacting with AT Protocol, monitoring feeds, analyzing sentiment, and replying to posts.
"""

import os
import asyncio
import json
from atproto import Client
from typing import List, Dict, Any
from queue_manager import queue_manager, RequestType

class BlueskyClient:
    """Bluesky bot for monitoring feeds, analyzing sentiment, and posting replies."""

    def __init__(self):
        self.client = Client()
        # Don't load environment variables during initialization
        # They will be loaded when login() is called
        self.username = None
        self.password = None
        
        self.feeds = self.load_feeds()
        
        # Initialize analyzers (will be set by main.py)
        self.sentiment_analyzer = None
        self.vibe_analyzer = None
        self.response_generator = None
        
        # Track processed notifications to prevent duplicates
        self.processed_notifications = set()
        # Track the latest notification timestamp we've processed
        self.last_processed_timestamp = None
        # Track when the bot started - only process mentions after this time
        self.bot_start_time = None
        # Don't load files during initialization - will be loaded when monitoring starts
    
    def _load_last_timestamp(self):
        """Load the last processed timestamp from file."""
        try:
            with open('last_processed_timestamp.txt', 'r') as f:
                timestamp_str = f.read().strip()
                # Clean the timestamp string (remove any extra characters)
                timestamp_str = timestamp_str.split('%')[0].strip()
                if timestamp_str:
                    self.last_processed_timestamp = timestamp_str
                    print(f"📅 Loaded last processed timestamp: {timestamp_str}")
                else:
                    print("📅 Empty timestamp file, starting fresh")
                    self.last_processed_timestamp = None
        except FileNotFoundError:
            print("📅 No previous timestamp found, starting fresh")
            self.last_processed_timestamp = None
        except Exception as e:
            print(f"⚠️ Error loading timestamp: {e}")
            self.last_processed_timestamp = None
    
    def _save_last_timestamp(self):
        """Save the last processed timestamp to file."""
        if self.last_processed_timestamp:
            try:
                with open('last_processed_timestamp.txt', 'w') as f:
                    f.write(self.last_processed_timestamp)
                print(f"📅 Saved last processed timestamp: {self.last_processed_timestamp}")
            except Exception as e:
                print(f"⚠️ Error saving timestamp: {e}")
    
    def _load_processed_notifications(self):
        """Load processed notification URIs from file."""
        try:
            with open('processed_notifications.txt', 'r') as f:
                for line in f:
                    uri = line.strip()
                    if uri:
                        self.processed_notifications.add(uri)
                print(f"📋 Loaded {len(self.processed_notifications)} processed notifications")
        except FileNotFoundError:
            print("📋 No processed notifications file found")
        except Exception as e:
            print(f"⚠️ Error loading processed notifications: {e}")
    
    def _save_processed_notifications(self):
        """Save processed notification URIs to file."""
        try:
            with open('processed_notifications.txt', 'w') as f:
                for uri in self.processed_notifications:
                    f.write(f"{uri}\n")
            print(f"📋 Saved {len(self.processed_notifications)} processed notifications")
        except Exception as e:
            print(f"⚠️ Error saving processed notifications: {e}")
    
    def _initialize_persistence(self):
        """Initialize persistence data (called when monitoring starts)."""
        # Load the last processed timestamp from file to persist between runs
        self._load_last_timestamp()
        # Load processed notifications from file
        self._load_processed_notifications()
    
    def _reset_persistence(self):
        """Reset persistence data to start fresh."""
        self.last_processed_timestamp = None
        self.processed_notifications.clear()
        
        # Delete persistence files
        import os
        try:
            if os.path.exists('last_processed_timestamp.txt'):
                os.remove('last_processed_timestamp.txt')
                print("🗑️ Deleted last_processed_timestamp.txt")
        except Exception as e:
            print(f"⚠️ Error deleting timestamp file: {e}")
        
        try:
            if os.path.exists('processed_notifications.txt'):
                os.remove('processed_notifications.txt')
                print("🗑️ Deleted processed_notifications.txt")
        except Exception as e:
            print(f"⚠️ Error deleting notifications file: {e}")
        
        print("🔄 Persistence data reset - will process all mentions from now on")
    
    def load_feeds(self) -> List[Dict[str, Any]]:
        """Load feeds configuration from feeds.json."""
        try:
            with open('feeds.json', 'r') as f:
                feeds_data = json.load(f)
                
                # Handle the current format which is a dict of feed objects
                if isinstance(feeds_data, dict):
                    # Convert to list format with default URIs
                    feeds = []
                    for name, feed_info in feeds_data.items():
                        feeds.append({
                            "name": name,
                            "uri": "at://did:plc:z72i7hdynmk6r22z27h6tvur/app.bsky.feed.generator/whats-hot",  # Default URI
                            "description": feed_info.get("description", ""),
                            "keywords": feed_info.get("keywords", []),
                            "enabled": True
                        })
                    return feeds
                else:
                    # Handle list format
                    return [feed for feed in feeds_data if feed.get('enabled', True)]
                    
        except FileNotFoundError:
            print("Warning: feeds.json not found. Using default feeds.")
            return [
                {"name": "What's Hot", "uri": "at://did:plc:z72i7hdynmk6r22z27h6tvur/app.bsky.feed.generator/whats-hot", "enabled": True},
                {"name": "Following", "uri": "at://did:plc:z72i7hdynmk6r22z27h6tvur/app.bsky.feed.generator/following", "enabled": True}
            ]

    async def login(self):
        """Log in to the Bluesky account using app password."""
        # Load environment variables when login is called
        if not self.username or not self.password:
            self.username = os.getenv('BLUESKY_HANDLE')
            self.password = os.getenv('BLUESKY_PASSWORD')
            
            # Debug: Check if environment variables are loaded
            print(f"🔍 Debug - Environment variables:")
            print(f"   BLUESKY_HANDLE: '{self.username}' (length: {len(self.username) if self.username else 0})")
            print(f"   BLUESKY_PASSWORD: {'*' * len(self.password) if self.password else 'Not set'} (length: {len(self.password) if self.password else 0})")
            print(f"   All env vars starting with BLUESKY: {[k for k in os.environ.keys() if k.startswith('BLUESKY')]}")
            
            if not self.username or not self.password:
                print("⚠️ Environment variables not found:")
                print(f"   BLUESKY_HANDLE: {'Set' if self.username else 'Not set'}")
                print(f"   BLUESKY_PASSWORD: {'Set' if self.password else 'Not set'}")
                print("   Make sure these are set in Railway environment variables")
                raise ValueError("BLUESKY_HANDLE and BLUESKY_PASSWORD must be set as environment variables (either in .env file or system environment)")
        
        try:
            print(f"🔐 Attempting login with username: {self.username}")
            self.client.login(self.username, self.password)
            print(f"✅ Logged in as {self.username}")
        except Exception as e:
            print(f"❌ Login failed: {e}")
            print(f"❌ Error type: {type(e)}")
            print(f"❌ Error details: {str(e)}")
            raise

    async def get_notifications(self, limit: int = 20) -> List[Dict[str, Any]]:
        """Fetch recent notifications including mentions."""
        try:
            response = await queue_manager.add_request(
                RequestType.GET_NOTIFICATIONS,
                self.client.app.bsky.notification.list_notifications,
                {'limit': limit}
            )
            return response.notifications
        except Exception as e:
            print(f"❌ Error fetching notifications: {e}")
            return []
    
    async def get_author_posts(self, handle: str, limit: int = 10, days_back: int = 30) -> List[Any]:
        """Fetch recent posts from a specific author, using pagination to get posts from the last N days."""
        try:
            print(f"🔍 Fetching posts from @{handle} (last {days_back} days)...")
            
            from datetime import datetime, timedelta, timezone
            cutoff_time = datetime.now(timezone.utc) - timedelta(days=days_back)
            
            all_posts = []
            cursor = None
            total_fetched = 0
            
            while True:
                # Prepare request parameters - use smaller batch to avoid video embeds
                params = {'actor': handle, 'limit': 20}  # Smaller batch to avoid video embeds
                if cursor:
                    params['cursor'] = cursor
                
                # Use raw HTTP request to bypass video embed validation
                try:
                    import aiohttp
                    import json
                    
                    # Create a new session since the client doesn't expose it
                    session = aiohttp.ClientSession()
                    base_url = "https://bsky.social/xrpc/app.bsky.feed.getAuthorFeed"
                    
                    # Prepare headers
                    headers = {
                        'Authorization': f'Bearer {self.client.session.access_jwt}',
                        'Content-Type': 'application/json'
                    }
                    
                    # Make raw request
                    async with aiohttp.ClientSession() as session:
                        async with session.post(base_url, headers=headers, json=params) as resp:
                            if resp.status == 200:
                                raw_data = await resp.json()
                                
                                # Manually filter out posts with video embeds
                                filtered_feed = []
                                for item in raw_data.get('feed', []):
                                    post = item.get('post', {})
                                    embed = post.get('embed')
                                    
                                    # Skip posts with video embeds
                                    if embed and embed.get('$type') == 'app.bsky.embed.video#view':
                                        continue
                                    
                                    # Create a simple post object with just the text and timestamp
                                    if 'record' in post and 'text' in post['record']:
                                        filtered_feed.append({
                                            'post': {
                                                'record': {
                                                    'text': post['record']['text'],
                                                    'created_at': post['record']['created_at']
                                                }
                                            }
                                        })
                                
                                # Convert to a simple response object
                                response = type('Response', (), {
                                    'feed': filtered_feed,
                                    'cursor': raw_data.get('cursor')
                                })()
                            else:
                                print(f"❌ HTTP error {resp.status} for @{handle}")
                                break
                            
                except ImportError:
                    print(f"⚠️ aiohttp not available, falling back to atproto method for @{handle}")
                    # Fallback to original method
                    response = await queue_manager.add_request(
                        RequestType.GET_AUTHOR_POSTS,
                        self.client.app.bsky.feed.get_author_feed,
                        params
                    )
                    
                    # Handle case where response is None due to video embed issues
                    if response is None:
                        print(f"⚠️ Skipping batch due to video embed validation errors for @{handle}")
                        break
                        
                except Exception as e:
                    print(f"❌ Error fetching posts for @{handle}: {e}")
                    break
                
                batch_posts = response.feed
                total_fetched += len(batch_posts)
                
                # Check if any posts in this batch are older than our cutoff
                old_posts_found = False
                for post in batch_posts:
                    if hasattr(post, 'post') and hasattr(post.post, 'record') and hasattr(post.post.record, 'created_at'):
                        post_time = datetime.fromisoformat(post.post.record.created_at.replace('Z', '+00:00'))
                        if post_time >= cutoff_time:
                            all_posts.append(post)
                        else:
                            old_posts_found = True
                            break
                    else:
                        # If we can't get timestamp, include the post
                        all_posts.append(post)
                
                # If we found old posts, we've reached our time limit
                if old_posts_found:
                    break
                
                # Check if we have more posts to fetch
                if hasattr(response, 'cursor') and response.cursor:
                    cursor = response.cursor
                else:
                    break
                
                # Safety check to prevent infinite loops
                if total_fetched > 1000:  # Max 1000 posts
                    print(f"⚠️ Reached safety limit of 1000 posts for @{handle}")
                    break
            
            print(f"📊 Found {len(all_posts)} posts from @{handle} in the last {days_back} days")
            return all_posts
            
        except Exception as e:
            print(f"❌ Error fetching posts from @{handle}: {e}")
            return []

    async def get_author_post_timestamps(self, handle: str, days_back: int = 30) -> List[str]:
        """Fetch only timestamps from recent posts, much more efficient for counting."""
        try:
            print(f"🔍 Fetching timestamps from @{handle} (last {days_back} days)...")
            
            from datetime import datetime, timedelta, timezone
            cutoff_time = datetime.now(timezone.utc) - timedelta(days=days_back)
            
            timestamps = []
            cursor = None
            total_fetched = 0
            
            while True:
                # Prepare request parameters - use smaller batch to avoid video embeds
                params = {'actor': handle, 'limit': 20}  # Smaller batch to avoid video embeds
                if cursor:
                    params['cursor'] = cursor
                
                # Use raw HTTP request to bypass video embed validation
                try:
                    import aiohttp
                    import json
                    
                    # Create a new session since the client doesn't expose it
                    session = aiohttp.ClientSession()
                    base_url = "https://bsky.social/xrpc/app.bsky.feed.getAuthorFeed"
                    
                    # Prepare headers
                    headers = {
                        'Authorization': f'Bearer {self.client.session.access_jwt}',
                        'Content-Type': 'application/json'
                    }
                    
                    # Make raw request
                    async with aiohttp.ClientSession() as session:
                        async with session.post(base_url, headers=headers, json=params) as resp:
                            if resp.status == 200:
                                raw_data = await resp.json()
                                
                                # Manually filter out posts with video embeds and extract timestamps
                                for item in raw_data.get('feed', []):
                                    post = item.get('post', {})
                                    embed = post.get('embed')
                                    
                                    # Skip posts with video embeds
                                    if embed and embed.get('$type') == 'app.bsky.embed.video#view':
                                        continue
                                    
                                    # Extract timestamp
                                    if 'record' in post and 'created_at' in post['record']:
                                        timestamp = post['record']['created_at']
                                        post_time = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                                        if post_time >= cutoff_time:
                                            timestamps.append(timestamp)
                                        else:
                                            # Found old post, stop processing
                                            break
                                
                                # Get cursor for next batch
                                cursor = raw_data.get('cursor')
                            else:
                                print(f"❌ HTTP error {resp.status} for @{handle}")
                                break
                            
                except ImportError:
                    print(f"⚠️ aiohttp not available, falling back to atproto method for @{handle}")
                    # Fallback to original method
                    response = await queue_manager.add_request(
                        RequestType.GET_AUTHOR_POSTS,
                        self.client.app.bsky.feed.get_author_feed,
                        params
                    )
                    
                    # Handle case where response is None due to video embed issues
                    if response is None:
                        print(f"⚠️ Skipping batch due to video embed validation errors for @{handle}")
                        break
                    
                    # Extract timestamps from response
                    batch_posts = response.feed
                    for post in batch_posts:
                        if hasattr(post, 'post') and hasattr(post.post, 'record') and hasattr(post.post.record, 'created_at'):
                            timestamp = post.post.record.created_at
                            post_time = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                            if post_time >= cutoff_time:
                                timestamps.append(timestamp)
                            else:
                                # Found old post, stop processing
                                break
                    
                    # Get cursor for next batch
                    cursor = response.cursor if hasattr(response, 'cursor') else None
                        
                except Exception as e:
                    print(f"❌ Error fetching timestamps for @{handle}: {e}")
                    break
                
                # Check if we have more posts to fetch
                if cursor:
                    continue
                else:
                    break
                
                # Safety check to prevent infinite loops
                if total_fetched > 1000:  # Max 1000 posts
                    print(f"⚠️ Reached safety limit of 1000 posts for @{handle}")
                    break
            
            print(f"📊 Found {len(timestamps)} timestamps from @{handle} in the last {days_back} days")
            return timestamps
            
        except Exception as e:
            print(f"❌ Error fetching timestamps from @{handle}: {e}")
            return []
    
    async def get_post_thread(self, uri: str) -> Dict[str, Any]:
        """Get a post and its thread context."""
        try:
            response = await queue_manager.add_request(
                RequestType.GET_POST_THREAD,
                self.client.app.bsky.feed.get_post_thread,
                {'uri': uri}
            )
            
            # Handle case where response is None due to video embed issues
            if response is None:
                print(f"⚠️ Skipping post thread due to video embed validation errors: {uri}")
                return {}
            
            return response.thread
        except Exception as e:
            print(f"❌ Error fetching post thread: {e}")
            return {}
    
    async def mark_notification_read(self, notification_uri: str):
        """Mark a notification as read."""
        try:
            # Try the simpler approach - just update the seen timestamp
            # This should mark all notifications as seen up to the current time
            await queue_manager.add_request(
                RequestType.MARK_NOTIFICATION_READ,
                self.client.app.bsky.notification.update_seen,
                {'seenAt': self.client.get_current_time_iso()}
            )
            print(f"✅ Marked notifications as read up to: {self.client.get_current_time_iso()}")
        except Exception as e:
            print(f"❌ Failed to mark notifications as read: {e}")
    
    async def _get_target_account_for_analysis(self, notification) -> str:
        """Determine which account to analyze based on the mention context."""
        try:
            # Get the post URI from the notification
            post_uri = None
            if hasattr(notification, 'uri'):
                post_uri = notification.uri
            elif hasattr(notification, 'post') and hasattr(notification.post, 'uri'):
                post_uri = notification.post.uri
            
            if not post_uri:
                print("⚠️ No post URI found in notification")
                return None
            
            print(f"🔍 Analyzing post: {post_uri}")
            
            # Get the post thread to see if this is a reply
            thread = await self.get_post_thread(post_uri)
            
            if not thread:
                print("⚠️ Could not fetch post thread")
                return None
            
            # Check if this post is a reply to another post
            if hasattr(thread, 'post') and hasattr(thread.post, 'record') and hasattr(thread.post.record, 'reply'):
                # This is a reply, get the parent post's author
                parent_uri = thread.post.record.reply.parent.uri
                print(f"🔍 Detected reply, parent URI: {parent_uri}")
                
                # Try to get parent thread, but don't fail if it has video embeds
                try:
                    parent_thread = await self.get_post_thread(parent_uri)
                    
                    if parent_thread and hasattr(parent_thread, 'post') and hasattr(parent_thread.post, 'author'):
                        target_handle = parent_thread.post.author.handle
                        print(f"🎯 Analyzing original post author: @{target_handle}")
                        return target_handle
                    else:
                        print("⚠️ Could not get parent post author from thread")
                except Exception as e:
                    print(f"⚠️ Error getting parent thread: {e}")
                
                # Fallback: try to extract handle from the parent URI
                try:
                    # Parent URI format: at://did:plc:xxx/app.bsky.feed.post/xxx
                    # We need to get the DID and then resolve it to a handle
                    if 'at://' in parent_uri and '/app.bsky.feed.post/' in parent_uri:
                        did = parent_uri.split('at://')[1].split('/app.bsky.feed.post/')[0]
                        print(f"🔍 Extracting DID from parent URI: {did}")
                        
                        # Try to resolve DID to handle
                        try:
                            profile = await queue_manager.add_request(
                                RequestType.GET_PROFILE,
                                self.client.app.bsky.actor.get_profile,
                                {'actor': did}
                            )
                            if profile and hasattr(profile, 'handle'):
                                target_handle = profile.handle
                                print(f"🎯 Resolved parent DID to handle: @{target_handle}")
                                return target_handle
                        except Exception as e:
                            print(f"⚠️ Could not resolve DID to handle: {e}")
                except Exception as e:
                    print(f"⚠️ Error extracting DID from parent URI: {e}")
                
                print("⚠️ Could not determine parent post author, falling back to mention author")
            else:
                print("ℹ️ Not a reply, analyzing mention author")
            
            # If not a reply, analyze the author of the mention
            if hasattr(notification, 'author') and hasattr(notification.author, 'handle'):
                return notification.author.handle
            elif hasattr(notification, 'post') and hasattr(notification.post, 'author') and hasattr(notification.post.author, 'handle'):
                return notification.post.author.handle
            
            return None
            
        except Exception as e:
            print(f"❌ Error determining target account: {e}")
            return None
    
    async def get_feed_posts(self, feed_uri: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Fetch recent posts from a feed."""
        try:
            response = self.client.app.bsky.feed.get_feed({'feed': feed_uri, 'limit': limit})
            return response.feed
        except Exception as e:
            print(f"❌ Error fetching posts from feed {feed_uri}: {e}")
            return []

    async def post_reply(self, text: str, parent_uri: str, parent_cid: str):
        """Post a reply to a specific Bluesky post."""
        try:
            # Check if the post still exists before replying
            try:
                thread = await self.get_post_thread(parent_uri)
                if not thread or not hasattr(thread, 'post'):
                    print(f"⚠️ Post {parent_uri} no longer exists, skipping reply")
                    return
            except Exception as e:
                print(f"⚠️ Could not verify post existence: {e}")
                # Continue anyway, the API will handle the error
            
            await queue_manager.add_request(
                RequestType.POST_REPLY,
                self.client.com.atproto.repo.create_record,
                {
                    "repo": self.client.me.did,
                    "collection": "app.bsky.feed.post",
                    "record": {
                        "$type": "app.bsky.feed.post",
                        "text": text,
                        "reply": {
                            "root": {
                                "cid": parent_cid,
                                "uri": parent_uri
                            },
                            "parent": {
                                "cid": parent_cid,
                                "uri": parent_uri
                            }
                        },
                        "createdAt": self.client.get_current_time_iso()
                    }
                },
                priority=2  # High priority for posting replies
            )
            print(f"✅ Reply posted: {text[:60]}...")
        except Exception as e:
            print(f"❌ Failed to post reply: {e}")

    async def process_mention(self, notification):
        """Process a mention notification and respond."""
        if not all([self.sentiment_analyzer, self.vibe_analyzer, self.response_generator]):
            print("⚠️ Analyzers not initialized, skipping mention processing")
            return
            
        try:
            # Create a unique identifier for this notification to prevent duplicates
            notification_id = None
            if hasattr(notification, 'uri'):
                notification_id = notification.uri
            elif hasattr(notification, 'cid'):
                notification_id = notification.cid
            elif hasattr(notification, 'indexedAt'):
                notification_id = f"{notification.indexedAt}"
            
            # Check if we've already processed this notification
            if notification_id and notification_id in self.processed_notifications:
                print(f"⏭️ Already processed notification {notification_id}, skipping")
                return
            
            # Get author handle from notification
            author_handle = "user"  # Default
            if hasattr(notification, 'author') and hasattr(notification.author, 'handle'):
                author_handle = notification.author.handle
            elif hasattr(notification, 'post') and hasattr(notification.post, 'author') and hasattr(notification.post.author, 'handle'):
                author_handle = notification.post.author.handle
            
            print(f"👀 Processing mention from @{author_handle}...")
            print(f"🔍 Determining which account to analyze...")
            
            # Determine which account to analyze
            target_handle = await self._get_target_account_for_analysis(notification)
            
            if not target_handle:
                print(f"⚠️ Could not determine target account, analyzing @{author_handle}")
                target_handle = author_handle
            
            print(f"🎯 Analyzing account: @{target_handle}")
            print(f"📋 Target account for reputation analysis: @{target_handle}")
            
            # Fetch recent posts from the target account
            target_posts = await self.get_author_posts(target_handle, days_back=30)
            
            if not target_posts:
                print(f"⚠️ Could not fetch posts from @{target_handle}")
                return
            
            # Analyze the target account's recent posts
            all_post_texts = []
            print(f"🔍 Processing {len(target_posts)} posts from @{target_handle}...")
            for i, post in enumerate(target_posts):
                if hasattr(post, 'post') and hasattr(post.post, 'record') and hasattr(post.post.record, 'text'):
                    all_post_texts.append(post.post.record.text)
                elif hasattr(post, 'record') and hasattr(post.record, 'text'):
                    all_post_texts.append(post.record.text)
                elif hasattr(post, 'post') and hasattr(post.post, 'text'):
                    all_post_texts.append(post.post.text)
                # Removed noisy logging for individual post text extraction
            
            if not all_post_texts:
                print(f"⚠️ No text found in posts from @{target_handle}")
                return
            
            # Combine all posts for analysis
            combined_text = " ".join(all_post_texts)
            print(f"📊 Analyzing {len(all_post_texts)} posts from @{target_handle}...")
            
            # Analyze sentiment and vibe of the target account's content
            sentiment_result = self.sentiment_analyzer.analyze_sentiment(combined_text)
            vibe_result = self.vibe_analyzer.analyze_vibe(combined_text)
            
            # For posts/day calculation, use the more efficient timestamp method
            target_timestamps = await self.get_author_post_timestamps(target_handle, days_back=30)
            
            # Generate response based on target account's content
            response = self.response_generator.generate_response(sentiment_result, vibe_result, combined_text, target_handle, target_timestamps)
            
            if response:
                # Get post details for reply
                if hasattr(notification, 'uri'):
                    post_uri = notification.uri
                elif hasattr(notification, 'post') and hasattr(notification.post, 'uri'):
                    post_uri = notification.post.uri
                else:
                    post_uri = ''
                    
                if hasattr(notification, 'cid'):
                    post_cid = notification.cid
                elif hasattr(notification, 'post') and hasattr(notification.post, 'cid'):
                    post_cid = notification.post.cid
                else:
                    post_cid = ''
                
                # Debug: print what we extracted
                print(f"🔍 Extracted URI: {post_uri}")
                print(f"🔍 Extracted CID: {post_cid}")
                print(f"🔍 URI type: {type(post_uri)}")
                print(f"🔍 CID type: {type(post_cid)}")
                
                if post_uri and post_cid:
                    # Ensure CID is a string
                    if not isinstance(post_cid, str):
                        print(f"⚠️ CID is not a string: {post_cid}")
                        post_cid = str(post_cid)
                    
                    await self.post_reply(response, post_uri, post_cid)
                    print(f"✅ Replied to mention: {response[:50]}...")
                    
                    # Mark this notification as processed
                    if notification_id:
                        self.processed_notifications.add(notification_id)
                        print(f"✅ Marked notification {notification_id} as processed")
                        # Save processed notifications immediately
                        self._save_processed_notifications()
                    
                    # Update the latest processed timestamp
                    notification_time = getattr(notification, 'indexed_at', None)
                    if notification_time:
                        # Always update to the latest timestamp (even if same, to handle multiple notifications)
                        if not self.last_processed_timestamp or notification_time >= self.last_processed_timestamp:
                            self.last_processed_timestamp = notification_time
                            print(f"📅 Updated latest processed timestamp: {notification_time}")
                            # Save the timestamp immediately
                            self._save_last_timestamp()
                else:
                    print("⚠️ Missing post URI or CID, cannot reply")
            else:
                print("ℹ️ No response generated for this mention")
                
        except Exception as e:
            print(f"❌ Error processing mention: {e}")
            print(f"Notification structure: {type(notification)}")
            print(f"Notification attributes: {dir(notification)}")
    
    async def process_post(self, post):
        """Analyze a single post and respond if appropriate."""
        if not all([self.sentiment_analyzer, self.vibe_analyzer, self.response_generator]):
            print("⚠️ Analyzers not initialized, skipping post processing")
            return
            
        try:
            # Extract post text from FeedViewPost object
            post_text = post.post.text if hasattr(post, 'post') and hasattr(post.post, 'text') else ''
            if not post_text:
                return
                
            print(f"👀 Processing post: {post_text[:60]}...")
            
            # Analyze sentiment and vibe
            sentiment_result = self.sentiment_analyzer.analyze_sentiment(post_text)
            vibe_result = self.vibe_analyzer.analyze_vibe(post_text)
            
            # Generate response
            response = self.response_generator.generate_response(sentiment_result, vibe_result)
            
            if response:
                # Get post details for reply
                post_uri = post.post.uri if hasattr(post, 'post') and hasattr(post.post, 'uri') else ''
                post_cid = post.post.cid if hasattr(post, 'post') and hasattr(post.post, 'cid') else ''
                
                if post_uri and post_cid:
                    await self.post_reply(response, post_uri, post_cid)
                else:
                    print("⚠️ Missing post URI or CID, cannot reply")
            else:
                print("ℹ️ No response generated for this post")
                
        except Exception as e:
            print(f"❌ Error processing post: {e}")

    async def start_monitoring(self):
        """Start monitoring mentions for the bot."""
        await self.login()
        
        # Initialize persistence data after login
        self._initialize_persistence()
        
        # Check if we should reset persistence (for debugging)
        import os
        if os.getenv('RESET_PERSISTENCE', 'false').lower() == 'true':
            print("🔄 Reset flag detected, clearing persistence data...")
            self._reset_persistence()
        
        # Also check for a simple reset file
        if os.path.exists('reset_bot.txt'):
            print("🔄 Reset file detected, clearing persistence data...")
            self._reset_persistence()
            try:
                os.remove('reset_bot.txt')
                print("🗑️ Removed reset file")
            except Exception as e:
                print(f"⚠️ Error removing reset file: {e}")
        
        # Force reset if environment variable is set
        if os.getenv('FORCE_RESET', 'false').lower() == 'true':
            print("🔄 FORCE_RESET detected, clearing all persistence data...")
            self._reset_persistence()
            # Clear the processed notifications set in memory
            self.processed_notifications.clear()
            self.last_processed_timestamp = None
            print("🔄 Memory cleared - starting completely fresh")
        
        # Set the bot start time - only process mentions that arrive after this
        from datetime import datetime, timezone, timedelta
        self.bot_start_time = datetime.now(timezone.utc) - timedelta(seconds=30)  # 30 second buffer
        print(f"🕐 Bot started at: {self.bot_start_time.isoformat()}")
        
        print("📡 Starting mention monitoring...")
        print(f"🤖 Bot handle: @{self.username}")
        print("💬 Will respond to posts that mention the bot")
        
        # Set up graceful shutdown
        import signal
        def signal_handler(signum, frame):
            print("\n🛑 Shutting down gracefully...")
            self._save_last_timestamp()
            self._save_processed_notifications()
            exit(0)
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        
        while True:
            try:
                # Get notifications (mentions)
                notifications = await self.get_notifications()
                
                print(f"📬 Found {len(notifications)} notifications")
                
                # Debug: Show all notification details
                for i, notification in enumerate(notifications[:5]):  # Show first 5
                    reason = getattr(notification, 'reason', 'unknown')
                    indexed_at = getattr(notification, 'indexed_at', 'unknown')
                    uri = getattr(notification, 'uri', 'unknown')[:50]
                    print(f"  {i+1}. Reason: {reason}, Time: {indexed_at}, URI: {uri}...")
                
                # Filter notifications based on timestamp and processed set
                filtered_notifications = []
                print(f"🔍 Current last processed timestamp: {self.last_processed_timestamp}")
                
                for notification in notifications:
                    notification_time = getattr(notification, 'indexed_at', None)
                    notification_uri = getattr(notification, 'uri', None)
                    
                    # Skip if we've already processed this notification
                    if notification_uri in self.processed_notifications:
                        print(f"⏭️ Skipping already processed notification: {notification_uri[:50]}...")
                        continue
                    
                    # Simple filter: only process mentions from the last 2 hours
                    from datetime import datetime, timedelta, timezone
                    if notification_time:
                        try:
                            notification_dt = datetime.fromisoformat(notification_time.replace('Z', '+00:00'))
                            cutoff_time = datetime.now(timezone.utc) - timedelta(hours=2)
                            if notification_dt < cutoff_time:
                                print(f"⏭️ Skipping notification older than 2 hours: {notification_time}")
                                continue
                        except Exception as e:
                            print(f"⚠️ Error parsing notification timestamp {notification_time}: {e}")
                            continue
                    
                    filtered_notifications.append(notification)
                
                notifications = filtered_notifications
                print(f"📬 After filtering: {len(notifications)} new notifications")
                
                for notification in notifications:
                    # Debug: print notification type and reason
                    reason = getattr(notification, 'reason', 'unknown')
                    print(f"🔍 Notification type: {reason}")
                    
                    if reason == 'mention':
                        print("🎯 Processing mention notification")
                        await self.process_mention(notification)
                    else:
                        print(f"⏭️ Skipping notification type: {reason}")
                
                # Mark all notifications as read at the end of processing cycle
                try:
                    await self.mark_notification_read("")
                    print("📝 Marked all notifications as read for this cycle")
                except Exception as e:
                    print(f"⚠️ Could not mark notifications as read: {e}")
                
                # Display queue statistics
                stats = queue_manager.get_stats()
                if stats["queue_length"] > 0 or stats["processing"]:
                    print(f"📊 Queue: {stats['queue_length']} pending, {stats['total_requests']} total, {stats['successful_requests']} success, {stats['failed_requests']} failed")
                
                # Wait before next check
                await asyncio.sleep(30)  # Check every 30 seconds
                
            except Exception as e:
                print(f"❌ Error in mention monitoring: {e}")
                await asyncio.sleep(60)  # Wait longer on error
