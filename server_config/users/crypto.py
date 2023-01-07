from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes

from cryptography.hazmat.primitives.asymmetric import padding

message = b"A message I want to sign"


def encrypt(plain_data):
    private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
    )
    # sign the plain_data
    signature = private_key.sign(
    plain_data,
    padding.PSS(
        mgf=padding.MGF1(hashes.SHA256()),
        salt_length=padding.PSS.MAX_LENGTH
    ),
    hashes.SHA256()
    )
    
    public_key = private_key.public_key()
    
    cipher_data = public_key.encrypt(
    signature,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
    )

def decrypt(cipher_data, private_key):
    signature = private_key.decrypt(
    cipher_data,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
    )
    
    public_key = private_key.public_key()
    public_key.verify(
    signature,
    message,
    padding.PSS(
        mgf=padding.MGF1(hashes.SHA256()),
        salt_length=padding.PSS.MAX_LENGTH
    ),
    hashes.SHA256()
    )

