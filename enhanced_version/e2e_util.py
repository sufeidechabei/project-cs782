import torch
from transformers import AutoModelForCausalLM, \
  AutoTokenizer
# from torch import nn
import numpy as np

def tokenize(full_eng, toker, model):
    """Parse out the seed and the tokens from the provided english"""   
    bundle = full_eng.split(" ",1)
    seed = bundle[0]
    eng = " "+bundle[1]
    if seed[-1] == ",":
        eng = ","+eng
        seed = seed[:-1]
    inpts = toker(eng, return_tensors="pt")
    inpt_ids = inpts["input_ids"]
    tokens = []
    for tid in inpt_ids[0]:
        word = toker.decode(tid)
        tokens.append(word)
    return seed, tokens


