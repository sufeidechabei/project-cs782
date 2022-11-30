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
    print("---------------------------------------------")
   
    t_str = iv.hex()+ct.hex()+".."
    t_list = []
    for i in range(0,len(t_str)//2):
        t_list.append(t_str[i*2]+t_str[i*2+1])
    print(t_list)
    re_encoded_ct = encoder.encode_ytb(t_list, "complx")
    print(hex(int("".join(re_encoded_ct),2))[2:])



    re_ct = decoder.decode_ytb(re_encoded_ct, "complx")
    print("\n"+"".join(re_ct))


run_exp("UW - Madison")
#run_exp("AF may lack fresh water!")
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
