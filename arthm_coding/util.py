"""Utils needed for arithmatic encoding and decoding"""
import model as model
import random
import math

coding_parameters = {
        "symbol_length":8,
        "coding_length":4,
        }


def Adjust(model_name, token, a, b):
    cumu, relative = model.GetFreq(token, model_name)
    diff = b - a
    new_a = a + math.floor((cumu - relative) * diff) #The paper says addition, but I think it should be subtraction
    new_b = a + math.floor(cumu * diff)
    return new_a, new_b


def Rescale(D, w, a, b, c=-1, C=None):
    r = coding_parameters["symbol_length"]
    l = coding_parameters["coding_length"]
    xor_val = 1 << (r*l-1)
    cmp_val = 1 << (r*(l-1))
    while(1):
        if w > 0 and double_floor_op(a, r*l, r*l-1) == double_floor_op(b, r*l, r*l-1):
            D[-w] = D[-w] + double_floor_op(a, r*l, r*l-1)
            print("?? = "+str(double_floor_op(a, r*l, r*l-1)))
            for i in range(1,w):
                D[-i] = int(not D[-i])
            w = 0;
            a = a ^ xor_val
            b = b ^ xor_val
            if c >= 0:
                c = c ^ xor_val
        if b - a < cmp_val:
            A = double_floor_op(a, r*l, r*(l-1))
            D.append(A)
            a = double_ceil_op(a, r*l, r)
            b = double_ceil_op(b, r*l, r)
            if A != double_floor_op(b, r*l, r*(l-1)):
                a = a ^ xor_val 
                b = b ^ xor_val
                if c >= 0: 
                    c = c ^ xor_val
                if C is not None and len(D) + l <= len(C):
                    c = c + C[len(D)+l]
                else:
                    c = c+ dollar_sign(1 << r)
                    print("haha")
                w = w+1
        if b - a > cmp_val:
            break
    return a, b, c, w



def double_ceil_op(a,b,c):
    c2 = 1 << c
    b2 = 1 << b
    return (a * c2) % b2

def double_floor_op(a,b,c):
    c2 = 1 << c
    b2 = 1 << b
    res = (a % b2) / c2
    return math.floor(res)

def dollar_sign(n):
    ret = random.randint(0, n-1)
    return ret
