""" Too Simple of a test """
import binascii as binascii

import crypto.util as crypto
import arthm_coding.encoder as encoder
import arthm_coding.decoder as decoder
import arthm_coding.util as util

from datetime import datetime

def run_exp(secret_msg):
    key = crypto.obtain_key("super_simple")
    runs = 100
    print("Message to encrypt = "+secret_msg)
    print("Running "+str(runs)+" experiments")
    stats = {}
    stats[0] = []
    stats[1] = []
    stats[2] = []
    for ii in range(0, runs):
        res = run_single_exp(secret_msg, key)
        stats[res[0]].append((res[1],res[2],res[3]))
        print("=",end="")
    print()
    print("-------- Summary ---------")
    print("Success: "+str(len(stats[1])))
    print("Failure: "+str(len(stats[0])+len(stats[2])))
    print()
    date_str = datetime.now().strftime("%d-%m-%Y@%H:%M:%S.txt") 
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
    binary_ct_len = len(ct.hex())*4
    ct_bin = (str(bin(int(ct.hex(),16)))[2:]).zfill(binary_ct_len)

    eng = decoder.decode_ytb(ct_bin, "complx")
    
    
    
    
    encoded_ct = "".join(encoder.encode_ytb(eng, "complx"))[:binary_ct_len]
    

    old_value = int(ct_bin, 2)
    new_value = int(encoded_ct, 2)
    xored = old_value ^ new_value
    xored_str = str((bin(xored)[2:])).zfill(binary_ct_len)

    
    hex_encoded_ct = hex(int(encoded_ct,2)).zfill(len(ct.hex()))
   
    
    new_ct = (bytes.fromhex(hex_encoded_ct[2:].zfill(len(ct.hex()))))
    try:
        new_msg = crypto.decrypt_aes_cbc(key, iv, new_ct)
    except:
        return (0,ct.hex(),hex_encoded_ct[2:],"")
    if new_msg == secret_msg:
        return (1, ct.hex(),eng,"")
    else:
        return (2,ct.hex(),hex_encoded_ct[2:],new_msg)






run_exp("UW - Madison")
#run_exp("AF may lack fresh water!")
#run_exp("Ba Yue Qiu Gao Feng Nu Hao, Juan Wo Wu Shang San Chong Mao.")
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
