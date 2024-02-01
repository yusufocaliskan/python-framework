import uuid
import secrets
import string


def generate_client_id():
    return str(uuid.uuid4())


def generate_secret_key(length=32):
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))
