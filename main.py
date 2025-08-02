#!/usr/bin/env python3
"""
Main entry point for the Bluesky sentiment analysis bot.
"""

import os
import sys
import asyncio
from dotenv import load_dotenv
from bluesky import BlueskyClient
from vibe import VibeAnalyzer
from analyze import SentimentAnalyzer
from responder import ResponseGenerator

# Load environment variables
load_dotenv()

async def main():
    """Main function to run the sentiment analysis bot."""
    print("Starting Bluesky Sentiment Analysis Bot...")
    
    try:
        # Health check - print environment info
        print("🔍 Health check:")
        print(f"   Python version: {sys.version}")
        print(f"   Working directory: {os.getcwd()}")
        print(f"   Files in directory: {os.listdir('.')}")
        
        # Initialize components
        print("🔧 Initializing components...")
        sentiment_analyzer = SentimentAnalyzer()
        vibe_analyzer = VibeAnalyzer()
        response_generator = ResponseGenerator()
        bluesky_client = BlueskyClient()
        
        # Set up the processing pipeline
        print("🔗 Setting up processing pipeline...")
        bluesky_client.sentiment_analyzer = sentiment_analyzer
        bluesky_client.vibe_analyzer = vibe_analyzer
        bluesky_client.response_generator = response_generator
        
        print("🚀 Starting monitoring...")
        # Start monitoring feeds
        await bluesky_client.start_monitoring()
    except KeyboardInterrupt:
        print("\nShutting down gracefully...")
    except Exception as e:
        print(f"❌ Error in main: {e}")
        print(f"❌ Error type: {type(e)}")
        import traceback
        print(f"❌ Traceback: {traceback.format_exc()}")


if __name__ == "__main__":
    asyncio.run(main())
