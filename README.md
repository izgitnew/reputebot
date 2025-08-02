# ReputeBot - Bluesky Reputation Analysis Bot

A Bluesky bot that analyzes user accounts and provides detailed reputation reports when mentioned.

## Features

- **Mention-based Analysis**: Responds to mentions with detailed account analysis
- **Sentiment Analysis**: Uses VADER sentiment analysis with custom social media lexicon
- **Vibe Analysis**: Analyzes overall tone and mood of content
- **Activity Tracking**: Calculates accurate posts per day using 30-day data
- **Content Categorization**: Identifies content categories (sports, tech, entertainment, etc.)
- **Persona Detection**: Determines user personas based on content patterns
- **Rate Limiting**: Built-in API rate limiting and request queuing
- **Duplicate Prevention**: Prevents duplicate responses and re-processing

## Setup

### Prerequisites

- Python 3.8+
- Bluesky account with app password

### Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd ReputeBot
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file with your Bluesky credentials:
```bash
BLUESKY_HANDLE=your-handle.bsky.social
BLUESKY_PASSWORD=your-app-password
```

4. Run the bot:
```bash
python main.py
```

## Environment Variables

- `BLUESKY_HANDLE`: Your Bluesky handle (e.g., `reputebot.bsky.social`)
- `BLUESKY_PASSWORD`: Your Bluesky app password

## Usage

1. Start the bot
2. Mention `@reputebot.bsky.social` on any post
3. The bot will analyze the account and provide a reputation report

## Response Format

```
Should you follow @username?
✅ Yes — here's why:
🔹 Vibes: Encouraging
🔹 Persona: Enthusiast
🔹 ~27 posts/day, mostly original
🔹 Posts on sports
📌 Add to your Sports Feed.
```

## Deployment

### Railway

1. Connect your GitHub repository to Railway
2. Add environment variables in Railway dashboard
3. Deploy automatically

### Other Platforms

- **DigitalOcean**: Use a droplet with PM2 or systemd
- **Render**: Deploy as a web service
- **Heroku**: Use the Procfile method

## Architecture

- `main.py`: Entry point and bot orchestration
- `bluesky.py`: Bluesky API client and notification handling
- `analyze.py`: Sentiment analysis using VADER
- `vibe.py`: Vibe and tone analysis
- `responder.py`: Response generation and formatting
- `queue_manager.py`: API rate limiting and request queuing
- `utils.py`: Utility functions

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License 