""" Too Simple of a test """
import binascii as binascii

import crypto.util as crypto
import gpt2_arthm_coding.encoderGPT2 as en_gpt2
import gpt2_arthm_coding.decoderGPT2 as de_gpt2

import e2e_tokenizer as tknizer

import time

import getopt
import sys

from datetime import datetime


def parse_eng(eng):
   re_T = tknizer.tokenize(eng)
   print()
   seed = re_T[0]
   tokens = re_T[1:]
   print("Parsed  seed  = "+seed)
   print("Parsed T list = "+str(tokens))
   return seed, tokens

def run_decryption(eng, my_l, given_iv=None):
    t4 = time.perf_counter()
    first_phrase, tokens = parse_eng(eng)
    en = en_gpt2.GPT2ArthmEncoder(l=my_l, seed=first_phrase)
    t5 = time.perf_counter()
    print(f"\nParsing & Encoder intialization took {t5 - t4:0.4f} s")
    D, w = en.encode(tokens)
    t6 = time.perf_counter()
    print(f"Encoding generated sentences took {t6 - t5:0.4f} s")
    new_encoded = bytes(D)
    new_iv = new_encoded[:16]
    new_ct = new_encoded[16:]
 
    key = crypto.obtain_key("e2e")
    success = False
    print()
    print("Obtained iv="+new_iv.hex())
    print("Obtained ct="+new_ct.hex())
    print()
    while not success:
        try:
            new_msg = crypto.decrypt_aes_cbc(key, new_iv, new_ct)
            break
        except:
            if new_ct[-1] == 1:
                new_ct = new_ct[:-1]
                print("Last one failed. try this new ct="+new_ct.hex())
                continue
            print("Really failed this time")
            exit(1)
    print()
    print("===========================  Secret Message  ============================")
    print(new_msg)
    print("=========================================================================")

if __name__ == "__main__":
    arglist = sys.argv[1:]
    if len(arglist) == 0:
        print("Usage: python e2e_decryptor.py -l [coding range]")
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
    print()
    msg = input("Type the english sentence found:")
    run_decryption(msg, my_l)
        
