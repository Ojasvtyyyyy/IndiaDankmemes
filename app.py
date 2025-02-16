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
    start_bot()

# Start the bot in a separate thread
bot_thread = threading.Thread(target=run_bot)
bot_thread.start()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
