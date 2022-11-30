"""Arithmatic Decoding functions"""
try:
    import arthm_coding.util as util
    import arthm_coding.model as model
    import arthm_coding.encoder as encoder
except ModuleNotFoundError as e:
    import util as util
    import model as model
    import encoder as encoder

import time

def process_input_cipher_text(ct, mode=2):
    if mode == 2:
        return int("0b"+ct, 2)
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
    for i in range (0,len(C)):
        C[i] = int(C[i])
    #s = model.get_first_seed() TODO

    while(1):
        target_freq = (c-a)/(b-a) 
        token = model.GetToken(target_freq, model_name)
        generated_sentence += " "+token
        a,b = util.Adjust(model_name, token, a, b)
        a,b,c,w = util.Rescale(D, w, a, b, c, C)
        #s = model.next_seed(#TODO
        print(D)
        print(C)
        print(a)
        print(b)
        print(c)
        print(w)
        print("-------------------")
        if len(D) >= len(C):
            break

    return generated_sentence

debug_decoder = False

def dprint(s):
    if debug_decoder:
        print(s)
    

def decode_ytb(ct_str, model_name = None):
    """Following youtube decoder"""
    ct = [*ct_str]
    M = len(ct)
    preci = util.coding_parameters["precision2"]
    whole = 1 << preci
    half = whole / 2
    quarter = whole / 4
    EMIT = []
    a = 0
    b = 1 << preci
    bb = b
    z = 0
    i = 1
    DL = 0
    s = 0
    token = None
    break_sign = False
    while (i <= preci and i <= M):
        if ct[i-1] == '1':
            z = z + (1 << (preci - i))
        i = i + 1

    tt = time.perf_counter()
    print_counter = 0
    okay_to_break = False
    #Now Z is an integer of the ct.
    #print("input cipher text in numeber (z): "+str(z))
    model.reset()
    while (1):
        """ Approach 2 : Stick with YouTube"""
        emission = model.EmitToken(a,b,z,model_name)
        if emission is not None:
            token = emission[0]
            a = emission[1]
            b = emission[2]
            okay_to_break = emission[3]
            EMIT.append(token)
        #print("emitted"+str(token))
        """ End of approach 1 """
        while (b < half) or (a > half):
            if b < half:
                a = 2 * a
                b = 2 * b
                z = 2 * z
                DL = DL + s + 1
                s = 0
            elif a > half:
                a = 2 * (a - half)
                b = 2 * (b - half)
                z = 2 * (z - half)
                DL = DL + s + 1
                s = 0
            """ Update approximation?? """
            if i <= M and ct[i-1] == '1':
                z = z + 1
            i = i + 1
            """ Middle type rescaling """
        while a > quarter and b < 3 * quarter:
            s = s + 1
            a = 2 * (a - quarter)
            b = 2 * (b - quarter)
            z = 2 * (z - quarter)
            if i <= M and ct[i-1] == '1':
                z = z + 1
            i = i + 1
        #if DL >= M:
        #    break
        t = time.perf_counter()
        if t - tt > 3 or (DL >= M and okay_to_break):
            dprint(len(EMIT))
            dprint("DL="+str(DL))
            dprint("M="+str(M))
            dprint("s="+str(s))
            dprint("a="+str(a))
            dprint("b="+str(b))
            dprint("z="+str(z))
            dprint("half="+str(half))
            if (t - tt) > 3:
                dprint("Operation lasted longer than 3 seconds. Abort!!!")
            else:
                dprint("Lasted "+str(t-tt)+" seconds")
            break
        else:
            if not z == half or print_counter < 10:
                #RE = encoder.encode_ytb(EMIT, "complx")
                #reencode = "".join(RE)
                #dprint("         "+reencode)
                dprint("a="+str(a/bb)+"\tb="+str(b/bb)+"\tz="+str(z/bb))
        if z == half:
            print_counter += 1
            #RE2 = encoder.encode_ytb(EMIT, "complx")
            #if len(RE2) >= M and okay_to_break:
            if okay_to_break:
                break
        #if z == half:
            #break_sign = True
        #print(DL)
        #print(M)
    #print("----------------")
    #print("Final emit : "+" ".join(EMIT))
    return EMIT



    

def decode(ct_str, model_name = None):
    """interface"""
    #print("######################################################")
    return decode_ytb(ct_str, model_name)


if __name__ == "__main__":
    test_ct = "11011110101011011011111011101111" #0xdeadbeef
    test_ct_2 = "00100011100111"
    test_ct_2_1 = test_ct_2 +"010010"
    test_ct_3 = "001000110110001111101110001100001"
    test_ct_3_1 = test_ct_3 +"10111011101"

    decode(test_ct_2, "complx")
    #decode(test_ct_2_1)
    decode(test_ct_3, "complx")
    #decode(test_ct_3_1)
    #decode(test_ct)

    #out = decode_basic(test_ct)
    #print(out)
