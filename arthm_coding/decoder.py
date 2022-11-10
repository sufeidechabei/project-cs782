"""Arithmatic Decoding functions"""
import .util as util


def decode_basic(input_cipher_text, model):
    """ basic decoder"""
    r = util.coding_parameters["symbol_length"]
    l = util.coding_parameters["coding_length"]
    w = 0 # ???
    a = 0 # Lower bound of the interval
    b = 1 << (r*l) # upper bound of the interval
    D = "" # ??? TODO
    C = #TODO (truncated input cipher text?)
    generated_sentence = "" # Should be the container for the token.
    s = model.get_first_seed()

    while(#TODO):
        token = util.GetToken(#TODO)
        generated_sentence += " "+token
        a,b = util.Adjust(#TODO)
        Rescale(#TODO)
        s = model.next_seed(#TODO

    return generated_sentence

