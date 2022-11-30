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


def bin32(x):
    return bin(x)[2:].zfill(32)

def bin8(x):
    l = util.coding_parameters["symbol_length"]
    return bin(x)[2:].zfill(l)

def print_D(str, D):
    print(str+" D =", end="")
    for s in D:
        print(" "+bin8(s), end="")
    print()

def print_D2(str, D):
    print(str+" D =", end="")
    for s in D:
        print(""+bin8(s), end="")
    print()

def encode_paper_retry(list_tokens, model_name = None):
    """ Retry implementing the encoer """
    r = util.coding_parameters["symbol_length"]
    l = util.coding_parameters["coding_length"]
    w = 0
    a = 0
    b = 1 << (r*l)
    D = []
    print("a = "+bin32(a)+" b = "+bin32(b))
    for token in list_tokens:
        print()
        print()
        print("Processing token '"+token+"' ================================================================")
        a,b = util.Adjust(model_name, token, a, b)
        while(1):
            print("a = "+bin32(a)+" b = "+bin32(b) + " are the lower and upper bound at the beginning of this loop")
            adf = util.double_floor_op(a, r*l, r*l-1)
            bdf = util.double_floor_op(b, r*l, r*l-1)
            if w > 0 and adf == bdf:
                print("we are doing the first IF with w = "+str(w)+" adf = bdf = "+bin32(adf))
                print_D("    before, we have", D)
                D[-w] = D[-w] + adf
                for i in range(1, w):
                    D[-i] = not D[-i]
                print_D("    after,  we have", D)
                w = 0
                xor_val = 1 << (r*l-1)
                a = a ^ xor_val
                b = b ^ xor_val
                print("    and now a = "+bin32(a)+" b = "+bin32(b))
            cmp_val = 1 << (r*(l-1))
            if b - a < cmp_val:
                print("b-a = "+bin32(b-a)+" < "+bin32(cmp_val)+" entering second IF")
                A = util.double_floor_op(a, r*l, r*(l-1))
                print("    Adding A = "+bin8(A)+" to D")
                D.append(A)
                print_D("    now we have", D)
                a = util.double_ceil_op(a, r*l, r)
                b = util.double_ceil_op(b, r*l, r)
                dfb2 = util.double_floor_op(b, r*l, r*(l-1))
                print("    changed to a = "+bin32(a)+" b = "+bin32(b)+" and we have dfb2 = "+bin8(dfb2))
                if A != dfb2:
                    print("        A is not the same as dfb2, entering the inner IF")
                    xor_val = 1 << (r*l-1)
                    a = a ^ xor_val
                    b = b ^ xor_val
                    w = w + 1
                    print("        changed to a = "+bin32(a)+" b = "+bin32(b)+" and increment w to "+str(w))
            if (b - a > cmp_val):
                print("b-a = "+bin32(b-a)+" > "+bin32(cmp_val)+" existing loop....")
                break
            #input()
    return D,w
                
def test_retry():
    tlist = ["I","really","eat","meat"]
    D,w = encode_paper_retry(tlist)
    print("\n$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$\nFinal Result:")
    print_D2("", D)
    print("w = "+str(w))





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
        while b < half or a > half:
            if b < half:
                EMIT.append('0')
                for i in range(0,s):
                    EMIT.append('1')
                s = 0
                a = 2 * a
                b = 2 * b
            elif a > half:
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
    test_retry()
    tlist = ["I","really","eat","meat"]
    #tlist2 = ["I","really","eat","hello","what","I","eat","impossible","secret","meat"]
    #D = encode_ytb(tlist)
    #print("finally")
    #for n in D:
    #    print(bin(n)[2:], end=" ")
    #print(w)
    r1 = encode_ytb(tlist)
    print("First  emit : "+"".join(r1))
    #print()
    #r2 = encode(tlist2)
    #print("Second emit : "+"".join(r2))
    #print("================")
    #r1 = encode_ytb(tlist)
    #print("First  emit : "+"".join(r1))
    #print()
    #r2 = encode_ytb(tlist2)
    #print("Second emit : "+"".join(r2))

