import time
from datetime import datetime

class Performance:
    def __init__(self):
        self.start_time = time.time()
        self.request_count = 0
        self.error_count = 0

    def increment_request(self):
        self.request_count += 1

    def increment_error(self):
        self.error_count += 1

    def get_uptime(self):
        uptime_seconds = int(time.time() - self.start_time)
        days = uptime_seconds // 86400
        hours = (uptime_seconds % 86400) // 3600
        minutes = (uptime_seconds % 3600) // 60
        seconds = uptime_seconds % 60
        return f"{days}d {hours}h {minutes}m {seconds}s"

    def get_stats(self):
        return {
            'uptime': self.get_uptime(),
            'requests': self.request_count,
            'errors': self.error_count
        }

performance = Performance()
