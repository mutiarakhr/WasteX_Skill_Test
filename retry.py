import time
import random

def retry(func, retries=3, delay=2):

    def wrapper(*args, **kwargs):

        for i in range(retries):
            try:
                return func(*args, **kwargs)

            except Exception as e:
                print(f"Retry {i+1}/{retries} failed:", e)

                time.sleep(delay * (i + 1) + random.random())

        raise Exception("Max retries exceeded")

    return wrapper