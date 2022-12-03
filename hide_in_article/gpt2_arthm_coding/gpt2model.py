import torch
from transformers import AutoModelForCausalLM, \
  AutoTokenizer
# from torch import nn
import numpy as np

from collections import OrderedDict

from termcolor import colored

import time

def my_normalizer(tensor_vals):
    z = np.array(tensor_vals)
    beta = 1.0
    zz = z / beta
    return list(np.exp(zz)/sum(np.exp(zz)))

def should_ignore(token):
    igs = ['\n','"','(',')','<|endoftext|>','[',']','{','}']
    for ig in igs:
        if ig in token:
            return True
    return False

class GPT2Model:
    

    def __init__(self, first_phrase="I think", toker = None, model = None):
        self.seed_update_mode = 1 # 0 for original, 1 for new
        self.time_advancement = False
        # GPT-2 and Pytorch params
        self.toker = toker
        self.model = model
        # Our model specific
        self.k_value = 3000
        self.initial_seed = first_phrase
        self.current_seed = self.initial_seed
        self.current_token_distro = OrderedDict()
        # parameters for advanced seeding
        self.seed_rotater = ["","","",""]
        self.rotater_cursor = 0
        # Initialize to get the first token.
        self.next()

    def update_seed_original(self, token):
        if token is None:
            return
        self.current_seed = self.current_seed + token

    def see_distro(self):
        return self.current_token_distro

    def update_seed_advanced(self, token):
        if token is None:
            # first iteration. for hide in article, current seed must end in period.
            # following up seeds must append to the next array
            self.seed_rotater[0] = self.current_seed
            self.rotater_cursor += 1
        else:
            # append to which ever we are rotating
            self.seed_rotater[self.rotater_cursor] = self.seed_rotater[self.rotater_cursor] + token
            if token == '.' or token == '?' or token == '!':
                # current one in rotater is now a sentence, shift to the next one to append.
                self.rotater_cursor += 1
            if self.rotater_cursor >= len(self.seed_rotater):
                # oh, we have len(rotater) sentences now. start shifting back.
                for i in range(0, len(self.seed_rotater)-1):
                    self.seed_rotater[i] = self.seed_rotater[i+1]
                self.seed_rotater[-1] = ""
                self.rotater_cursor = len(self.seed_rotater) - 1
        self.current_seed = "".join(self.seed_rotater)
        #print(colored("\n"+self.current_seed, "cyan"),end="",flush=True)

    def next(self,token=None):
        # update seed if needed
        if self.seed_update_mode == 0:
            self.update_seed_original(token)
        else:
            self.update_seed_advanced(token)
        # start generation
        t0 = time.perf_counter()
        inpts = self.toker(self.current_seed, return_tensors="pt")
        with torch.no_grad():
            logits = self.model(**inpts).logits[:, -1, :]
        # logitis generated. now we can start calcualte the probabilities.
        tensor_vals = logits.topk(self.k_value).values.tolist()[0]
        # now get the tokens list
        token_indices = logits.topk(self.k_value).indices.tolist()[0]
        t1 = time.perf_counter()
        t2 = time.perf_counter()
        tokens_list = []
        for index in token_indices:
            tokens_list.append(self.toker.decode(index))
        # prune the ignored ones
        normalized_sum = 0
        pruned_tokens = []
        pre_normalized_vals = []
        for i in range(0, len(tokens_list)):
            if (not should_ignore(tokens_list[i])) and (tokens_list[i] not in pruned_tokens):
                pruned_tokens.append(tokens_list[i])
                pre_normalized_vals.append(tensor_vals[i])
        normalized_vals = my_normalizer(pre_normalized_vals)
        for v in normalized_vals:
            normalized_sum += v
        # now the probabilities
        assert len(normalized_vals) == len(pruned_tokens)
        self.current_token_distro = OrderedDict()
        current_cumu = 0
        t3 = time.perf_counter()
        t4 = time.perf_counter()
        for i in range(0, len(pruned_tokens)):
            token = pruned_tokens[i]
            if (token in self.current_token_distro):
                continue
            cumu_freq = current_cumu / normalized_sum
            rela_freq = normalized_vals[i] / normalized_sum
            self.current_token_distro[token] = (cumu_freq, rela_freq)
            current_cumu += normalized_vals[i]
        t5 = time.perf_counter()
        if (self.time_advancement):
            print(f"\n[Timeing] Obtain={t1 - t0:0.4f}s\tPrep={t3 - t2:0.4f}s\tGen={t5 - t4:0.4f}s");



    def GetToken(self, freq):
        last_freq = 0
        for distro in self.current_token_distro:
            last_freq = self.current_token_distro[distro][0] + self.current_token_distro[distro][1]
            if last_freq >= freq: # [0] is cumu, [0] is rela
                return distro
        print("\n*** Getting token with frequency = "+str(freq)+" failed????   last distro = "+str(last_freq))


    def GetFreq(self, token):
        bundle = self.current_token_distro[token]
        return (bundle[0], bundle[1])



if __name__ == "__main__":
    M = GPT2Model()
    target_freq = 0.4
    sentence = "I think"
    print(sentence)
    while(True):
        t = M.GetToken(target_freq)
        sentence = sentence + t
        print(sentence)
        M.next(t)
        input()
        















