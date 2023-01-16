from django.contrib.auth.hashers import BCryptSHA256PasswordHasher
import random
import string


def generate_api_key():
    letters = string.ascii_letters + string.digits
    raw_key = ''.join(random.choices(letters, k=50))
    key_harser = BCryptSHA256PasswordHasher()
    salt = key_harser.salt()
    harsed_key = key_harser.encode(raw_key, salt)
    return raw_key, harsed_key
