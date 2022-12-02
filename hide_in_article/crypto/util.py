"""Utils for cryptographic operations"""

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

import os
import hashlib

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


def get_md5(text):
    return hashlib.md5(text.encode()).hexdigest()


def produce_header(seed, ct_chunk_count):
    # produce a header base on the initial seed and the length of the cipher text
    md5hash = get_md5(seed)
    print(md5hash)
    header = md5hash[:13] + hex(ct_chunk_count)[2:]
    print("plain header is "+header+"  len = "+str(len(header)))
    header_key = obtain_key("header_key")
    iv, ct = encrypt_aes_cbc(header_key, header)
    print("ecryt header is "+iv.hex()+" "+ct.hex())
    return iv,ct
    
def check_header(partial_decoded, seed):
    # check if the partially_decoded text can be decrypted and has a matching partial md5 of the seed.
    # it it is, return the count of 16 byte chuncks. otherwise, return None
    iv = partial_decoded[:16]
    ct = partial_decoded[16:]
    if len(iv) + len(ct) != len(partial_decoded):
        print("!!! Length mismatch")
        return None
    header_key = obtain_key("header_key")
    try:
        header = decrypt_aes_cbc(header_key, iv, ct)
    except:
        print("Header cannot be decrypted")
        return None
    new_md5 = get_md5(seed)
    if (header[:13] == new_md5[:13]):
        chunk_count_hex = header[-2:]
        print(chunk_count_hex)
        return int(chunk_count_hex, 16)
    else:
        return None





if __name__ == "__main__":
    while(1):
        s = input()
        iv,ct = produce_header(s, 17)
        code = iv+ct
        a = check_header(code, "asdasdsadasd")
        print(a)
    # Test the util module
    key = obtain_key("test01")
    print("Key = "+key.hex()+"\n----------")
    test_plain_text = "1234567890123456"
    iv, cipher_txt = encrypt_aes_cbc(key, test_plain_text)
    print("Encryption results:")
    print("  IV = "+iv.hex())
    print("  CT = "+cipher_txt.hex())
    print("---------------------")
    decryption_res = decrypt_aes_cbc(key, iv, cipher_txt)
    print("Decryption result = "+decryption_res)
