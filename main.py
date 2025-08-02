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

async def start_http_server():
    """Start a simple HTTP server to keep Railway from stopping the container."""
    import aiohttp
    from aiohttp import web
    
    async def health_check(request):
        return web.Response(text="Bot is running! 🚀")
    
    app = web.Application()
    app.router.add_get('/', health_check)
    app.router.add_get('/health', health_check)
    
    runner = web.AppRunner(app)
    await runner.setup()
    
    # Get port from Railway environment or use default
    port = int(os.getenv('PORT', 8080))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    
    print(f"🌐 HTTP server started on port {port}")
    return runner

async def main():
    """Main function to run the sentiment analysis bot."""
    print("Starting Bluesky Sentiment Analysis Bot...")
    
    try:
        # Health check - print environment info
        print("🔍 Health check:")
        print(f"   Python version: {sys.version}")
        print(f"   Working directory: {os.getcwd()}")
        print(f"   Files in directory: {os.listdir('.')}")
        
        # Start HTTP server first
        http_runner = await start_http_server()
        
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
        # Run both HTTP server and bot monitoring concurrently
        bot_task = asyncio.create_task(bluesky_client.start_monitoring())
        
        # Keep the HTTP server running indefinitely
        while True:
            await asyncio.sleep(1)
            if bot_task.done():
                print("❌ Bot monitoring stopped unexpectedly")
                break
    except KeyboardInterrupt:
        print("\nShutting down gracefully...")
    except Exception as e:
        print(f"❌ Error in main: {e}")
        print(f"❌ Error type: {type(e)}")
        import traceback
        print(f"❌ Traceback: {traceback.format_exc()}")


if __name__ == "__main__":
    asyncio.run(main())
