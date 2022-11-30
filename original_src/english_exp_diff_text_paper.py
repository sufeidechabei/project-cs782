""" Too Simple of a test """
import binascii as binascii

import crypto.util as crypto
import arthm_coding.encoder as encoder
import arthm_coding.decoder as decoder
import arthm_coding.util as util

import arthm_coding.encoder_paper as en_paper
import arthm_coding.decoder_paper as de_paper


from datetime import datetime

to_file = False

def run_exp(secret_msg):
    key = crypto.obtain_key("super_simple")
    counter = 0
    while(1):
        counter = counter + 1
        res = run_single_exp(secret_msg, key)
        if res[0] == 1:
            break
    print()
    print("Ran "+str(counter)+" times to successuflly encrypt '"+secret_msg+"'")
    print("----------------------------------------------------------------------------------------------")
    print("OUTPUT = "+res[2])
    print()
    print()
    date_str = datetime.now().strftime("%d-%m-%Y@%H:%M:%S.txt")
    if not to_file:
        return
    with open("stats_log/"+date_str, "w+") as w:
        w.write("Failure cases due to decryption/padding error\n")
        print("Failure cases due to decryption/padding error")
        for data in stats[0]:
            w.write(data[0]+"  --->  "+data[1]+"\n")
            print(data[0]+"  --->  "+data[1])
        print()
        print()
        print("Failure cases due to wrong message produced")
        w.write("\n\n")
        w.write("Failure cases due to wrong message produced\n")
        for data in stats[2]:
            w.write(data[0]+"  --->  "+data[1]+" = "+data[2]+"\n")
            print(data[0]+"  --->  "+data[1]+" = "+data[2]+"\n")
        w.write("\n\n")
        w.write("Succeeded ones\n")
        print()
        print()
        print("Succeeded ones")
        for data in stats[1]:
            w.write(data[0]+" = "+"".join(data[1])+"\n")
            print(data[0]+" = "+" ".join(data[1]))





def run_single_exp(secret_msg, key):
    iv, ct = crypto.encrypt_aes_cbc(key, secret_msg)

    code = ct
    de = de_paper.PaperArthmDecoder(code = code)
    T = de.decode("english")
    eng = " ".join(T)




    tokens = eng.split()
    en = en_paper.PaperArthmEncoder()
    D, w = en.encode(tokens, "english")
    new_ct = bytes(D)


    try:
        new_msg = crypto.decrypt_aes_cbc(key, iv, new_ct)
    except:
        return (0,ct.hex(),new_ct.hex()+" w="+str(len(w)),"")
    if new_msg == secret_msg:
        return (1, ct.hex(),eng,"")
    else:
        return (2,ct.hex(),new_ct.hex()+" w="+str(len(w)),new_msg)






run_exp("UW - Madison")
run_exp("AF may lack fresh water!")
run_exp("Ba Yue Qiu Gao Feng Nu Hao, Juan Wo Wu Shang San Chong Mao.")
run_exp("..__.._.._..._..___..._.._...__.__..")

#print()
    #print("breaking into chunks")
    #twit_list = []
    #for i in range(0,1):
    #    sub_ct_bin = ct_bin[i*128:(i+1)*128]
    #    print(sub_ct_bin, end=" ")
    #    emit = decoder.decode_ytb(sub_ct_bin, "complx")
    #    twit_list.append(emit)

#print()

#print("Translate each 32-bit chunck with decoder:")
#for twit in twit_list:
    #print("#"+" ".join(twit))


#print()
#print()
#print("Attempt to translate them back with encoder:")
#reassemble= ""
#print("Encoded  CT = ", end = "")
#
#for twit in twit_list:
#    each = "".join(encoder.encode_ytb(twit, "complx"))[:64]
#    print(each,end = " ")
#    reassemble = reassemble + each
#
#
#print()
#print("Results from translating each 32-bit chunck with decoder:")
#for twit in twit_list:
#    print("#"+" ".join(twit))



#print()
#print("Results from translating Re-Encoded with decoder:")

#twit_list_2 = []
#for i in range(0,2):
#    sub_ct_bin = reassemble[i*64:(i+1)*64]
#    #print(sub_ct_bin)
#    emit = decoder.decode_ytb(sub_ct_bin, "complx")
#    twit_list_2.append(emit)

#for twit in twit_list_2:
#    print("#"+" ".join(twit))

#print()
#print()
#print()
#print()
#print()
#print()
#print("Trying decode the entire CT")
#print()
#emit2 = decoder.decode_ytb(ct_bin, "complx")
#print(" ".join(emit2))
