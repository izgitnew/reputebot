#!/usr/bin/env python3
"""
Test script to verify text truncation for Bluesky posts.
"""

def test_truncation():
    """Test the text truncation logic."""
    
    # Test case 1: Short text (should not be truncated)
    short_text = "This is a short response that should not be truncated."
    print(f"Short text ({len(short_text)} chars): {short_text}")
    
    if len(short_text) > 280:
        short_text = short_text[:277] + "..."
        print(f"📝 Truncated to: {short_text}")
    else:
        print("✅ No truncation needed")
    
    print()
    
    # Test case 2: Long text (should be truncated)
    long_text = """Why should you follow @nba.com?

🔹 Vibes: Optimistic, energetic, and motivating
🔹 Archetype: Innovator / Pioneer
🔹 Activity: ~1 post/day, mostly original content
🔹 Engagement: Avg 7 likes, 3 reposts
🔹 Network: Connected to @tech.leaders, @design.masters, @startup.founders
🔹 Content: Lifestyle tips, wellness practices, personal growth

📈 Consistent, connected, and brings useful insight.

🗂️ Recommendation:
👉 This account should be added to your Gaming Feed.

(Tag me with any @handle to check their rep!)"""
    
    print(f"Long text ({len(long_text)} chars): {long_text}")
    
    if len(long_text) > 280:
        truncated_text = long_text[:277] + "..."
        print(f"📝 Truncated to ({len(truncated_text)} chars): {truncated_text}")
    else:
        print("✅ No truncation needed")
    
    print()
    
    # Test case 3: Very long text
    very_long_text = "This is a very long text that exceeds the 280 character limit by quite a lot. " * 10
    print(f"Very long text ({len(very_long_text)} chars): {very_long_text[:100]}...")
    
    if len(very_long_text) > 280:
        truncated_text = very_long_text[:277] + "..."
        print(f"📝 Truncated to ({len(truncated_text)} chars): {truncated_text}")
    else:
        print("✅ No truncation needed")

if __name__ == "__main__":
    test_truncation() 