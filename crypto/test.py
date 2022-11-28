from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad

SamplePlainText = [b"Hello World!",
        b"Hitler is dead.",
        b"Death Start plan is on scarif",
        b"3.1415926535897932384626",
        b"John Doe; Male; Age 27; COD unknown",
        ]

def test():
    key = get_random_bytes(16)

    print("Key is "+key.hex())
    print()


    for txt in SamplePlainText:
        cipher = AES.new(key, AES.MODE_CBC)
        ciphered_txt = cipher.encrypt(pad(txt, AES.block_size))
        print(str(txt)+" ------->  "+cipher.iv.hex()+"  |  "+ciphered_txt.hex())


if __name__ == "__main__":
    test()
