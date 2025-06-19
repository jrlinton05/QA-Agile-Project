from cryptography.fernet import Fernet
from Source.Constants.Constants import ENCRYPTION_KEY

def encrypt_string(string_to_encrypt):
    fernet = Fernet(ENCRYPTION_KEY)
    return fernet.encrypt(string_to_encrypt.encode())
