"""Arithmatic Encoding functions"""
import .util as util


def encode_basic(list_tokens, model):
    """ basic encoder"""
    r = util.coding_parameters["symbol_length"]
    l = util.coding_parameters["coding_length"]
    w = 0 # ???
    a = 0 # Lower bound of the interval
    b = 1 << (r*l) # upper bound of the interval
    D = "" # ??? TODO
    s = model.get_first_seed()
    
    for token in list_tokens:
        a, b = util.Adjust(#TODO)
        Rescale(#TODO)
        s = model.next_seed(#TODO

    return D, w 


