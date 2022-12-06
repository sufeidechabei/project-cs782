

import time
import os
import json
from e2e_encryptor import run_encryption
from e2e_decryptor import run_decryption
diff_msg = ["I", "UW-Madiosn", "Truth"]
diff_bytes = [16, 32, 64]
diff_first_phase = ["Until", "When", "My", "You"]
running_times = 1000
file_name = "setnence.txt"

# Check if the file exists
if os.path.exists(file_name):
  # If the file exists, delete it
  os.remove(file_name)
for m in diff_msg:
    for b in diff_bytes:
        for ph in diff_first_phase:
            encode_time = []
            decode_time = []
            generated_length = []
            for i in range(running_times):
                # sentence_ref = ''.join(en[1])
                # with bert_serving.client.BertClient() as bc:
                # vector1 = bc.encode([sentence])
                # vector2 = bc.encode([m])
                # similarity = cosine_similarity(vector1)[0][0]
                # bleu_score = nltk.translate.bleu_score.sentence_bleu([sentence_ref], sentence)
                # similarity =

                try:
                   begin_de_time = time.time()
                   begin_enc_time = time.time()
                   en = run_encryption(m, b, ph, include_iv=True)
                   end_enc_time = time.time()


                   sentence = ph + ''.join(en[0])
                   sentence_length = len(sentence)
                   de = run_decryption(sentence, b)
                   end_de_time = time.time()
                   encode_time.append(end_enc_time - begin_enc_time)
                   decode_time.append(end_de_time - begin_de_time)
                   metrics = {"message": m, "byte": b, "first": ph,
                              "encode_time":encode_time, "decode_time":decode_time, "sentence":sentence}
                   json_string = json.dumps(metrics)
                   with open(file_name, 'w+') as f:
                       f.write(json_string)

                except:
                    continue

                if len(encode_time) == 5:
                    break
                print("hhhhh")
