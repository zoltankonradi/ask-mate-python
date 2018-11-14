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


def separate_string(string, substring):
    separated_string = []
    clean_string_list = []
    while string.find(substring) != -1:
        index = string.find(substring)
        separated_string.append(string[:index])
        separated_string.append(substring)
        string = string[index+len(substring):]
    for i in range(len(separated_string)):
        if separated_string[i] != '':
            clean_string_list.append(separated_string[i])
    return clean_string_list
