import praw
import telegram
from telegram import Update, BotCommand
from telegram.ext import Updater, CommandHandler, CallbackContext
import random
from datetime import datetime
from config import Config
from utils import performance
import logging

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

reddit = praw.Reddit(
    client_id=Config.REDDIT_CLIENT_ID,
    client_secret=Config.REDDIT_CLIENT_SECRET,
    user_agent='DankMemesBot/2.0'
)

bot = telegram.Bot(token=Config.TELEGRAM_TOKEN)

def set_commands(updater):
    try:
        commands = [
            BotCommand(command, description) 
            for command, description in Config.COMMANDS.items()
        ]
        updater.bot.set_my_commands(commands)
        logger.info("Bot commands set successfully")
        # Verify commands were set
        current_commands = updater.bot.get_my_commands()
        logger.info(f"Verified commands: {[cmd.command for cmd in current_commands]}")
    except Exception as e:
        logger.error(f"Error setting commands: {str(e)}")
        raise

def format_commands_list():
    return '\n'.join([
        f"/{cmd} \- {desc}" 
        for cmd, desc in Config.COMMANDS.items()
    ])

def start(update: Update, context: CallbackContext):
    logger.info(f"Start command received from user {update.effective_user.id}")
    performance.increment_request()
    welcome_text = f"""
🎉 *Welcome to IndianDankMemes Bot\!*

I serve fresh memes from r/{Config.SUBREDDIT}\!

*Available Commands:*
{format_commands_list()}

_Made with ❤️ by @Krish_Devare_
    """
    update.message.reply_text(welcome_text, parse_mode='MarkdownV2')

def get_meme_by_time(update: Update, context: CallbackContext, days=None):
    logger.info(f"Meme request received from user {update.effective_user.id} with days={days}")
    performance.increment_request()
    try:
        subreddit = reddit.subreddit(Config.SUBREDDIT)
        memes = []
        
        if days is None:
            submissions = subreddit.hot(limit=50)
        else:
            submissions = subreddit.top(time_filter='all', limit=50)
            
        current_time = datetime.utcnow()
        
        for submission in submissions:
            if days is not None:
                post_time = datetime.fromtimestamp(submission.created_utc)
                if (current_time - post_time).days > days:
                    continue
                    
            if not submission.stickied and submission.url.endswith(Config.ALLOWED_EXTENSIONS):
                memes.append(submission)

        if memes:
            meme = random.choice(memes)
            caption = f"*{meme.title}*\n\n💬 {meme.num_comments} | ⬆️ {meme.score}"
            
            if len(caption) > Config.MAX_CAPTION_LENGTH:
                caption = caption[:Config.MAX_CAPTION_LENGTH-3] + "..."
                
            if meme.url.endswith(('.mp4', '.webm')):
                update.message.reply_video(meme.url, caption=caption, parse_mode='Markdown')
            else:
                update.message.reply_photo(meme.url, caption=caption, parse_mode='Markdown')
            logger.info(f"Meme sent successfully to user {update.effective_user.id}")
        else:
            update.message.reply_text("😢 No memes found!")
            logger.warning(f"No memes found for user {update.effective_user.id}")
            
    except Exception as e:
        performance.increment_error()
        logger.error(f"Error fetching meme: {str(e)}")
        update.message.reply_text("🚫 Error fetching meme! Please try again later.")

def get_stats(update: Update, context: CallbackContext):
    logger.info(f"Stats request received from user {update.effective_user.id}")
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
        update.message.reply_text(stats, parse_mode='Markdown')
        logger.info(f"Stats sent successfully to user {update.effective_user.id}")
    except Exception as e:
        performance.increment_error()
        logger.error(f"Error fetching stats: {str(e)}")
        update.message.reply_text("Error fetching stats!")

def trending(update: Update, context: CallbackContext):
    logger.info(f"Trending request received from user {update.effective_user.id}")
    performance.increment_request()
    try:
        subreddit = reddit.subreddit(Config.SUBREDDIT)
        top_posts = subreddit.top(time_filter='all', limit=5)
        
        response = "*🔥 Top Posts of All Time:*\n\n"
        for i, post in enumerate(top_posts, 1):
            response += f"{i}. {post.title}\n⬆️ {post.score} | 💬 {post.num_comments}\n\n"
            
        update.message.reply_text(response, parse_mode='Markdown')
        logger.info(f"Trending posts sent successfully to user {update.effective_user.id}")
    except Exception as e:
        performance.increment_error()
        logger.error(f"Error fetching trending posts: {str(e)}")
        update.message.reply_text("Error fetching trending memes!")

def about(update: Update, context: CallbackContext):
    logger.info(f"About request received from user {update.effective_user.id}")
    about_text = """
🤖 *About DankMemes Bot*

A Reddit\-powered Telegram bot that brings you the dankest memes from r/indiandankmemes\.

*Features:*
\- Fresh memes from hot posts
\- Historical memes from all time
\- Trending memes
\- Subreddit statistics
\- Multiple time filters

*Developer:* @Krish_Devare
*Version:* 2\.0
*Framework:* python\-telegram\-bot

_For issues/suggestions, contact developer_
    """
    update.message.reply_text(about_text, parse_mode='MarkdownV2')
    logger.info(f"About info sent successfully to user {update.effective_user.id}")

def start_bot():
    try:
        logger.info("Initializing bot...")
        updater = Updater(Config.TELEGRAM_TOKEN, use_context=True)
        dp = updater.dispatcher
        
        logger.info("Setting up command handlers...")
        
        # Register command handlers
        handlers = [
            ('start', start),
            ('meme', lambda u,c: get_meme_by_time(u,c)),
            ('memeforever', lambda u,c: get_meme_by_time(u,c)),
            ('memetoday', lambda u,c: get_meme_by_time(u,c, days=1)),
            ('meme3days', lambda u,c: get_meme_by_time(u,c, days=3)),
            ('memeweek', lambda u,c: get_meme_by_time(u,c, days=7)),
            ('stats', get_stats),
            ('trending', trending),
            ('about', about)
        ]
        
        for command, handler in handlers:
            dp.add_handler(CommandHandler(command, handler))
            logger.info(f"Registered /{command} command")
        
        # Set commands menu
        try:
            commands = [
                BotCommand(command, Config.COMMANDS[command]) 
                for command, _ in handlers
            ]
            updater.bot.set_my_commands(commands)
            logger.info("Bot commands set successfully")
            
            # Verify commands were set
            current_commands = updater.bot.get_my_commands()
            logger.info(f"Verified commands: {[cmd.command for cmd in current_commands]}")
        except Exception as e:
            logger.error(f"Error setting commands: {str(e)}")
        
        logger.info("Starting bot polling...")
        updater.start_polling(drop_pending_updates=True)
        logger.info("Bot polling started successfully!")
        
        # Keep the bot running
        updater.idle()
            
    except Exception as e:
        logger.error(f"Error in start_bot: {str(e)}")
        raise e

if __name__ == "__main__":
    start_bot()
