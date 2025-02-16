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

def run_bot():
    try:
        start_bot()
    except Exception as e:
        print(f"Bot Error: {str(e)}")

if __name__ == '__main__':
    # Start the bot in a separate thread
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.daemon = True  # Make thread daemon so it closes with the main program
    bot_thread.start()
    
    app.run(host='0.0.0.0', port=10000)
