# Python Standard Library
import random
import string


def generate_code(length=7):
    code = ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))
    return code
