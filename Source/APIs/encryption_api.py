from cryptography.fernet import Fernet
from Source.Constants.constants import ENCRYPTION_KEY

def encrypt_string(string_to_encrypt):
    fernet = Fernet(ENCRYPTION_KEY)
    return fernet.encrypt(string_to_encrypt.encode())

def decrypt_string(string_to_decrypt):
    fernet = Fernet(ENCRYPTION_KEY)
    return fernet.decrypt(string_to_decrypt).decode()
