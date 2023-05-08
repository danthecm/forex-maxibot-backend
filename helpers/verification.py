import random
import string


def generate_code(base_url, username):
    code = ''.join(random.choices(string.digits, k=6))
    verify_url = f"https://{base_url}/verify/{username}/?code={code}"
    return verify_url, code