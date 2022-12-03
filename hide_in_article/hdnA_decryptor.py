#!/usr/bin/env python3
""" English-to-English(E2E) Decryption Tool """
import binascii as binascii

import crypto.util as crypto
import gpt2_arthm_coding.encoderGPT2 as en_gpt2
import gpt2_arthm_coding.decoderGPT2 as de_gpt2

import e2e_util as util

from termcolor import colored

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
    print("Parsed out "+str(len(all_tokens))+" Tokens")

    #Try to find the header
    seed_candidate_tokens = []
    seed_candidate = ""
    remaining_tokens = []
    chunk_num = None
    print("\n\n____________________  Step 1: header searching  ____________________")
    for index in range(0, len(all_tokens)):
         t = all_tokens[index]
         seed_candidate_tokens.append(t)
         if t == "." or t == "?" or t == "!":
             # we now have a seed candidate
             seed_candidate = "".join(seed_candidate_tokens)
             print("\nseed candidate = '"+seed_candidate+"'")
             if not (index + 1 < len(all_tokens)):
                 print("Exahusted!! Aborting")
                 exit(1)
             remaining_tokens =  all_tokens[index+1:]
             try:
                extracted_header_bytes = en_gpt2.GPT2ArthmEncoder.encode_partial(my_l, remaining_tokens, seed_candidate, toker, model)
             except:
                 print("] ",end="")
                 print(colored(" Cannot be extracted","red"))
                 seed_candidate_tokens = []
                 continue
             chunk_num = crypto.check_header(bytes(extracted_header_bytes), seed_candidate)
             if chunk_num is not None:
                 break;
             else:
                 seed_candidate_tokens = []
             
    en = en_gpt2.GPT2ArthmEncoder(l=my_l, seed=seed_candidate, toker=toker, model=model)
    t5 = time.perf_counter()
    print(f"\nIntialization and searching took {t5 - t4:0.4f} s")
    print("\n\n____________________  Step 2: decrypt the secret  __________________")
    D, _ = en.encode(remaining_tokens, 32 + chunk_num * 16)
    D_ct = D[32:]
    t6 = time.perf_counter()
    print(f"Encoding generated sentences took {t6 - t5:0.4f} s")
    new_encoded = bytes(D_ct)
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
        print("To be more specified, run ./hdnA_decryptor.py -l [coding range (32 as default)] -f [file to replace manual input]")
    print()
    options="f:l:s:a"
    long_options=["range","seed","iv"]
    arguments, values = getopt.getopt(arglist, options, long_options)
    my_l = 32
    file_loc = None
    for curarg, curval in arguments:
        if curarg == "-l":
            my_l = int(curval)
        if curarg == "-f":
            file_loc = curval
    print("coding range = "+str(my_l))
    print()
    msg = ""
    if file_loc is None:
        msg = input("Enter the passage you found:")
    else:
        with open(file_loc, "r") as f:
            msg = f.read()
    run_decryption(msg, my_l)
        
