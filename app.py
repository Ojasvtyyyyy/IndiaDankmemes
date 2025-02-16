from flask import Flask, jsonify
from bot import start_bot
import threading
from utils import performance
import logging
import os

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Log environment variables (safely)
logger.info("Checking environment variables...")
logger.info(f"TELEGRAM_TOKEN exists: {bool(os.getenv('TELEGRAM_TOKEN'))}")
logger.info(f"REDDIT_CLIENT_ID exists: {bool(os.getenv('REDDIT_CLIENT_ID'))}")
logger.info(f"REDDIT_CLIENT_SECRET exists: {bool(os.getenv('REDDIT_CLIENT_SECRET'))}")

app = Flask(__name__)
bot_thread = None

@app.route('/')
def home():
    return "Bot is running!"

@app.route('/health')
def health_check():
    stats = performance.get_stats()
    return jsonify({
        'status': 'healthy',
        'uptime': stats['uptime'],
        'requests': stats['requests'],
        'errors': stats['errors'],
        'env_vars': {
            'telegram_token_exists': bool(os.getenv('TELEGRAM_TOKEN')),
            'reddit_client_id_exists': bool(os.getenv('REDDIT_CLIENT_ID')),
            'reddit_secret_exists': bool(os.getenv('REDDIT_CLIENT_SECRET'))
        }
    })

def run_bot():
    try:
        logger.info("Starting bot thread...")
        start_bot()
    except Exception as e:
        logger.error(f"Bot Error: {str(e)}")

def start_flask_thread():
    global bot_thread
    if bot_thread is None or not bot_thread.is_alive():
        bot_thread = threading.Thread(target=run_bot)
        bot_thread.daemon = True
        bot_thread.start()
        logger.info("Bot thread started")

if __name__ == '__main__':
    start_flask_thread()
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
