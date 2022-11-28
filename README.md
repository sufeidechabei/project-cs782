This is an attempt to realize the E2E mechanisms in "Passing Covert Messages on Public Platforms: An Approach Using Model-Based Format-Transforming Encryption"

The crypto folder contains necessary modules for encryption/decryption.

The arthm_coding folder contains modules for arithmatic decoding/encoding and the model used for them.

THe gpt2_arthm_coding folder contains the version using gpt2.

## How to use

Install PyTorch and and transformers and pycryptodome and termcolor

To encrypt a message run:
```
python e2e_encryptor.py -l [coding range] -s [first word]
```

To decrypt a message run:
```
python e2e_decryptor.py -l [coding range]
```
