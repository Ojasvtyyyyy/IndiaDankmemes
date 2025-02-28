import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Telegram Config
    TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
    if not TELEGRAM_TOKEN:
        raise ValueError("TELEGRAM_TOKEN environment variable is not set!")
    
    # Reddit Config
    REDDIT_CLIENT_ID = os.getenv('REDDIT_CLIENT_ID')
    if not REDDIT_CLIENT_ID:
        raise ValueError("REDDIT_CLIENT_ID environment variable is not set!")
        
    REDDIT_CLIENT_SECRET = os.getenv('REDDIT_CLIENT_SECRET')
    if not REDDIT_CLIENT_SECRET:
        raise ValueError("REDDIT_CLIENT_SECRET environment variable is not set!")
    
    SUBREDDIT = 'indiandankmemes'
    
    # Bot Config
    ALLOWED_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.gif', '.mp4', '.webm')
    MAX_CAPTION_LENGTH = 1024
    
    # Command Descriptions
    COMMANDS = {
        'meme': 'Get a random meme',
        'memetoday': 'Get memes from last 24 hours',
        'meme3days': 'Get memes from last 3 days',
        'memeweek': 'Get memes from last week',
        'memeforever': 'Get memes from all time',
        'stats': 'View subreddit statistics',
        'trending': 'See top posts',
        'about': 'About this bot'
    }
