import torch
from transformers import AutoModelForCausalLM, \
  AutoTokenizer
# from torch import nn
import numpy as np

def tokenize(eng):
    toker = AutoTokenizer.from_pretrained("gpt2")
    model = AutoModelForCausalLM.from_pretrained("gpt2")
    inpts = toker(eng, return_tensors="pt")
    inpt_ids = inpts["input_ids"]
    tokens = []
    for tid in inpt_ids[0]:
        word = toker.decode(tid)
        tokens.append(word)
    return tokens


