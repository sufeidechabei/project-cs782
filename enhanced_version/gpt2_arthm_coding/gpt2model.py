import torch
from transformers import AutoModelForCausalLM, \
  AutoTokenizer
# from torch import nn
import numpy as np


def my_normalizer(tensor_vals):
    z = np.array(tensor_vals)
    beta = 1.0
    zz = z / beta
    return list(np.exp(zz)/sum(np.exp(zz)))

def should_ignore(token):
    igs = ['\n','"','(',')','<|endoftext|>']
    for ig in igs:
        if ig in token:
            return True
    return False

class GPT2Model:
    

    def __init__(self, first_phrase="I think", toker = None, model = None):
        # GPT-2 and Pytorch params
        self.toker = toker
        self.model = model
        # Our model specific
        self.k_value = 3000
        self.initial_seed = first_phrase
        self.current_seed = self.initial_seed
        self.current_token_distro = []
        # Initialize to get the first token.
        self.next()

    def next(self,token=None):
        # update seed if needed
        if token is not None:
            self.current_seed = self.current_seed + token
        # start generation
        inpts = self.toker(self.current_seed, return_tensors="pt")
        with torch.no_grad():
            logits = self.model(**inpts).logits[:, -1, :]
        # logitis generated. now we can start calcualte the probabilities.
        # firstly normalie the tensor vals
        tensor_vals = logits.topk(self.k_value).values.tolist()[0]
        # now get the tokens list
        token_indices = logits.topk(self.k_value).indices.tolist()[0]
        tokens_list = []
        for index in token_indices:
            tokens_list.append(self.toker.decode(index))
        # prune the ignored ones
        normalized_sum = 0
        tmp_t = []
        tmp_v = []
        for i in range(0,len(tokens_list)):
            if not should_ignore(tokens_list[i]):
                tmp_t.append(tokens_list[i])
                tmp_v.append(tensor_vals[i])
        normalized_vals = my_normalizer(tmp_v)
        tokens_list = tmp_t
        for v in normalized_vals:
            normalized_sum += v
        # now the probabilities
        self.current_token_distro = []
        current_cumu = 0
        for i in range(0, len(tokens_list)):
            token = tokens_list[i]
            cumu_freq = current_cumu / normalized_sum
            rela_freq = normalized_vals[i] / normalized_sum
            self.current_token_distro.append((token, cumu_freq, rela_freq))
            current_cumu += normalized_vals[i]
        


    def GetToken(self, freq):
        for distro in self.current_token_distro:
            if distro[1] + distro[2] >= freq: # [1] is cumu, [2] is rela
                return distro[0]


    def GetFreq(self, token):
        for distro in self.current_token_distro:
            if distro[0] == token:
                cumu = distro[1]
                rela = distro[2]
                return (cumu, rela)




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
        















