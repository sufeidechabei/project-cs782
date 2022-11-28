""" Too Simple of a test """
import binascii as binascii

import crypto.util as crypto
import gpt2_arthm_coding.encoderGPT2 as en_gpt2
import gpt2_arthm_coding.decoderGPT2 as de_gpt2

import time

import getopt
import sys

from datetime import datetime


def run_encryption(secret_msg, my_l, first_phrase, include_iv = False):


    print()
    print("Start encryption for '"+secret_msg+"'\n")
    t1 = time.perf_counter()
    key = crypto.obtain_key("e2e")
    iv, ct = crypto.encrypt_aes_cbc(key, secret_msg)
    t2 = time.perf_counter()
    print(f"AES encryption took {t2 - t1:0.4f} s")
    print("Generated ciphertext="+ct.hex()+"  iv="+iv.hex())

    if include_iv:
        code = iv+ct
    else:
        code = ct

    de = de_gpt2.GPT2ArthmDecoder(l=my_l, code = code, seed=first_phrase)
    t3 = time.perf_counter()
    print(f"Arithmatic decoder intialization took {t3 - t2:0.4f} s")
    T = de.decode()
    t4 = time.perf_counter()
    all_T = [first_phrase] + T
    print(f"Decoding the cipher text took {t4 - t3:0.4f} s")
    print()
    print("In list format:")
    print(all_T)
    print()
    print("In English sentence:")
    eng = "".join(all_T)
    print(eng)

    #tokens = T
    #en = en_gpt2.GPT2ArthmEncoder(l=16)
    #t5 = time.perf_counter()
    #print(f"Encoder intialization took {t5 - t4:0.4f} s")
    #D, w = en.encode(tokens)
    #t6 = time.perf_counter()
    #print(f"Encoding generated sentences took {t6 - t5:0.4f} s")
    #new_ct = bytes(D)


    #try:
    #    new_msg = crypto.decrypt_aes_cbc(key, iv, new_ct)
    #except:
    #    return (0,ct.hex(),new_ct.hex()+" w="+str(len(w)),"")
    #if new_msg == secret_msg:
    #    return (1, ct.hex(),eng,"")
    #else:
    #    return (2,ct.hex(),new_ct.hex()+" w="+str(len(w)),new_msg)





if __name__ == "__main__":
    arglist = sys.argv[1:]
    if len(arglist) == 0:
        print("Usage: python e2e_encryptor.py -l [coding range] -s [first phrase]")
        print("add -a opt to include iv in the overall ciphertext")
        exit(0)
    options="l:s:a"
    long_options=["range","seed","iv"]
    arguments, values = getopt.getopt(arglist, options, long_options)
    add_iv = False
    for curarg, curval in arguments:
        if curarg == "-l":
            my_l = int(curval)
        if curarg == "-s":
            seed = curval
        if curarg == "-a":
            add_iv = True
    print("coding range = "+str(my_l))
    print("first phrase = "+seed)
    print("iv  included = "+str(add_iv))
    print()
    msg = input("Type your secret message:")
    run_encryption(msg, my_l, seed, include_iv = add_iv)
