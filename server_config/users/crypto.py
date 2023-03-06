from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

from cryptography.fernet import Fernet
# message = b"A message I want to sign"
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
)
public_key = private_key.public_key()


def encrypt(plain_data: bytes):
    cipher_data = public_key.encrypt(
        plain_data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return cipher_data


def decrypt(cipher_data, private_key):
    decrpyted = private_key.decrypt(
        cipher_data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return decrpyted


key = Fernet.generate_key()
print(key)
fernet = Fernet(key)
encrypt_str = fernet.encrypt(b'Hello World')
print(encrypt_str)

decrypt_str = fernet.decrypt(encrypt_str)
print(decrypt_str)
