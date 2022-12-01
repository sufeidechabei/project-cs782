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


def run_encryption(data_pack, secret_msg, my_l, first_phrase, toker, model):

    key = crypto.obtain_key("e2e")
    iv, ct = crypto.encrypt_aes_cbc(key, secret_msg)
    code = iv+ct

    de = de_gpt2.GPT2ArthmDecoder(l=my_l, code = code, seed=first_phrase, toker=toker, model=model)
    T = de.decode()
    all_T = [first_phrase] + T
    eng = "".join(all_T)
    parsed_seed, re_T = util.tokenize(eng, toker, model)
    tokenizable = re_T == T and parsed_seed == first_phrase
    data = (code.hex(), len(all_T), len(eng), tokenizable)
    data_pack.append(data)
    print("done...",end="",flush=True)




def run_ct_itself_experiment():
    """ I want to know if ct itself has anything to do with the length of the output"""
    toker, model = initialize_GPT2()
    data_pack = []
    for i in range(0,20):
        seed = "If"
        try:
            run_encryption(data_pack,"UW-Madison", 32, seed, toker, model)
        except:
            print("oops...",end="",flush=True)
            continue
    print("All done!!!")
    sorted_data_pack = sorted(data_pack, key = lambda x: x[1])
    for data in sorted_data_pack:
        print(data[0] + "\t"+"#tokens: "+str(data[1])+"\tmsg length = "+str(data[2])+"\t"+str(data[3]))


    sorted_data_pack = sorted(data_pack, key = lambda x: x[0])
    for data in sorted_data_pack:
        print(data[0] + "\t"+"#tokens: "+str(data[1])+"\tmsg length = "+str(data[2])+"\t"+str(data[3]))
 
    return data_pack


if __name__ == "__main__":
    run_ct_itself_experiment()
