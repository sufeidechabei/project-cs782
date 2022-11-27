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
            return (token, a0, b0, True)
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


#######################################################
# TRY TO INCOPORATE OPEN AI
#######################################################
#import os
#import openai
#with open("SENSITIVE.txt","r") as r:
#    api_key = r.read()
#
#openai.api_key = api_key.rstrip()
#top_p = 0.1
#engine = "text-davinci-001"
#prompt = "The"
#max_tokens = 1
#logprobs = 5
#temperature = 0
#bias = {19990:-100,198:-100, 628:-100}
#
#response = openai.Completion.create(engine = engine, prompt = prompt, max_tokens = max_tokens, logprobs = logprobs, temperature=temperature, logit_bias =  bias)
#print(response)


##############################################################################################
# A more speaking friendly model
#############################################################################################
rotation = 1
english_token_set = {}
english_token_set[1] = ["James", "Robert", "John", "Michael", "David", "William", "Richard", "Joseph", "Thomas", "Charles", "Mary", "Patricia", "Jennifer", "Linda", "Elizabeth", "Barbara", "Susan", "Jessica", "Sarah", "Karen"]
english_token_set[2] = ["is", "has", "checks", "gets", "makes", "knows", "takes", "sees", "wants", "gives", "uses", "finds", "feels", "eats", "kicks", "touches"]
english_token_set[3] = ["door", "keys", "eyes", "headphones", "house", "spoon", "clothes", "pencil", "hairband", "glasses", "candle", "watch", "blanket", "toothpaste", "baseball", "burger", "chocolate"]
english_token_set[4] = ["when", "where", "if", "since", "although", "and", "or", "but"]

english_freq_set = {}
english_freq_set[1] = [23, 26, 33, 6, 19, 31, 48, 1, 5, 16, 18, 31, 36, 23, 12, 49, 20, 4, 43, 3]
english_freq_set[2] = [24, 6, 46, 37, 9, 33, 19, 9, 49, 1, 39, 14, 39, 34, 33, 27]
english_freq_set[3] = [12, 19, 44, 1, 46, 32, 39, 11, 15, 33, 21, 34, 45, 50, 30, 8, 12]
english_freq_set[4] = [33, 6, 28, 37, 3, 33, 5, 30]

english_freq_sum = {}
english_freq_sum[1] = 447
english_freq_sum[2] = 419
english_freq_sum[3] = 452
english_freq_sum[4] = 175

english_info_dict = {}
class rotation:
    r = 1

def reset():
    rotation.r = 1

def generate_english_cumu_frequency():
    a = rotation()
    if len(english_info_dict) !=  0:
        return
    for pos in range(1,5):
        english_info_dict[pos] = {}
        current_cumu = 0
        for i in range(0,len(english_token_set[pos])):
            #print(pos)
            #print(len(english_token_set[pos]))
            #print(len(english_freq_set[pos]))
            token = english_token_set[pos][i]
            #current_cumu += english_freq_set[pos][i]
            cumu_freq = current_cumu / english_freq_sum[pos]
            rela_freq = english_freq_set[pos][i]/english_freq_sum[pos]
            english_info_dict[pos][token] = (cumu_freq, rela_freq)
            current_cumu += english_freq_set[pos][i]


def englishEmitToken(a,b,z):
    for token in english_info_dict[rotation.r]:
        cumu = english_info_dict[rotation.r][token][0]
        rela = english_info_dict[rotation.r][token][1]
        diff = b - a
        a0 = a + math.floor((cumu-rela) * diff)
        b0 = a + math.floor(cumu * diff)
        breakable = False
        if rotation.r == 3:
            breakable = True
        if a0 <= z and z < b0:
            if rotation.r != 4:
                rotation.r = rotation.r + 1
            else:
                rotation.r = 1
            return (token, a0, b0, breakable)
    return None


def englishGetToken(freq):
    for token in english_info_dict[rotation.r]:
        if english_info_dict[rotation.r][token][0] + english_info_dict[rotation.r][token][1] >= freq:
            if rotation.r != 4:
                rotation.r = rotation.r + 1
            else:
                rotation.r = 1
            return token

def englishGetFreq(token):
    for pos in range(1, 5):
        if token in english_info_dict[pos]:
            cumu = english_info_dict[pos][token][0]
            rela = english_info_dict[pos][token][1]
            return (cumu, rela)

    








def GetToken(freq):
    generate_english_cumu_frequency()
    return englishGetToken(freq)



def GetFreq(token, model=None):
    if model is None:
        generate_simple_cumu_frequency()
        return simpleGetFreq(token)
    if model == "complx":
        generate_complx_cumu_frequency()
        return complxGetFreq(token)
    if model == "english":
        generate_english_cumu_frequency()
        return englishGetFreq(token)
    return None


def EmitToken(a,b,z,model=None):
    if model is None:
        return None
    if model == "complx":
        generate_complx_cumu_frequency()
        return complxEmitToken(a,b,z)
    if model == "english":
        generate_english_cumu_frequency()
        return englishEmitToken(a,b,z)
    return None

#if __name__ == '__main__' and False:
#    generate_simple_cumu_frequency()
#    print(simple_token_cumu_frequency_dict)
#    print("----")
#    print(simple_token_cumu_frequency_list)
#    print(simpleGetToken(0.456))
#    print(simpleGetToken(0.876))
#    print(simpleGetToken(0.234))
#    print(simpleGetToken(0.123))
#    print(simpleGetToken(0.567))
#    print(simpleGetToken(0.987))
#    print(simpleGetFreq("I"))
#    print(simpleGetFreq("eat"))
#    print(simpleGetFreq("hello"))
#    print(simpleGetFreq("what"))
#    print(simpleGetFreq("really"))
#    print(simpleGetFreq("meat"))
