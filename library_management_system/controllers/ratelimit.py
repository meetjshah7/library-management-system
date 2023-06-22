from datetime import datetime
from time import sleep
from functools import wraps

class RateLimit:

    def __init__(self):
        self.rate_limit_details = {}

    def reset_count_and_first_call(self, api_name):
        self.rate_limit_details[api_name] = {
            'first_call': datetime.now(),
            'count': 1
        }

    def get_time_diff_in_seconds(self, api_name):
        return (datetime.now() - self.rate_limit_details[api_name]['first_call']).total_seconds()


    def wait(self, api_name: str, max_calls_in_window: int, window_period_in_seconds: int):
        def rate_limit_decorator(func):
            @wraps(func)
            def ratelimit_wrapper(*args, **kwargs):
                if api_name not in self.rate_limit_details:
                    self.reset_count_and_first_call(api_name)
                elif self.rate_limit_details[api_name]['count'] < max_calls_in_window:
                    self.rate_limit_details[api_name]['count'] += 1
                else:
                    time_diff = self.get_time_diff_in_seconds(api_name)
                    if time_diff > window_period_in_seconds:
                        self.reset_count_and_first_call(api_name)
                    else:
                        sleep(time_diff)
                        self.reset_count_and_first_call(api_name)
                return func(*args, **kwargs)
            return ratelimit_wrapper
        return rate_limit_decorator


rate_limit: RateLimit = RateLimit()