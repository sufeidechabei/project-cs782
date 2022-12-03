#!/usr/bin/env python3
""" English-to-English(E2E) Encryption Tool for hiding text in the middle of an article """
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

def initial_seed_check(seed):
    p = seed[-1]
    if p != '.' and p != '!' and p != '?':
        print(colored("!!!! INVALID seed for this tool. It must be a sentence with . or ! or ? as the ending", 'red'))
        exit(1)


def run_encryption(secret_msg, my_l, initial_seed):
    initial_seed_check(initial_seed)
    initial_seed = util.pad(initial_seed)
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

    pre_header_code = iv+ct
    # calculate the length of actual ct and put them in the header
    assert len(pre_header_code) % 16 == 0
    chunk_num = len(pre_header_code) // 16
    print()
    code_header = crypto.produce_header(initial_seed, chunk_num)
    code = code_header + pre_header_code
 

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
    all_T_2 = util.tokenize(initial_seed, toker, model) + T
    print()
    print("Can be uniquely Tokenized? ",end="",flush=True)
    if (re_T != all_T_2):
        print(colored('No! Here are there contents:', 'red'))
        print(re_T)
        print()
        print(all_T_2)
    else:
        print(colored('Yes it can!','green'))
    return eng[1:]





if __name__ == "__main__":
    arglist = sys.argv[1:]
    if len(arglist) == 0:
        print("To be more specified, run ./hdnA_encryptor.py -l [coding range (32 as default)] -s [first full sentence] -f [file to save the output]")
    print()
    options="f:l:s:a"
    long_options=["range","seed","iv"]
    arguments, values = getopt.getopt(arglist, options, long_options)
    seed = None
    rand_seed = False
    my_l = 32
    file_loc = None
    for curarg, curval in arguments:
        if curarg == "-l":
            my_l = int(curval)
        if curarg == "-s":
            seed = curval
        if curarg == "-f":
            file_loc = curval
    if seed is None:
        print("No first sentence provided! Exiting......")
        exit(1)
    print("coding range= "+str(my_l))
    print("first  sentence = "+seed)
    print()
    msg = input("Type your secret message:")
    while(1):
        result = run_encryption(msg, my_l, seed)
        if file_loc is not None:
            with open(file_loc, 'w+') as f:
                f.write(result)
            print("Saved generated sentence to "+file_loc)
        stop = input("\nPress enter to regenerate or type anything to exit:")
        if len(stop) > 0:
            break
        if rand_seed:
            seed = util.sample_seed()
            print("\nUsing a new first word = "+seed+" \n")
           
