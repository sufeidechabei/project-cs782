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


def run_encryption(secret_msg, my_l, initial_seed, include_iv = False):

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
    initial_seed = util.pad(initial_seed)
    de = de_gpt2.GPT2ArthmDecoder(l=my_l, code = code, seed=initial_seed, toker=toker, model=model)
    t3 = time.perf_counter()
    print(f"Arithmatic decoder intialization took {t3 - t2:0.4f} s")
    print()
    print("===================== Generated English Sentence ========================")
    T = de.decode()
    print("=========================================================================")
    t4 = time.perf_counter()
    all_T = [initial_seed] + T
    print(f"\nDecoding the cipher text took {t4 - t3:0.4f} s")
    eng = "".join(all_T)
    re_T = util.tokenize(eng, toker, model)
    print()
    print("Can be uniquely Tokenized? ",end="",flush=True)
    if (re_T != all_T):
        print(colored('No! Here are there contents:', 'red'))
        print(re_T)
        print()
        print(all_T)
    else:
        print(colored('Yes it can!','green'))





if __name__ == "__main__":
    arglist = sys.argv[1:]
    if len(arglist) == 0:
        print("To be more specified, run ./e2e_encryptor.py -l [coding range (32 as default)] -s [first word]")
    print()
    options="l:s:a"
    long_options=["range","seed","iv"]
    arguments, values = getopt.getopt(arglist, options, long_options)
    add_iv = False
    seed = None
    rand_seed = False
    my_l = 32
    for curarg, curval in arguments:
        if curarg == "-l":
            my_l = int(curval)
        if curarg == "-s":
            seed = curval
        if curarg == "-a":
            add_iv = True
    if seed is None:
        seed = util.sample_seed()
        rand_seed = True
        print("No first word provided. Randomly using one of ours.")
    print("coding range= "+str(my_l))
    print("first  word = "+seed)
    print()
    msg = input("Type your secret message:")
    while(1):
        run_encryption(msg, my_l, seed, include_iv = True)
        stop = input("\nPress enter to regenerate or type anything to exit:")
        if len(stop) > 0:
            break
        if rand_seed:
            seed = util.sample_seed()
            print("\nUsing a new first word = "+seed+" \n")
           
