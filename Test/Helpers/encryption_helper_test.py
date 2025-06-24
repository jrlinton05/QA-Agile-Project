from Source.Helpers.encryption_helper import encrypt_string, decrypt_string
from Source.Constants.constants import ENCRYPTION_KEY
from cryptography.fernet import Fernet
import pytest

def test_encrypt_and_decrypt():
    original_text = "testPassword123"
    encrypted = encrypt_string(original_text)
    assert isinstance(encrypted, bytes)

    decrypted = decrypt_string(encrypted)
    assert decrypted == original_text

def test_decrypt_invalid_token():
    invalid_token = b"invalidtoken"
    with pytest.raises(Exception):
        decrypt_string(invalid_token)
