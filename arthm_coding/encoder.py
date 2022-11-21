"""Arithmatic Encoding functions"""
try:
    import arthm_coding.util as util
    import arthm_coding.model as model
except ModuleNotFoundError as e:
    import util as util
    import model as model
import math as math


def encode_basic(list_tokens, model_name=None):
    """ basic encoder"""
    r = util.coding_parameters["symbol_length"]
    l = util.coding_parameters["coding_length"]
    w = 0 # ???
    a = 0 # Lower bound of the interval
    b = 1 << (r*l) # upper bound of the interval
    D = [] # ??? TODO
    #s = model.get_first_seed()
   
    bb = b
    #print(str(a/bb)+","+str(b/bb))
    for token in list_tokens:
        a, b = util.Adjust(model_name, token, a, b)
        #print(str(a/bb)+","+str(b/bb))
        a, b, _, w = util.Rescale(D, w, a, b)
        #s = model.next_seed(#TODO
        #print(token+":", end="")
        #for n in D:
            #print(bin(n)[2:], end=" ")
        #print()
    DD = []
    for d in D:
        DD.append(bin(d)[2:])
    return DD #, w


def encode_ytb(list_tokens, model_name = None):
    """Following ytb's algorithm"""
    preci = util.coding_parameters["precision2"]
    whole = 1 << preci
    half = whole / 2
    quarter = whole / 4
    EMIT = []
    a = 0
    b = 1 << preci
    s = 0
    for token in list_tokens:
        a, b = util.Adjust(model_name, token, a, b) #we can still use the Adjust function
        while b <= half or a >= half:
            if b <= half:
                EMIT.append('0')
                for i in range(0,s):
                    EMIT.append('1')
                s = 0
                a = 2 * a
                b = 2 * b
            elif a >= half:
                EMIT.append('1')
                for i in range(0,s):
                    EMIT.append('0')
                s = 0
                a = 2 * (a-half)
                b = 2 * (b-half)
            #print("curr  emit : "+"".join(EMIT))
        while a > quarter and b < 3 * quarter:
            s = s + 1
            a = 2 * (a - quarter)
            b = 2 * (b - quarter)
    s = s + 1
    if a < quarter:
        EMIT.append('0')
        for i in range(0,s):
            EMIT.append('1')
    else:
        EMIT.append('1')
        for i in range(0,s):
            EMIT.append('0')
    #print("-------------------------")
    #print("Final emit : "+"".join(EMIT))
    return EMIT




def encode(list_tokens, model_name = None):
    """interface"""
    return encode_basic(list_tokens, model_name)


if __name__ == "__main__":
    tlist = ["I","really","eat","meat"]
    tlist2 = ["I","really","eat","hello","what","I","eat","impossible","secret","meat"]
    #D,w = encode_basic(tlist)
    #print("finally")
    #for n in D:
    #    print(bin(n)[2:], end=" ")
    #print(w)
    #r1 = encode(tlist)
    #print("First  emit : "+"".join(r1))
    #print()
    #r2 = encode(tlist2)
    #print("Second emit : "+"".join(r2))
    #print("================")
    r1 = encode_ytb(tlist)
    print("First  emit : "+"".join(r1))
    print()
    r2 = encode_ytb(tlist2)
    print("Second emit : "+"".join(r2))

