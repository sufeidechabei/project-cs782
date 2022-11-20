""" Too Simple of a test """
import binascii as binascii

import crypto.util as crypto
import arthm_coding.encoder as encoder
import arthm_coding.decoder as decoder
import arthm_coding.util as util

secret_msg = "UW - Madison"
key = crypto.obtain_key("super_simple")

print("Message to encrypt = "+secret_msg)
print()
print()

iv, ct = crypto.encrypt_aes_cbc(key, secret_msg)
print("Obtained IV = "+iv.hex())
print("Obtained CT = "+ct.hex())
print("----------- translate  CT to binary ---------")
ct_bin = str(bin(int(ct.hex(),16)).zfill(8))[2:]
print("Obtained CT = "+ct_bin)
#print(hex(int(ct_bin,2)))


print(len(ct_bin))
print()

""" This is totally not the correct way but lets try first """
twit_list = []
for i in range(0,4):
    sub_ct_bin = ct_bin[i*32:(i+1)*32]
    emit = decoder.decode(sub_ct_bin)
    print(sub_ct_bin)
    twit_list.append(emit)

print("Translate each 32-bit chunck with decoder:")
for twit in twit_list:
    print("#"+" ".join(twit))


print()
print()
print("Attempt to translate them back with encoder:")
reassemble= ""
for twit in twit_list:
    each = "".join(encoder.encode(twit))[:32]
    print(each)
    reassemble = reassemble + each



print()





