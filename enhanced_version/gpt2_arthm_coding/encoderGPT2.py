"""Arithmatic Encoding functions"""
try:
    import gpt2_arthm_coding.gpt2model as gpt2modellib
except ModuleNotFoundError as e:
    import gpt2model as gpt2modellib

import math as math


class GPT2ArthmEncoder:

    def __init__(self, l=4, r=8, seed="I think", toker=None, model=None):
        self.r = r
        self.l = l
        self.w = [] # The D? No. The w
        self.a = 0
        self.b = 1 << (self.r * self.l)
        self.magic_num = 0x80
        self.M = gpt2modellib.GPT2Model(first_phrase=seed, toker=toker, model=model)

    def adjust(self, token):
        cumu, relative = self.M.GetFreq(token)
        diff = self.b - self.a
        self.b = self.a + math.floor((cumu + relative) * diff)
        self.a = self.a + math.floor(cumu * diff)
        
    def invert_range(self):
        mask = 1 << self.l * self.r - 1
        self.a = self.a ^ mask
        self.b = self.b ^ mask


    def encode(self, token_list):
        """ Follow their written version and pseudo-code in blend """
        D = []
        print("\nEncoding",end="",flush=True)
        for token in token_list:
            print(".",end="",flush=True)
            self.adjust(token)
            dbf_a = self.a >> self.r*self.l-1
            dbf_b = self.b - 1 >> self.r*self.l-1
            if len(self.w) > 0 and dbf_a == dbf_b:
                D.append(self.w[0] + dbf_a)
                for n in self.w[1:]:
                    D.append(n + dbf_a ^ self.magic_num)
                self.w = []
                self.invert_range()
            bb = 1 << (self.r * self.l)
            while self.b - self.a <= bb >> 9: #why 9? is it self.r + 1?
                symbol = (self.a % bb) >> (self.r * self.l - self.r)
                self.a = (self.a << self.r) % bb
                self.b = (self.b << self.r) % bb
                if self.b == 0:
                    self.b = bb
                if self.a > self.b:
                    self.w.append(symbol)
                    self.invert_range()
                else:
                    D.append(symbol)
            self.M.next(token)
        print()
        print()
        return D, self.w
                    
def bin32(x):
    return bin(x)[2:].zfill(32)

def bin8(x):
    l = 8
    return bin(x)[2:].zfill(l)

def print_D(str, D):
    print(str+" D =", end="")
    for s in D:
        print(" "+bin8(s), end="")
    print()

def print_D2(str, D):
    print(str+" D = ", end="")
    for s in D:
        print(""+hex(s)[2:].zfill(2), end="")
    print()



if __name__ == "__main__":
    #sentence = "David kicks candle when Charles finds watch if John eats chocolate and Richard gets candle since Barbara makes keys"
    #sentence = "Barbara wants toothpaste but Patricia eats hairband since John uses toothpaste although John kicks house since William finds glasses when James checks watch"
    sentence = "Barbara wants toothpaste but Patricia eats hairband since John uses toothpaste although John kicks house since William finds glasses when James checks spoon"
    tokens = sentence.split()
    en = PaperArthmEncoder()
    D, w = en.encode(tokens, "english")
    print_D2("", D)
    print(len(w))
