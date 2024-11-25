# Homework Number: 01
# Name: Parth R Doshi 
# ECN Login: doshi36 
# Due Date: 1/19/2023
# Credit : Avinash Kak

import sys
from BitVector import *
import time

def cryptBreak(ciphertextFile, key_bv):
    #Arguments:
    # * ciphertextFile: String containing file name of the ciphertext
    # * key_bv: 16-bit BitVector for the decryption key 
    #
    # Function Decomposition: 
    #   Attempts to decrypt the ciphertext within ciphertextFile file using key_bv and returns the original plaintext as a string
    
    PassPhrase = "Hopes and dreams of a million years"
    BLOCKSIZE = 16
    numbytes = BLOCKSIZE // 8

    # Reduce the passphrase to a bit array of size BLOCKSIZE:

    bv_iv = BitVector(bitlist = [0]*BLOCKSIZE)
    for i in range(0,len(PassPhrase) // numbytes):
        textstr = PassPhrase[i*numbytes:(i+1)*numbytes]
        bv_iv ^= BitVector( textstring = textstr )
    
    # Create a bitvector from ciphertext hex string:
    FILEIN = open(ciphertextFile)
    encrypted_bv = BitVector( hexstring = FILEIN.read())
    FILEIN.close()

    # Create a bitvector for storing the decrypted plaintext bit array
    msg_decrypted_bv = BitVector( size = 0 )

    # Differential XORing
    previous_decrypted_block = bv_iv
    for i in range(0, len(encrypted_bv) // BLOCKSIZE):
        bv = encrypted_bv[i*BLOCKSIZE:(i+1)*BLOCKSIZE]
        temp = bv.deep_copy()
        bv ^= previous_decrypted_block
        previous_decrypted_block = temp
        bv ^= key_bv
        msg_decrypted_bv += bv

    # Extract plaintext from decrypted BitVector 
    output_txt = msg_decrypted_bv.get_text_from_bitvector()
    # FILEOUT = open(sys.argv[2], 'w')
    # FILEOUT.write(output_txt)
    # FILEOUT.close
    return output_txt

if __name__ == "__main__":
    
    for i in range (0, pow(2,16)):
        key_bv = BitVector(intVal = i, size = 16)
        decryptedMessage = cryptBreak('ciphertext.txt', key_bv)
        # print(i)
        if 'Sir Lewis' in decryptedMessage:
            break
    # print(f"Encrypted Key:",i,"\n")
    print(f"{decryptedMessage}")