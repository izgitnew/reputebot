#!/usr/bin/env python3
"""
Test script to demonstrate ReputeBot response scenarios
"""

from vibe import VibeAnalyzer
from analyze import SentimentAnalyzer
from responder import ResponseGenerator

def test_response_scenarios():
    """Test different response scenarios for the ReputeBot."""
    
    # Initialize components
    sentiment_analyzer = SentimentAnalyzer()
    vibe_analyzer = VibeAnalyzer()
    response_generator = ResponseGenerator()
    
    print("🎯 REPUTEBOT RESPONSE SCENARIOS\n")
    print("=" * 60)
    
    # Scenario 1: Tech/Science Account
    print("\n📱 SCENARIO 1: Tech/Science Account")
    print("-" * 40)
    tech_content = """
    Just deployed our new AI model to production! The transformer architecture 
    is showing incredible results on our benchmark tests. Machine learning 
    breakthroughs are happening every day. #AI #ML #Tech #Innovation
    """
    sentiment = sentiment_analyzer.analyze_sentiment(tech_content)
    vibe = vibe_analyzer.analyze_vibe(tech_content)
    response = response_generator.generate_response(sentiment, vibe, tech_content, "techguru.bsky.social")
    print(response)
    
    # Scenario 2: Sports/Entertainment Account
    print("\n🏀 SCENARIO 2: Sports/Entertainment Account")
    print("-" * 40)
    sports_content = """
    What an incredible game tonight! The energy in the arena was electric. 
    Our team showed amazing teamwork and determination. Fans were absolutely 
    incredible - thank you for the support! #Basketball #Championship #Team
    """
    sentiment = sentiment_analyzer.analyze_sentiment(sports_content)
    vibe = vibe_analyzer.analyze_vibe(sports_content)
    response = response_generator.generate_response(sentiment, vibe, sports_content, "sportsfan.bsky.social")
    print(response)
    
    # Scenario 3: News/Journalism Account
    print("\n📰 SCENARIO 3: News/Journalism Account")
    print("-" * 40)
    news_content = """
    Breaking: Major policy changes announced today. Our investigative team 
    has been working on this story for months. Important developments that 
    will affect millions of people. Stay tuned for updates. #News #Politics
    """
    sentiment = sentiment_analyzer.analyze_sentiment(news_content)
    vibe = vibe_analyzer.analyze_vibe(news_content)
    response = response_generator.generate_response(sentiment, vibe, news_content, "newshound.bsky.social")
    print(response)
    
    # Scenario 4: Personal/Lifestyle Account
    print("\n🌟 SCENARIO 4: Personal/Lifestyle Account")
    print("-" * 40)
    lifestyle_content = """
    Beautiful morning walk in the park! The flowers are blooming and the 
    birds are singing. Taking time to appreciate the little things in life. 
    Remember to practice gratitude every day. #Mindfulness #Nature #Life
    """
    sentiment = sentiment_analyzer.analyze_sentiment(lifestyle_content)
    vibe = vibe_analyzer.analyze_vibe(lifestyle_content)
    response = response_generator.generate_response(sentiment, vibe, lifestyle_content, "lifestyleguru.bsky.social")
    print(response)
    
    # Scenario 5: Business/Professional Account
    print("\n💼 SCENARIO 5: Business/Professional Account")
    print("-" * 40)
    business_content = """
    Quarterly earnings report shows strong growth across all divisions. 
    Our team's hard work is paying off. Excited about the new partnerships 
    we're announcing next week. #Business #Success #Leadership
    """
    sentiment = sentiment_analyzer.analyze_sentiment(business_content)
    vibe = vibe_analyzer.analyze_vibe(business_content)
    response = response_generator.generate_response(sentiment, vibe, business_content, "ceo.bsky.social")
    print(response)
    
    # Scenario 6: Negative/Toxic Account
    print("\n⚠️ SCENARIO 6: Negative/Toxic Account")
    print("-" * 40)
    negative_content = """
    Everything is terrible and nothing matters. People are so stupid and 
    the world is going to hell. I hate this place and everyone in it. 
    Nothing good ever happens anymore.
    """
    sentiment = sentiment_analyzer.analyze_sentiment(negative_content)
    vibe = vibe_analyzer.analyze_vibe(negative_content)
    response = response_generator.generate_response(sentiment, vibe, negative_content, "grumpy.bsky.social")
    print(response)
    
    # Scenario 7: Mixed/Neutral Account
    print("\n🔄 SCENARIO 7: Mixed/Neutral Account")
    print("-" * 40)
    mixed_content = """
    Today was okay. Had some good moments and some bad ones. Work was 
    stressful but dinner was nice. Not sure how I feel about tomorrow. 
    Just taking it one day at a time.
    """
    sentiment = sentiment_analyzer.analyze_sentiment(mixed_content)
    vibe = vibe_analyzer.analyze_vibe(mixed_content)
    response = response_generator.generate_response(sentiment, vibe, mixed_content, "neutral.bsky.social")
    print(response)
    
    # Scenario 8: High Engagement Account
    print("\n🔥 SCENARIO 8: High Engagement Account")
    print("-" * 40)
    engagement_content = """
    AMAZING NEWS! 🎉 We just hit 100K followers! Thank you all so much 
    for the incredible support! This community is everything to me! 
    Let's celebrate together! #Milestone #Grateful #Community
    """
    sentiment = sentiment_analyzer.analyze_sentiment(engagement_content)
    vibe = vibe_analyzer.analyze_vibe(engagement_content)
    response = response_generator.generate_response(sentiment, vibe, engagement_content, "influencer.bsky.social")
    print(response)

if __name__ == "__main__":
    test_response_scenarios() 