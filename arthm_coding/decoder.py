"""Arithmatic Decoding functions"""
import util as util
import model as model


def process_input_cipher_text(ct, mode=2)
    if mode = 2
        return int(ct, 2)
    return 0
    


def decode_basic(input_cipher_text, model_name=None):
    """ basic decoder"""
    r = util.coding_parameters["symbol_length"]
    l = util.coding_parameters["coding_length"]
    w = 0 # ??? TODO
    a = 0 # Lower bound of the interval
    b = (1 << (r*l)) # upper bound of the interval
    c = process_input_cipher_text(input_cipher_text)
    generated_sentence = "" #The "T" in pseudocode. Should be the container for the token.
    D = [] # ??? TODO  Use list of chars for mutability
    C = [*input_cipher_text]
    #s = model.get_first_seed() TODO

    while(#TODO):
        target_freq = (c-a)/(b-a) 
        token = model.GetToken(target_freq, model_name)
        generated_sentence += " "+token
        a,b = util.Adjust(model_name, token, a, b)
        w,a,b,c = util.Rescale(D, w, a, b, c, input_cipher_text)
        #s = model.next_seed(#TODO

    return generated_sentence

