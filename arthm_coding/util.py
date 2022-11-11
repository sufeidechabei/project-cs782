"""Utils needed for arithmatic encoding and decoding"""
import model as model


coding_parameters = {
        "symbol_length":8,
        "coding_length":4;
        }


def Adjust(model_name, token, a, b):
    cumu, relative = model.GetFreq(token, model_name)
    diff = b - a
    new_a = a + math.floor((cumu - relative) * diff) #The paper says addition, but I think it should be subtraction
    new_b = a + math.floor(cumu * diff)
    return new_a, new_b


def Rescale(D, w, a, b, c=0, C=None)
    #TODO
    r = coding_parameters["symbol_length"]
    l = coding_parameters["coding_length"]
    if w > 0 and double_floor_op(a, r*l, r*l-1) == double_floor_op(b, r*l, r*l-1):


def double_ceil_op(a,b,c):
    c2 = 1 << c
    b2 = 1 << b
    return (a * c2) % b2

def double_floor_op(a,b,c):
    c2 = 1 << c
    b2 = 1 << b
    res = (a % b2) / c2
    return math.floor(res)
