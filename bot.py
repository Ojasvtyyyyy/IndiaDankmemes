import praw
import telegram
from telegram import Update, BotCommand
from telegram.ext import Updater, CommandHandler, CallbackContext
import random
from datetime import datetime
from config import Config
from utils import performance
import asyncio
import html

reddit = praw.Reddit(
    client_id=Config.REDDIT_CLIENT_ID,
    client_secret=Config.REDDIT_CLIENT_SECRET,
    user_agent='DankMemesBot/2.0'
)

bot = telegram.Bot(token=Config.TELEGRAM_TOKEN)

# Command Handlers
async def set_commands(bot):
    commands = [
        BotCommand(command, description) 
        for command, description in Config.COMMANDS.items()
    ]
    await bot.set_my_commands(commands)

async def start(update: Update, context: CallbackContext):
    performance.increment_request()
    welcome_text = f"""
🎉 *Welcome to IndianDankMemes Bot\!*

I serve fresh memes from r/{Config.SUBREDDIT}\!

*Available Commands:*
{format_commands_list()}

_Made with ❤️ by @Krish_devare
    """
    await update.message.reply_text(welcome_text, parse_mode='MarkdownV2')

def format_commands_list():
    return '\n'.join([
        f"/{cmd} \- {desc}" 
        for cmd, desc in Config.COMMANDS.items()
    ])

async def get_meme_by_time(update: Update, context: CallbackContext, days=None):
    performance.increment_request()
    try:
        subreddit = reddit.subreddit(Config.SUBREDDIT)
        memes = []
        
        if days is None:
            submissions = subreddit.hot(limit=100)
        else:
            submissions = subreddit.new(limit=None)
            
        current_time = datetime.utcnow()
        
        for submission in submissions:
            if days is not None:
                post_time = datetime.fromtimestamp(submission.created_utc)
                if (current_time - post_time).days > days:
                    break
                    
            if not submission.stickied and submission.url.endswith(Config.ALLOWED_EXTENSIONS):
                memes.append(submission)

        if memes:
            meme = random.choice(memes)
            caption = f"*{html.escape(meme.title)}*\n\n💬 {meme.num_comments} | ⬆️ {meme.score}"
            
            if len(caption) > Config.MAX_CAPTION_LENGTH:
                caption = caption[:Config.MAX_CAPTION_LENGTH-3] + "..."
                
            if meme.url.endswith(('.mp4', '.webm')):
                await update.message.reply_video(meme.url, caption=caption, parse_mode='HTML')
            else:
                await update.message.reply_photo(meme.url, caption=caption, parse_mode='HTML')
        else:
            await update.message.reply_text("😢 No memes found!")
            
    except Exception as e:
        performance.increment_error()
        print(f"Error: {str(e)}")
        await update.message.reply_text("🚫 Error fetching meme! Please try again later.")

async def get_stats(update: Update, context: CallbackContext):
    performance.increment_request()
    try:
        subreddit = reddit.subreddit(Config.SUBREDDIT)
        stats = f"""
📊 *Subreddit Statistics*
Subscribers: {subreddit.subscribers:,}
Active Users: {subreddit.active_user_count:,}

🤖 *Bot Statistics*
Uptime: {performance.get_uptime()}
Requests Handled: {performance.request_count:,}
Errors: {performance.error_count:,}
        """
        await update.message.reply_text(stats, parse_mode='Markdown')
    except Exception as e:
        performance.increment_error()
        await update.message.reply_text("Error fetching stats!")

async def trending(update: Update, context: CallbackContext):
    performance.increment_request()
    try:
        subreddit = reddit.subreddit(Config.SUBREDDIT)
        top_posts = subreddit.hot(limit=5)
        
        response = "*🔥 Trending Memes:*\n\n"
        for i, post in enumerate(top_posts, 1):
            response += f"{i}. {post.title}\n⬆️ {post.score} | 💬 {post.num_comments}\n\n"
            
        await update.message.reply_text(response, parse_mode='Markdown')
    except Exception as e:
        performance.increment_error()
        await update.message.reply_text("Error fetching trending memes!")

async def about(update: Update, context: CallbackContext):
    about_text = """
🤖 *About DankMemes Bot*

A Reddit\-powered Telegram bot that brings you the dankest memes from r/indiandankmemes\.

*Features:*
- Fresh memes from hot posts
- Historical memes from all time
- Trending memes
- Subreddit statistics
- Multiple time filters

*Developer:* @YourUsername
*Version:* 2\.0
*Framework:* python\-telegram\-bot

_For issues/suggestions, contact developer_
    """
    await update.message.reply_text(about_text, parse_mode='MarkdownV2')

def start_bot():
    updater = Updater(Config.TELEGRAM_TOKEN, use_context=True)
    dp = updater.dispatcher
    
    # Register command handlers
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('meme', lambda u,c: get_meme_by_time(u,c)))
    dp.add_handler(CommandHandler('memeforever', lambda u,c: get_meme_by_time(u,c)))
    dp.add_handler(CommandHandler('memetoday', lambda u,c: get_meme_by_time(u,c, days=1)))
    dp.add_handler(CommandHandler('meme3days', lambda u,c: get_meme_by_time(u,c, days=3)))
    dp.add_handler(CommandHandler('memeweek', lambda u,c: get_meme_by_time(u,c, days=7)))
    dp.add_handler(CommandHandler('stats', get_stats))
    dp.add_handler(CommandHandler('trending', trending))
    dp.add_handler(CommandHandler('about', about))
    
    # Set commands menu
    asyncio.run(set_commands(bot))
    
    updater.start_polling()
    updater.idle()
