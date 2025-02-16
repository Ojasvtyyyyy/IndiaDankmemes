import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    REDDIT_CLIENT_ID = os.getenv('REDDIT_CLIENT_ID')
    REDDIT_CLIENT_SECRET = os.getenv('REDDIT_CLIENT_SECRET')
    TELEGRAM_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    SUBREDDIT = 'indiandankmemes'
    ALLOWED_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.gif', '.mp4', '.webm')
    MAX_CAPTION_LENGTH = 1024
    COMMANDS = {
        'start': 'Start the bot and see commands',
        'meme': 'Get a random hot meme',
        'memeforever': 'Get a random meme from all time',
        'memetoday': 'Get a meme from last 24 hours',
        'meme3days': 'Get a meme from last 3 days',
        'memeweek': 'Get a meme from last week',
        'stats': 'Show subreddit statistics',
        'help': 'Show detailed help message',
        'about': 'About this bot',
        'trending': 'Get trending memes'
    }
