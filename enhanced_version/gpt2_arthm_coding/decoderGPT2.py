"""Arithmatic Encoding functions"""
try:
    import gpt2_arthm_coding.gpt2model as gpt2modellib
except ModuleNotFoundError as e:
    import gpt2model as gpt2modellib

from termcolor import colored

import math as math
import random as rng

class GPT2ArthmDecoder:

    def __init__(self, l=4, r=8, code=None, seed="I think", toker=None, model=None):
        self.r = r
        self.l = l
        self.w = [] # The D? No. The w
        self.a = 0
        self.b = 1 << (self.r * self.l)
        self.magic_num = 0x80
        self.C = code
        self.C_cursor = l
        self.c_padding = 1
        self.M = gpt2modellib.GPT2Model(first_phrase=seed, toker=toker, model=model)
        self.seed = seed
        if code is None:
            exit(1)
        self.c = int.from_bytes(code[:self.l], byteorder='big', signed=False)


    def target_frequency(self):
        diff1 = self.c - self.a
        diff2 = self.b - self.a
        return diff1 / diff2
        

    def adjust(self, token):
        cumu, relative = self.M.GetFreq(token)
        diff = self.b - self.a
        self.b = self.a + math.floor((cumu + relative) * diff)
        self.a = self.a + math.floor(cumu * diff)
        
    def invert_range(self):
        mask = 1 << self.l * self.r - 1
        self.a = self.a ^ mask
        self.b = self.b ^ mask
        if self.c is not None:
            self.c = self.c ^ mask


    def decode(self):
        """ Follow their written version and pseudo-code in blend """
        D = []
        T = []
        print(self.seed[1:],end="",flush=True)
        while (True):
            assert self.c < self.b # for future checks
            tfreq = self.target_frequency()
            token = self.M.GetToken(tfreq)
            T.append(token)
            self.adjust(token)
            shift_amount = self.r*self.l - 1
            dbf_a = self.a >>  shift_amount
            dbf_b = self.b-1 >> shift_amount
            if len(self.w) > 0 and dbf_a == dbf_b:
                D.append(self.w[0] + dbf_a)
                for n in self.w[1:]:
                    D.append(n + dbf_a ^ self.magic_num)
                self.w = []
                self.invert_range()
            bb = 1 << (self.r * self.l)
            break_flag = False
            # TODO Insert timer for this part and for encoder
            while self.b - self.a <= bb >> 9: #why 9? is it self.r + 1?
                symbol = self.a >> (self.r * self.l - self.r)
                self.a = (self.a << self.r) % bb
                self.b = (self.b << self.r) % bb
                if self.b == 0:
                    self.b = bb
                # process c
                if self.c is not None:
                    self.c = (self.c << self.r) % bb
                    if self.C_cursor < len(self.C):
                        next_byte = self.C[self.C_cursor]
                        self.C_cursor = self.C_cursor + 1
                        self.c = self.c + next_byte
                    else:
                        self.c = self.c + rng.randint(0,255)
                if self.a > self.b:
                    self.w.append(symbol)
                    self.invert_range()
                else:
                    D.append(symbol)

            self.M.next(token)

            if len(D) > len(self.C):
                print(colored(token,'yellow'),end="",flush=True)
            else:
                print(token,end="",flush=True)
            if len(D) >= len(self.C) and (token[0] == '.' or token[0] == '?' or token[0] == '!'):
                print()
                break
        return T
                    
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
        print(""+hex(s)[2:], end="")
    print()



if __name__ == "__main__":
    #sentence = "David kicks candle when Charles finds watch if John eats chocolate and Richard gets candle since Barbara makes keys"
    #ct = "3c33e0cd41363e59"
    ct = "cafef00d15deadbeef"
    code = bytes.fromhex(ct)
    de = PaperArthmDecoder(code = code)
    T = de.decode("english")
    for t in T:
        print(t,end=" ")
