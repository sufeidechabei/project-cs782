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
    t1 = time.perf_counter()
    key = crypto.obtain_key("e2e")
    iv, ct = crypto.encrypt_aes_cbc(key, secret_msg)
    t2 = time.perf_counter()

    if include_iv:
        code = iv+ct
    else:
        code = ct
    initial_seed = util.pad(initial_seed)
    de = de_gpt2.GPT2ArthmDecoder(l=my_l, code = code, seed=initial_seed, toker=toker, model=model)
    t3 = time.perf_counter()
    T = de.decode()
    t4 = time.perf_counter()
    all_T = [initial_seed] + T
    eng = "".join(all_T)
    re_T = util.tokenize(eng, toker, model)
    if (re_T != all_T):
        print(colored('No! Here are there contents:', 'red'))
    else:
        print(colored('Yes it can!','green'))
    print()
    return eng




if __name__ == "__main__":
    arglist = sys.argv[1:]
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
    msg = input("Type your secret message:")
    while(1):
        eng = run_encryption(msg, my_l, seed, include_iv = True)
        print("\nGenerated="+eng)
        stop = input("\nPress enter to regenerate or type anything to exit:")
        if len(stop) > 0:
            break
        if rand_seed:
            seed = util.sample_seed()
           
