#!/usr/bin/env python3
""" English-to-English(E2E) Decryption Tool """
import binascii as binascii

import crypto.util as crypto
import gpt2_arthm_coding.encoderGPT2 as en_gpt2
import gpt2_arthm_coding.decoderGPT2 as de_gpt2

import e2e_util as util

import time

import getopt
import sys

import torch
from transformers import AutoModelForCausalLM, \
  AutoTokenizer


from datetime import datetime

def initialize_GPT2():
    toker = AutoTokenizer.from_pretrained("gpt2")
    model = AutoModelForCausalLM.from_pretrained("gpt2")
    return toker, model


def run_decryption(eng, my_l, given_iv=None):
    t0 = time.perf_counter()
    toker, model = initialize_GPT2()
    print()
    t1 = time.perf_counter()
    print(f"GPT-2 toker and model took {t1 - t0:0.4f} s to initialize.");
    t4 = time.perf_counter()
    eng = util.pad(eng)
    all_tokens = util.tokenize(eng, toker, model)
    print("Tokens = "+str(all_tokens))

    en = en_gpt2.GPT2ArthmEncoder(l=my_l, seed=all_tokens[0], toker=toker, model=model)
    t5 = time.perf_counter()
    print(f"\nParsing & Encoder intialization took {t5 - t4:0.4f} s")
    D, w = en.encode(all_tokens[1:])
    t6 = time.perf_counter()
    print(f"Encoding generated sentences took {t6 - t5:0.4f} s")
    new_encoded = bytes(D)
    new_iv, new_ct = util.extract_iv_ct(new_encoded) 
    key = crypto.obtain_key("e2e")
    success = False
    print()
    print("Obtained iv="+new_iv.hex())
    print("Obtained ct="+new_ct.hex())
    print()
    try:
        new_msg = crypto.decrypt_aes_cbc(key, new_iv, new_ct)
    except:
        print("Decryption FAILED")
        exit(1)
    print()
    print("===========================  Secret Message  ============================")
    print(new_msg)
    print("=========================================================================")

if __name__ == "__main__":
    arglist = sys.argv[1:]
    if len(arglist) == 0:
        print("To be more specified, run ./e2e_decryptor.py -l [coding range (32 as default)]")
    print()
    options="l:s:a"
    long_options=["range","seed","iv"]
    arguments, values = getopt.getopt(arglist, options, long_options)
    add_iv = False
    my_l = 32
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
        
