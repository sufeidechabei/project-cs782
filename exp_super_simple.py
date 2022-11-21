""" Too Simple of a test """
import binascii as binascii

import crypto.util as crypto
import arthm_coding.encoder as encoder
import arthm_coding.decoder as decoder
import arthm_coding.util as util

def run_exp(secret_msg):
    print()
    print("======================================================")
    key = crypto.obtain_key("super_simple")

    print("Message to encrypt = "+secret_msg)
    print()
    print()

    iv, ct = crypto.encrypt_aes_cbc(key, secret_msg)
    print("Obtained IV = "+iv.hex())
    print("Obtained CT = "+ct.hex())
    print("----------- translate  CT to binary ---------")
    binary_ct_len = len(ct.hex())*4
    ct_bin = (str(bin(int(ct.hex(),16)))[2:]).zfill(binary_ct_len)
    print(ct_bin)
#print(hex(int(ct_bin,2)))

    print()
    print("Turning the CT into English:")
    print("---------------------------------------------")
    eng = decoder.decode_ytb(ct_bin, "complx")
    print("#"+" ".join(eng))
    
    
    print()
    print("Encode English back to CT:")
    
    
    encoded_ct = "".join(encoder.encode_ytb(eng, "complx"))[:binary_ct_len]
    print(encoded_ct)
    
    
    print("---------- translate CT to hex ---------------")
    hex_encoded_ct = hex(int(encoded_ct,2))
    print(hex_encoded_ct)
    
    
    print()
    print()
    new_ct = bytes.fromhex(hex_encoded_ct[2:])
    new_msg = crypto.decrypt_aes_cbc(key, iv, new_ct)
    
    print("Decrypted message = "+new_msg)


run_exp("UW - Madison")
run_exp("AF may lack fresh water!")
#run_exp("Ba Yue Qiu Gao Feng Nu Hao, Juan Wo Wu Shang San Chong Mao.")
    #print()
    #print("breaking into chunks")
    #twit_list = []
    #for i in range(0,1):
    #    sub_ct_bin = ct_bin[i*128:(i+1)*128]
    #    print(sub_ct_bin, end=" ")
    #    emit = decoder.decode_ytb(sub_ct_bin, "complx")
    #    twit_list.append(emit)

#print()

#print("Translate each 32-bit chunck with decoder:")
#for twit in twit_list:
    #print("#"+" ".join(twit))


#print()
#print()
#print("Attempt to translate them back with encoder:")
#reassemble= ""
#print("Encoded  CT = ", end = "")
#
#for twit in twit_list:
#    each = "".join(encoder.encode_ytb(twit, "complx"))[:64]
#    print(each,end = " ")
#    reassemble = reassemble + each
#
#
#print()
#print("Results from translating each 32-bit chunck with decoder:")
#for twit in twit_list:
#    print("#"+" ".join(twit))



#print()
#print("Results from translating Re-Encoded with decoder:")

#twit_list_2 = []
#for i in range(0,2):
#    sub_ct_bin = reassemble[i*64:(i+1)*64]
#    #print(sub_ct_bin)
#    emit = decoder.decode_ytb(sub_ct_bin, "complx")
#    twit_list_2.append(emit)

#for twit in twit_list_2:
#    print("#"+" ".join(twit))

#print()
#print()
#print()
#print()
#print()
#print()
#print("Trying decode the entire CT")
#print()
#emit2 = decoder.decode_ytb(ct_bin, "complx")
#print(" ".join(emit2))
