# app.py
from flask import Flask, jsonify
from bot import start_bot
import threading
from utils import performance
import logging

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

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
        'errors': stats['errors']
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

# Start bot when the Flask app starts
start_flask_thread()
