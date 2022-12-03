"""Utils for cryptographic operations"""

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

import os


def obtain_key(name, length=256):
    """obtain the stored key with the specified name. Generate a new one if DNE"""
    key_location = "key_data/"+name
    if not os.path.isfile(key_location):
        key = get_random_bytes(length//8)
        keyfile = open(key_location, "wb")
        keyfile.write(key)
        keyfile.close()
        return key
    else:
        keyfile = open(key_location, "rb")
        key = keyfile.read()
        keyfile.close()
        return key


def encrypt_aes_cbc(key, plain_text):
    """Encrpt input text using CBC mode of AES. Return tuple of (iv, cipher text)"""
    cipher = AES.new(key, AES.MODE_CBC)
    b_plain_text = plain_text.encode()
    cipher_text = cipher.encrypt(pad(b_plain_text, AES.block_size))
    return (cipher.iv, cipher_text)

def decrypt_aes_cbc(key, iv, cipher_text):
    """Decrypt AES CBC encrupted data"""
    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    decrypted = unpad(cipher.decrypt(cipher_text), AES.block_size)
    return str(decrypted.decode())

if __name__ == "__main__":
    # Test the util module
    key = obtain_key("test01")
    print("Key = "+key.hex()+"\n----------")
    test_plain_text = "AF lacks drinking water"
    iv, cipher_txt = encrypt_aes_cbc(key, test_plain_text)
    print("Encryption results:")
    print("IV = "+iv.hex())
    print("Cipher text = "+cipher_txt.hex())
    print("---------------------")
    decryption_res = decrypt_aes_cbc(key, iv, cipher_txt)
    print("Decryption result = "+decryption_res)
