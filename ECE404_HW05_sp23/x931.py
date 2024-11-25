# Homework Number:05 - Part 1
# Name: Parth R Doshi   
# ECN Login: doshi36
# Due Date: 2/21/2023

import sys
from BitVector import *

AES_modulus = BitVector(bitstring='100011011')
subBytesTable = []                                                  
invSubBytesTable = []      

def gee(keyword, round_constant, byte_sub_table):
    '''
    This is the g() function you see in Figure 4 of Lecture 8.
    '''
    rotated_word = keyword.deep_copy()
    rotated_word << 8
    newword = BitVector(size = 0)
    for i in range(4):
        newword += BitVector(intVal = byte_sub_table[rotated_word[8*i:8*i+8].intValue()], size = 8)
    newword[:8] ^= round_constant
    round_constant = round_constant.gf_multiply_modular(BitVector(intVal = 0x02), AES_modulus, 8)
    return newword, round_constant

def gen_key_schedule_256(key_bv):
    byte_sub_table = subBytesTable
    #  We need 60 keywords (each keyword consists of 32 bits) in the key schedule for
    #  256 bit AES. The 256-bit AES uses the first four keywords to xor the input
    #  block with.  Subsequently, each of the 14 rounds uses 4 keywords from the key
    #  schedule. We will store all 60 keywords in the following list:
    key_words = [None for i in range(60)]
    round_constant = BitVector(intVal = 0x01, size=8)
    for i in range(8):
        key_words[i] = key_bv[i*32 : i*32 + 32]
    for i in range(8,60):
        if i%8 == 0:
            kwd, round_constant = gee(key_words[i-1], round_constant, byte_sub_table)
            key_words[i] = key_words[i-8] ^ kwd
        elif (i - (i//8)*8) < 4:
            key_words[i] = key_words[i-8] ^ key_words[i-1]
        elif (i - (i//8)*8) == 4:
            key_words[i] = BitVector(size = 0)
            for j in range(4):
                key_words[i] += BitVector(intVal = 
                                 byte_sub_table[key_words[i-1][8*j:8*j+8].intValue()], size = 8)
            key_words[i] ^= key_words[i-8] 
        elif ((i - (i//8)*8) > 4) and ((i - (i//8)*8) < 8):
            key_words[i] = key_words[i-8] ^ key_words[i-1]
        else:
            sys.exit("error in key scheduling algo for i = %d" % i)
    return key_words

def genTables():
    c = BitVector(bitstring='01100011')
    d = BitVector(bitstring='00000101')
    for i in range(0, 256):
        # For the encryption SBox
        a = BitVector(intVal = i, size=8).gf_MI(AES_modulus, 8) if i != 0 else BitVector(intVal=0)
        # For bit scrambling for the encryption SBox entries:
        a1,a2,a3,a4 = [a.deep_copy() for x in range(4)]
        a ^= (a1 >> 4) ^ (a2 >> 5) ^ (a3 >> 6) ^ (a4 >> 7) ^ c
        subBytesTable.append(int(a))
        # For the decryption Sbox:
        b = BitVector(intVal = i, size=8)
        # For bit scrambling for the decryption SBox entries:
        b1,b2,b3 = [b.deep_copy() for x in range(3)]
        b = (b1 >> 2) ^ (b2 >> 5) ^ (b3 >> 7) ^ d
        check = b.gf_MI(AES_modulus, 8)
        b = check if isinstance(check, BitVector) else 0
        invSubBytesTable.append(int(b))

def gen_subbytes_table():
    subBytesTable = []
    c = BitVector(bitstring='01100011')
    for i in range(0, 256):
        a = BitVector(intVal = i, size=8).gf_MI(AES_modulus, 8) if i != 0 else BitVector(intVal=0)
        a1,a2,a3,a4 = [a.deep_copy() for x in range(4)]
        a ^= (a1 >> 4) ^ (a2 >> 5) ^ (a3 >> 6) ^ (a4 >> 7) ^ c
        subBytesTable.append(int(a))
    return subBytesTable
    
def sub_bytes(statearray):
    #Step 1: Substitution Bytes
    for i in range (0,4):
        for j in range (0,4):
            index = int(statearray[j][i])
            statearray[j][i] = subBytesTable[index]
    return statearray

def Inv_sub_bytes(statearray):

    for i in range (0,4):
        for j in range (0,4):
            index = int(statearray[j][i])
            statearray[j][i] = invSubBytesTable[index]
    return statearray

def Shift_Rows(statearray): 
    for k in range (1,4):
        statearray[k] = statearray[k][k:] + statearray[k][:k]
    return statearray

def Inv_Shift_Rows(statearray):
    new_shifted_statearray = [[0 for x in range(4)] for x in range(4)]

    new_shifted_statearray[0][0] = statearray[0][0]
    new_shifted_statearray[0][1] = statearray[0][1]
    new_shifted_statearray[0][2] = statearray[0][2]
    new_shifted_statearray[0][3] = statearray[0][3]

    new_shifted_statearray[1][0] = statearray[1][3]
    new_shifted_statearray[1][1] = statearray[1][0]
    new_shifted_statearray[1][2] = statearray[1][1]
    new_shifted_statearray[1][3] = statearray[1][2]

    new_shifted_statearray[2][0] = statearray[2][2]
    new_shifted_statearray[2][1] = statearray[2][3]
    new_shifted_statearray[2][2] = statearray[2][0]
    new_shifted_statearray[2][3] = statearray[2][1]

    new_shifted_statearray[3][0] = statearray[3][1]
    new_shifted_statearray[3][1] = statearray[3][2]
    new_shifted_statearray[3][2] = statearray[3][3]
    new_shifted_statearray[3][3] = statearray[3][0]

    return new_shifted_statearray

def Mix_Col(new_statearray):
    
    hex2 = BitVector(bitstring = "00000010")
    hex3 = BitVector(bitstring = "00000011")

    mix_col_statearray = [[0 for x in range(4)] for x in range(4)]
    
    for j in range(0,4):
        mix_col_statearray[0][j] = (new_statearray[0][j].gf_multiply_modular(hex2,AES_modulus,8)) ^ ((new_statearray[1][j].gf_multiply_modular(hex3,AES_modulus,8))) ^ (new_statearray[2][j]) ^ (new_statearray[3][j])
        mix_col_statearray[1][j] = (new_statearray[0][j]) ^ (new_statearray[1][j].gf_multiply_modular(hex2,AES_modulus,8)) ^ (new_statearray[2][j].gf_multiply_modular(hex3,AES_modulus,8)) ^ (new_statearray[3][j])
        mix_col_statearray[2][j] = (new_statearray[0][j]) ^ (new_statearray[1][j]) ^ (new_statearray[2][j].gf_multiply_modular(hex2,AES_modulus,8)) ^ (new_statearray[3][j].gf_multiply_modular(hex3,AES_modulus,8))
        mix_col_statearray[3][j] = (new_statearray[0][j].gf_multiply_modular(hex3,AES_modulus,8)) ^ (new_statearray[1][j]) ^ (new_statearray[2][j]) ^ (new_statearray[3][j].gf_multiply_modular(hex2,AES_modulus,8))

    new_state_array_bv = BitVector(size = 0)
    for i in range (0,4):
        for j in range (0,4):
            new_state_array_bv = new_state_array_bv + mix_col_statearray[j][i]

    return new_state_array_bv

def Inv_Mix_Col(new_statearray):

    hexE = BitVector(hexstring = "0e")
    hexD = BitVector(hexstring = "0d")
    hexB = BitVector(hexstring = "0b")
    hex9 = BitVector(hexstring = "09")

    mix_col_statearray = [[0 for x in range(4)] for x in range(4)]
    
    for j in range(0,4):
        mix_col_statearray[0][j] = (new_statearray[0][j].gf_multiply_modular(hexE, AES_modulus, 8)) ^ ((new_statearray[1][j].gf_multiply_modular(hexB,AES_modulus,8))) ^ ((new_statearray[2][j].gf_multiply_modular(hexD,AES_modulus,8))) ^ ((new_statearray[3][j].gf_multiply_modular(hex9,AES_modulus,8)))
        mix_col_statearray[1][j] = (new_statearray[0][j].gf_multiply_modular(hex9, AES_modulus, 8)) ^ ((new_statearray[1][j].gf_multiply_modular(hexE,AES_modulus,8))) ^ ((new_statearray[2][j].gf_multiply_modular(hexB,AES_modulus,8))) ^ ((new_statearray[3][j].gf_multiply_modular(hexD,AES_modulus,8)))
        mix_col_statearray[2][j] = (new_statearray[0][j].gf_multiply_modular(hexD, AES_modulus, 8)) ^ ((new_statearray[1][j].gf_multiply_modular(hex9,AES_modulus,8))) ^ ((new_statearray[2][j].gf_multiply_modular(hexE,AES_modulus,8))) ^ ((new_statearray[3][j].gf_multiply_modular(hexB,AES_modulus,8)))
        mix_col_statearray[3][j] = (new_statearray[0][j].gf_multiply_modular(hexB, AES_modulus, 8)) ^ ((new_statearray[1][j].gf_multiply_modular(hexD,AES_modulus,8))) ^ ((new_statearray[2][j].gf_multiply_modular(hex9,AES_modulus,8))) ^ ((new_statearray[3][j].gf_multiply_modular(hexE,AES_modulus,8)))

    new_state_array_bv = BitVector(size = 0)
    for i in range (0,4):
        for j in range (0,4):
            new_state_array_bv = new_state_array_bv + mix_col_statearray[j][i]

    return new_state_array_bv

def encrypt(plaintext_file, key_file):

    #Convert key_text into a bitvector 
    key_fp = open(key_file,'r')
    key_bv = BitVector(textstring = key_fp.read().strip())
    key_words = gen_key_schedule_256(key_bv)

    #Convert plaintext into a bitvector
    plaintext_bv = plaintext_file

#Ensure the input block is 128 bits
    if plaintext_bv._getsize() > 0:
        if plaintext_bv._getsize() < 128:
            plaintext_bv.pad_from_right(128 - plaintext_bv._getsize())

    num_rounds = 14

    #List of Round Keys
    round_keys = [None for i in range(num_rounds+1)]
    for i in range(num_rounds+1):
        round_keys[i] = (key_words[i*4] + key_words[i*4+1] + key_words[i*4+2] + key_words[i*4+3])

    #Xor before any input processing
    plaintext_bv ^= round_keys[0]

    for var in range (0,13):
        
        #Generation of Input State Array
        statearray = [[0 for x in range(4)] for x in range(4)]
        
        for i in range(4):
            for j in range(4):
                statearray[j][i] = plaintext_bv[32*i + 8*j:32*i + 8*(j+1)]
        
        #Step 1: Sub_Bytes
        statearray = sub_bytes(statearray)
        
        #Step 2: Shift_Rows
        statearray = Shift_Rows(statearray)
        
        #Convert the statearray from a list[list[int]] -> list[BitVectors]
        new_statearray = [[0 for x in range(4)] for x in range(4)]
        for i in range(0,4):
            for j in range(0,4): 
                new_statearray[j][i] =  BitVector(intVal = statearray[j][i], size = 8)
        
        #Step 3: Mixing Columns 
        new_state_array_bv = Mix_Col(new_statearray)

        #Add round key
        plaintext_bv = new_state_array_bv ^ round_keys[var + 1]
        
    #Generation of Input State Array
    statearray = [[0 for x in range(4)] for x in range(4)]
    
    for i in range(4):
        for j in range(4):
            statearray[j][i] = plaintext_bv[32*i + 8*j:32*i + 8*(j+1)]
    #Step 1: Sub_Bytes
    statearray = sub_bytes(statearray)
    #Step 2: Shift_Rows
    statearray = Shift_Rows(statearray)

    #Convert the statearray from a list[list[int]] -> list[BitVectors]
    new_statearray = [[0 for x in range(4)] for x in range(4)]
    for i in range(0,4):
        for j in range(0,4): 
            new_statearray[j][i] =  BitVector(intVal = statearray[j][i], size = 8)

    new_state_array_bv = BitVector(size = 0)
    for i in range (0,4):
        for j in range (0,4):
            new_state_array_bv = new_state_array_bv + new_statearray[j][i]

    new_state_array_bv = new_state_array_bv ^ round_keys[14]
    return new_state_array_bv

def decrypt(ciphertext_file, key_file, decrypted_txt):
    genTables()

    #Convert key_text into a bitvector 
    key_bv = BitVector(textstring = key_file.read().strip())
    key_words = gen_key_schedule_256(key_bv)

    #Convert plaintext into a bitvector
    cipher_fp = open(ciphertext_file,'r')

    ciphertext_bits = BitVector(hexstring = cipher_fp.read())

    for i in range(len(ciphertext_bits)//128):
        ciphertext_bv = ciphertext_bits[128*i:128*(i+1)]

    #Ensure the input block is 128 bits
        if ciphertext_bv._getsize() > 0:
            if ciphertext_bv._getsize() < 128:
                ciphertext_bv.pad_from_right(128 - ciphertext_bv._getsize())
    
        num_rounds = 14

        #List of Round Keys
        round_keys = [None for i in range(num_rounds+1)]
        for i in range(num_rounds+1):
            round_keys[i] = (key_words[i*4] + key_words[i*4+1] + key_words[i*4+2] + key_words[i*4+3])
        
        round_keys.reverse()

        #Xor before any input processing
        ciphertext_bv ^= round_keys[0]

        for var in range (0,13):
            
            #Generation of Input State Array
            statearray = [[0 for x in range(4)] for x in range(4)]
            
            for i in range(4):
                for j in range(4):
                    statearray[j][i] = ciphertext_bv[32*i + 8*j:32*i + 8*(j+1)]
            
            #Step 1: Inv_Shift_Rows
            statearray = Inv_Shift_Rows(statearray)

            #Step 2: Inv_Sub_Bytes
            statearray = Inv_sub_bytes(statearray)
            
            #Convert the statearray from a list[list[int]] -> list[BitVectors]
            new_statearray = [[0 for x in range(4)] for x in range(4)]
            for i in range(0,4):
                for j in range(0,4): 
                    new_statearray[j][i] =  BitVector(intVal = statearray[j][i], size = 8)
            
            new_state_array_bv = BitVector(size = 0)
            for i in range (0,4):
                for j in range (0,4):
                    new_state_array_bv = new_state_array_bv + new_statearray[j][i]

            #Add round key
            ciphertext_bv = new_state_array_bv ^ round_keys[var + 1]

            new_statearray_inv = [[0 for x in range(4)] for x in range(4)]
            
            for i in range(4):
                for j in range(4):
                    new_statearray_inv[j][i] = ciphertext_bv[32*i + 8*j:32*i + 8*(j+1)]

            #Step 3: Inv_Mixing Columns 
            new_state_array_bv = Inv_Mix_Col(new_statearray_inv)

            ciphertext_bv = new_state_array_bv

        #Generation of Input State Array
        statearray = [[0 for x in range(4)] for x in range(4)]
        
        for i in range(4):
            for j in range(4):
                statearray[j][i] = ciphertext_bv[32*i + 8*j:32*i + 8*(j+1)]

        #Step 2: Shift_Rows
        statearray = Inv_Shift_Rows(statearray)

        #Step 1: Sub_Bytes
        statearray = Inv_sub_bytes(statearray)
        
        #Convert the statearray from a list[list[int]] -> list[BitVectors]
        new_statearray = [[0 for x in range(4)] for x in range(4)]
        for i in range(0,4):
            for j in range(0,4): 
                new_statearray[j][i] =  BitVector(intVal = statearray[j][i], size = 8)

        new_state_array_bv = BitVector(size = 0)
        for i in range (0,4):
            for j in range (0,4):
                new_state_array_bv = new_state_array_bv + new_statearray[j][i]

        new_state_array_bv = new_state_array_bv ^ round_keys[14]

        decrypted_txt.write(new_state_array_bv.get_bitvector_in_ascii())

def x931(v0, dt, totalNum, key_file):
    genTables()
# * Arguments:
# v0: 128-bit BitVector object containing the seed value
# dt: 128-bit BitVector object symbolizing the date and time
# totalNum: The total number of random numbers to generate
# key_file: Filename for text file containing the ASCII encryption key for AES

# * Function Description:
# This function uses the arguments with the X9.31 algorithm to generate totalNum
# random numbers as BitVector objects.
# Returns a list of BitVector objects, with each BitVector object representing a
# random number generated from X9.31.

    #Xor the date and time with the bitvector object containing the seed value
    random_num = []
    for i in range (0,totalNum):
        dt_bv = encrypt(dt, key_file)
        xored_result = dt_bv ^ v0
        encrypted_v0 = encrypt(xored_result, key_file)
        random_num.append(encrypted_v0)
        v0 = encrypt((encrypted_v0 ^ dt_bv), key_file)
        
    return random_num

if __name__ == "__main__":
    
    v0 = BitVector(textstring="computersecurity") #v0 will be  128 bits
   
    #As mentioned before, for testing purposes dt is set to a predetermined value
    dt = BitVector(intVal = 501, size=128)
    listX931 = x931(v0,dt,3,"keyX931.txt")

    #Check if list is correct
    print("{}\n{}\n{}".format(int(listX931[0]),int(listX931[1]),int(listX931[2])))
