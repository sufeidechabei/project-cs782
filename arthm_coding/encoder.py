"""Arithmatic Encoding functions"""
import util as util
import model as model

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
    print(str(a/bb)+","+str(b/bb))
    for token in list_tokens:
        a, b = util.Adjust(model_name, token, a, b)
        print(str(a/bb)+","+str(b/bb))
        a, b, _, w = util.Rescale(D, w, a, b)
        #s = model.next_seed(#TODO
        print(token+":", end="")
        for n in D:
            print(bin(n)[2:], end=" ")
        print()
    return D, w 


if __name__ == "__main__":
    tlist = ["I","really","eat","meat"]
    D,w = encode_basic(tlist)
    print("finally")
    for n in D:
        print(bin(n)[2:], end=" ")
    print(w)


