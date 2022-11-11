"""This is where we put the code for models used in arithmatic coding"""


simple_token_set = ["I","cannot","hello","what","really","meat","secret","impossible"]
probability_base = 200
simple_token_frequency = [43,10,21,47,33,18,8,20]
simple_token_frequency_dict = {}
simple_token_cumu_frequency_dict = {}
simple_token_cumu_frequency_list = []

def generate_simple_cumu_frequency():
    if len(simple_token_cumu_frequency_dict) !=  0:
        return;
    current_cumu = 0
    for i in range(0,8):
        token = simple_token_set[i]
        current_cumu += simple_token_frequency[i]
        simple_token_cumu_frequency_dict[token] = current_cumu
        simple_token_frequency_dict[token] = simple_token_frequency[i]
        simple_token_cumu_frequency_list.append((token, current_cumu))


def simpleGetToken(freq):
    for token_info in simple_token_cumu_frequency_list:
        if token_info[1]/probability_base >= freq:
            return token_info[0]

def simpleGetFreq(token):
    cumu = simple_token_cumu_frequency_dict[token]
    relative = simple_token_frequency_dict[token]
    return (cumu/probability_base, relative/probability_base)




def GetToken(freq, model=None):
    if model is None:
        generate_simple_cumu_frequency()
        return simpleGetToken(freq)
    return None

def GetFreq(token, model=None):
    if model is None:
        generate_simple_cumu_frequency()
        return simpleGetFreq(token)
    return None


if __name__ == '__main__':
    generate_simple_cumu_frequency()
    print(simple_token_cumu_frequency_dict)
    print("----")
    print(simple_token_cumu_frequency_list)
    print(simpleGetToken(0.456))
    print(simpleGetToken(0.876))
    print(simpleGetToken(0.234))
    print(simpleGetToken(0.123))
    print(simpleGetToken(0.567))
    print(simpleGetToken(0.987))
    print(simpleGetFreq("I"))
    print(simpleGetFreq("cannot"))
    print(simpleGetFreq("hello"))
    print(simpleGetFreq("what"))
    print(simpleGetFreq("really"))
    print(simpleGetFreq("meat"))
