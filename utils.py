# utils.py
from datetime import datetime

class Performance:
    def __init__(self):
        self.start_time = datetime.now()
        self.request_count = 0
        self.error_count = 0
    
    def increment_request(self):
        self.request_count += 1
    
    def increment_error(self):
        self.error_count += 1
    
    def get_uptime(self):
        delta = datetime.now() - self.start_time
        days = delta.days
        hours, remainder = divmod(delta.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{days}d {hours}h {minutes}m {seconds}s"
    
    def get_stats(self):
        return {
            'uptime': self.get_uptime(),
            'requests': self.request_count,
            'errors': self.error_count
        }

performance = Performance()
