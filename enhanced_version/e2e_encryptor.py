#!/usr/bin/env python3
""" English-to-English(E2E) Encryption Tool """
import binascii as binascii
from termcolor import colored
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


def run_encryption(secret_msg, my_l, first_phrase, include_iv = False):

    t0 = time.perf_counter()
    toker, model = initialize_GPT2()
    print()
    t1 = time.perf_counter()
    print(f"GPT-2 toker and model took {t1 - t0:0.4f} s to initialize.");
    print("Start encryption for '"+secret_msg+"'\n")
    key = crypto.obtain_key("e2e")
    iv, ct = crypto.encrypt_aes_cbc(key, secret_msg)
    t2 = time.perf_counter()
    print(f"AES encryption took {t2 - t1:0.4f} s")
    print("Generated ciphertext="+ct.hex()+"  iv="+iv.hex())

    if include_iv:
        code = iv+ct
    else:
        code = ct

    de = de_gpt2.GPT2ArthmDecoder(l=my_l, code = code, seed=first_phrase, toker=toker, model=model)
    t3 = time.perf_counter()
    print(f"Arithmatic decoder intialization took {t3 - t2:0.4f} s")
    print()
    print("===================== Generated English Sentence ========================")
    T = de.decode()
    print("=========================================================================")
    t4 = time.perf_counter()
    all_T = [first_phrase] + T
    print(f"\nDecoding the cipher text took {t4 - t3:0.4f} s")
    eng = "".join(all_T)
    parsed_seed, re_T = util.tokenize(eng, toker, model)
    print()
    print("Can be uniquely Tokenized? ",end="",flush=True)
    if (re_T != T):
        print(colored('No! Here are there contents:', 'red'))
        print(re_T)
        print()
        print(T)
    elif (parsed_seed != first_phrase):
        print(colored('No! tokens match but seeds do not match:', 'red'))
        print("real seed = "+first_phrase+"  but parsed seed = "+parsed_seed)
    else:
        print(colored('Yes it can!','green'))





if __name__ == "__main__":
    arglist = sys.argv[1:]
    if len(arglist) == 0:
        print("Usage: python e2e_encryptor.py -l [coding range] -s [first word]")
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
    print()
    msg = input("Type your secret message:")
    while(1):
        run_encryption(msg, my_l, seed, include_iv = True)
        stop = input("\nPress enter to regenerate, or give any char and exit:")
        if len(stop) > 0:
            break
        
