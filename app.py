# app.py
from flask import Flask, jsonify
from bot import start_bot
import threading
from utils import performance

app = Flask(__name__)

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

updater = None

def run_bot():
    global updater
    try:
        updater = start_bot()
    except Exception as e:
        print(f"Bot Error: {str(e)}")
        if updater:
            updater.stop()

# Start the bot in a separate thread
bot_thread = threading.Thread(target=run_bot)
bot_thread.start()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
