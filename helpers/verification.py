import random
import string


def generate_code(base_url, user_id):
    code = ''.join(random.choices(string.digits, k=6))
    verify_url = f"http://{base_url}/verify/{user_id}/?code={code}"
    return verify_url, code