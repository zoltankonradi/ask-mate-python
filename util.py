from datetime import datetime


# KZoli - Generates time in the requested format.
def generate_time():
    dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return dt
