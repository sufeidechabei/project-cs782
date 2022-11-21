"""This is where we put the code for models used in arithmatic coding"""
import math

simple_token_set = ["I","eat","hello","what","really","meat","secret","impossible"]
probability_base = 200
simple_token_frequency = [43,10,21,47,33,18,8,20]
simple_token_frequency_dict = {}
simple_token_cumu_frequency_dict = {}
simple_token_cumu_frequency_list = []


complx_token_set = ["time", "person", "year", "way", "day", "thing", "man", "world", "life", "hand", "part", "child", "eye", "woman", "place", "work", "week", "case", "point", "government", "company", "number", "group", "problem", "fact", "be", "have", "do", "say", "get", "make", "go", "know", "take", "see", "come", "think", "look", "want", "give", "use", "find", "tell", "ask", "work", "seem", "feel", "try", "leave", "call", "good", "new", "first", "last", "long", "great", "little", "own", "other", "old", "right", "big", "high", "different", "small", "large", "next", "early", "young", "important", "few", "public", "bad", "same", "able", "to", "of", "in", "for", "on", "with", "at", "by", "from", "up", "about", "into", "over", "after", "the", "and", "a", "that", "I", "it", "not", "he", "as", "you", "this", "but", "his", "they", "her", "she", "or", "an", "will", "my", "one", "all", "would", "there", "their"]

complx_token_frequency = [93, 36, 41, 36, 11, 18, 34, 32, 15, 14, 67, 66, 75, 44, 70, 70, 23, 22, 71, 44, 13, 2, 43, 19, 24, 98, 6, 97, 33, 15, 22, 8, 33, 30, 11, 21, 38, 64, 33, 74, 45, 36, 62, 15, 91, 49, 100, 35, 34, 10, 56, 56, 87, 65, 30, 52, 6, 73, 94, 59, 5, 4, 8, 87, 77, 89, 12, 81, 80, 30, 2, 91, 46, 17, 76, 33, 92, 14, 27, 92, 65, 47, 54, 96, 17, 15, 57, 47, 56, 23, 85, 64, 91, 91, 30, 5, 35, 9, 73, 85, 70, 21, 17, 93, 52, 52, 47, 36, 84, 19, 44, 30, 43, 9]

complx_token_frequency_dict = {}
complx_token_cumu_frequency_dict = {}
complx_token_cumu_frequency_list = []

complx_token_freq_sum = 5246


def generate_complx_cumu_frequency():
    if len(complx_token_cumu_frequency_dict) !=  0:
        return;
    current_cumu = 0
    for i in range(0,len(complx_token_set)):
        token = complx_token_set[i]
        current_cumu += complx_token_frequency[i]
        complx_token_cumu_frequency_dict[token] = current_cumu/complx_token_freq_sum
        complx_token_frequency_dict[token] = complx_token_frequency[i]/complx_token_freq_sum
        complx_token_cumu_frequency_list.append((token,
            current_cumu/complx_token_freq_sum,
            complx_token_frequency[i]/complx_token_freq_sum 
            ))


def complxEmitToken(a, b, z):
    for token_info in complx_token_cumu_frequency_list:
        token = token_info[0]
        cumu = token_info[1]
        relative = token_info[2]
        diff = b - a
        a0 = a + math.floor((cumu-relative)*diff)
        b0 = a + math.floor(cumu*diff)
        if a0 <= z and z < b0:
            return (token, a0, b0)
    return None



def complxGetToken(freq):
    for token_info in complx_token_cumu_frequency_list:
        if token_info[1] >= freq:
            return token_info[0]

def complxGetFreq(token):
    cumu = complx_token_cumu_frequency_dict[token]
    relative = complx_token_frequency_dict[token]
    return (cumu, relative)

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
    if model == "complx":
        generate_complx_cumu_frequency()
        return complxGetToken(freq)
       
    return None

def GetFreq(token, model=None):
    if model is None:
        generate_simple_cumu_frequency()
        return simpleGetFreq(token)
    if model == "complx":
        generate_complx_cumu_frequency()
        return complxGetFreq(token)
    return None


def EmitToken(a,b,z,model=None):
    if model is None:
        return None
    if model == "complx":
        generate_complx_cumu_frequency()
        return complxEmitToken(a,b,z)
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
    print(simpleGetFreq("eat"))
    print(simpleGetFreq("hello"))
    print(simpleGetFreq("what"))
    print(simpleGetFreq("really"))
    print(simpleGetFreq("meat"))
