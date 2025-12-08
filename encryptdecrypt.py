from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from hashlib import sha256

def derive_key(password):
    return sha256(password.encode()).digest()

def encrypt(data, password):
    key = derive_key(password)

    iv = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)

    print(iv)

    pad_len = 16 - (len(data) % 16)
    data += bytes([pad_len]) * pad_len

    encrypted = cipher.encrypt(data)
    return iv + encrypted 

def decrypt(encrypted, password):
    key = derive_key(password)
    iv = encrypted[:16]
    ciphertext = encrypted[16:]

    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted = cipher.decrypt(ciphertext)

    pad_len = decrypted[-1]
    return decrypted[:-pad_len]
