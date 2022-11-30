# next_word_test.py

import torch
from transformers import AutoModelForCausalLM, \
  AutoTokenizer
# from torch import nn
import numpy as np

print("\nBegin next-word using HF GPT-2 demo ")

toker = AutoTokenizer.from_pretrained("gpt2")
model = AutoModelForCausalLM.from_pretrained("gpt2")

seq = "Machine learning with PyTorch can do amazing"
print("\nInput sequence: ")
print(seq)

inpts = toker(seq, return_tensors="pt")
print("\nTokenized input data structure: ")
print(inpts)

inpt_ids = inpts["input_ids"]  # just IDS, no attn mask
print("\nToken IDs and their words: ")
for id in inpt_ids[0]:
  word = toker.decode(id)
  print(id, word)

with torch.no_grad():
  logits = model(**inpts).logits[:, -1, :]
print("\nAll logits for next word: ")
print(logits)
print(logits.shape)

pred_id = torch.argmax(logits).item()
print("\nPredicted token ID of next word: ")
print(pred_id)

print("###################")
tensor_vals = logits.topk(10).values.tolist()[0]
token_indices = logits.topk(10).indices.tolist()[0]
my_probs = []
my_probs_real = []
my_tokens = []
summer = 0
for val in tensor_vals:
    p = -100/val
    my_probs.append(p)
    summer = summer + p
for probs in my_probs:
    real_prob = probs / summer
    my_probs_real.append(real_prob)

for index in token_indices:
    my_tokens.append("("+toker.decode(index)+")")

for i in range(0,len(my_tokens)):
    print("P"+my_tokens[i]+"\t=\t"+str(my_probs_real[i]))

print("###################")


pred_word = toker.decode(pred_id)
print("\nPredicted next word for sequence: ")
print(pred_word)

print("\nEnd demo ")

