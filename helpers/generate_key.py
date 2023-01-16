import random
import string

def generate_api_key():
    api_key = ''.join(random.choices(string.digits, k=20))
    print("the api_key is ", api_key)
    return api_key