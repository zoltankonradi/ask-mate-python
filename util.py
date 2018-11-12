from datetime import datetime
import bcrypt

# KZoli - Generates time in the requested format.
def generate_time():
    dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return dt


def hash_password(password):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    hashed_password = hashed_password.decode('utf-8')
    return hashed_password


def verify_password(password, hashed_password):
    hashed_bytes_password = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password.encode('utf-8'), hashed_bytes_password)
