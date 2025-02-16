import os
import praw
import telegram
from telegram.ext import Updater, CommandHandler
import asyncio
from dotenv import load_dotenv
import random
from datetime import datetime, timedelta
from flask import Flask
import threading

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

load_dotenv()

reddit = praw.Reddit(
    client_id=os.getenv('REDDIT_CLIENT_ID'),
    client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
    user_agent='telegram_bot/1.0'
)

bot = telegram.Bot(token=os.getenv('TELEGRAM_BOT_TOKEN'))

async def get_meme_by_time(update, context, days=None):
    try:
        subreddit = reddit.subreddit('indiandankmemes')
        memes = []
        
        if days is None:
            for submission in subreddit.hot(limit=None):
                if not submission.stickied and submission.url.endswith(('.jpg', '.jpeg', '.png', '.gif')):
                    memes.append(submission)
        else:
            current_time = datetime.utcnow()
            for submission in subreddit.new(limit=None):
                post_time = datetime.fromtimestamp(submission.created_utc)
                if (current_time - post_time).days > days:
                    break
                if not submission.stickied and submission.url.endswith(('.jpg', '.jpeg', '.png', '.gif')):
                    memes.append(submission)

        if memes:
            meme = random.choice(memes)
            await update.message.reply_text(meme.title)
            await update.message.reply_photo(meme.url)
        else:
            await update.message.reply_text("No memes found!")
            
    except Exception as e:
        print(f"Error: {str(e)}")
        await update.message.reply_text("Error fetching meme!")

async def get_meme_forever(update, context):
    try:
        subreddit = reddit.subreddit('indiandankmemes')
        memes = []
        
        for submission in subreddit.top('all', limit=None):
            if not submission.stickied and submission.url.endswith(('.jpg', '.jpeg', '.png', '.gif')):
                memes.append(submission)
        
        if memes:
            meme = random.choice(memes)
            await update.message.reply_text(meme.title)
            await update.message.reply_photo(meme.url)
        else:
            await update.message.reply_text("No memes found!")
            
    except Exception as e:
        print(f"Error: {str(e)}")
        await update.message.reply_text("Error fetching meme!")

async def start(update, context):
    welcome_text = """
Welcome to IndianDankMemes Bot!
Available commands:
/meme - Random meme from hot posts
/memeforever - Random meme from all time posts
/memetoday - Random meme from last 24 hours
/meme3days - Random meme from last 3 days
/memeweek - Random meme from last 7 days
    """
    await update.message.reply_text(welcome_text)

async def meme(update, context):
    await get_meme_by_time(update, context)

async def meme_today(update, context):
    await get_meme_by_time(update, context, days=1)

async def meme_3days(update, context):
    await get_meme_by_time(update, context, days=3)

async def meme_week(update, context):
    await get_meme_by_time(update, context, days=7)

def main():
    updater = Updater(os.getenv('TELEGRAM_BOT_TOKEN'), use_context=True)
    dp = updater.dispatcher
    
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('meme', meme))
    dp.add_handler(CommandHandler('memeforever', get_meme_forever))
    dp.add_handler(CommandHandler('memetoday', meme_today))
    dp.add_handler(CommandHandler('meme3days', meme_3days))
    dp.add_handler(CommandHandler('memeweek', meme_week))
    
    updater.start_polling()
    return updater

def run_flask():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

if __name__ == '__main__':
    updater = main()
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()
    updater.idle()
