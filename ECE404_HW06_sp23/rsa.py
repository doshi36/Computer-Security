# Homework Number: 06 - Part 1
# Name: Parth R Doshi   
# ECN Login: doshi36
# Due Date: 2/28/2023

import sys
from BitVector import * 
import random

class PrimeGenerator( object ):                                              #(A1)

    def __init__( self, **kwargs ):                                          #(A2)
        bits = debug = None                                                  #(A3)
        if 'bits' in kwargs  :     bits = kwargs.pop('bits')                 #(A4)
        if 'debug' in kwargs :     debug = kwargs.pop('debug')               #(A5)
        self.bits            =     bits                                      #(A6)
        self.debug           =     debug                                     #(A7)
        self._largest        =     (1 << bits) - 1                           #(A8)

    def set_initial_candidate(self):                                         #(B1)
        candidate = random.getrandbits( self.bits )                          #(B2)
        if candidate & 1 == 0: candidate += 1                                #(B3)
        candidate |= (1 << self.bits-1)                                      #(B4)
        candidate |= (2 << self.bits-3)                                      #(B5)
        self.candidate = candidate                                           #(B6)

    def set_probes(self):                                                    #(C1)
        self.probes = [2,3,5,7,11,13,17]                                     #(C2)

    # This is the same primality testing function as shown earlier
    # in Section 11.5.6 of Lecture 11:
    def test_candidate_for_prime(self):                                      #(D1)
        'returns the probability if candidate is prime with high probability'
        p = self.candidate                                                   #(D2)
        if p == 1: return 0                                                  #(D3)
        if p in self.probes:                                                 #(D4)
            self.probability_of_prime = 1                                    #(D5)
            return 1                                                         #(D6)
        if any([p % a == 0 for a in self.probes]): return 0                  #(D7)
        k, q = 0, self.candidate-1                                           #(D8)
        while not q&1:                                                       #(D9)
            q >>= 1                                                          #(D10)
            k += 1                                                           #(D11)
        if self.debug: print("q = %d  k = %d" % (q,k))                       #(D12)
        for a in self.probes:                                                #(D13)
            a_raised_to_q = pow(a, q, p)                                     #(D14)
            if a_raised_to_q == 1 or a_raised_to_q == p-1: continue          #(D15)
            a_raised_to_jq = a_raised_to_q                                   #(D16)
            primeflag = 0                                                    #(D17)
            for j in range(k-1):                                             #(D18)
                a_raised_to_jq = pow(a_raised_to_jq, 2, p)                   #(D19)
                if a_raised_to_jq == p-1:                                    #(D20)
                    primeflag = 1                                            #(D21)
                    break                                                    #(D22)
            if not primeflag: return 0                                       #(D23)
        self.probability_of_prime = 1 - 1.0/(4 ** len(self.probes))          #(D24)
        return self.probability_of_prime                                     #(D25)

    def findPrime(self):                                                     #(E1)
        self.set_initial_candidate()                                         #(E2)
        if self.debug:  print("    candidate is: %d" % self.candidate)       #(E3)
        self.set_probes()                                                    #(E4)
        if self.debug:  print("    The probes are: %s" % str(self.probes))   #(E5)
        max_reached = 0                                                      #(E6)
        while 1:                                                             #(E7)
            if self.test_candidate_for_prime():                              #(E8)
                if self.debug:                                               #(E9)
                    print("Prime number: %d with probability %f\n" %       
                          (self.candidate, self.probability_of_prime) )      #(E10)
                break                                                        #(E11)
            else:                                                            #(E12)
                if max_reached:                                              #(E13)
                    self.candidate -= 2                                      #(E14)
                elif self.candidate >= self._largest - 2:                    #(E15)
                    max_reached = 1                                          #(E16)
                    self.candidate -= 2                                      #(E17)
                else:                                                        #(E18)
                    self.candidate += 2                                      #(E19)
                if self.debug:                                               #(E20)
                    print("    candidate is: %d" % self.candidate)           #(E21)
        return self.candidate                                                #(E22)

def gcd(a,b):

    a,b = int(a),int(b)
    while b:                                             
        a,b = b, a % b
    return a

def key_generation(p_fp, q_fp):  

    e = 65537
    generator = PrimeGenerator(bits = 128) #object instantiation

    p = generator.findPrime() #generate p
    q = generator.findPrime() #generate q

    gcd_p = gcd(p  - 1, e)
    gcd_q = gcd(q  - 1, e)

    #Condition  2 and 3: 
    while ((p == q) or (gcd_p != 1) or (gcd_q != 1)) :
        
        p = generator.findPrime()
        q = generator.findPrime()

        gcd_p = gcd(p  - 1, e)
        gcd_q = gcd(q  - 1, e)    
    
    p_fp.write(str(p))
    q_fp.write(str(q))

def encrypt(plaintext_file, p_file, q_file, output_file):

    e =  65537
    plaintext_bits = BitVector(filename = plaintext_file)

    p_int = int(p_file.read())
    q_int = int(q_file.read())

    while plaintext_bits.more_to_read:

        plaintext_bv = plaintext_bits.read_bits_from_file(128)
        if plaintext_bv._getsize() > 0:
            if plaintext_bv._getsize() < 128:
                plaintext_bv.pad_from_right(128 - plaintext_bv._getsize())
        
        n = p_int * q_int 
        totient_n = (p_int-1) * (q_int-1)

        cipherblock = pow(int(plaintext_bv),e,n)
        cipherblock = BitVector(intVal = cipherblock, size = 256)
        output_file.write(cipherblock.get_hex_string_from_bitvector())

def decrypt(ciphertext_file, p_file, q_file, output_file):
    
    e = 65537
    p_int = int(p_file.read())
    q_int = int(q_file.read())
    n = p_int * q_int
    
    totient_n = (p_int-1) * (q_int-1)

    e_bv = BitVector(intVal = e, size = 128)
    d = int(e_bv.multiplicative_inverse(BitVector(intVal = totient_n, size = 256)))
    
    cipher_fp = open(ciphertext_file,'r')
    ciphertext_bits = BitVector(hexstring = cipher_fp.read())

    for i in range(len(ciphertext_bits)//256):
        ciphertext_bv = ciphertext_bits[256*i:256*(i+1)]

        if ciphertext_bv._getsize() > 0:
            if ciphertext_bv._getsize() < 256:
                ciphertext_bv.pad_from_right(256 - ciphertext_bv._getsize())

        plainblock = pow(int(ciphertext_bv), d, n)
        plainblock = BitVector(intVal = plainblock, size = 256)
        [left_half, right_half] = plainblock.divide_into_two()
        plainblock = BitVector(intVal = int(right_half), size = 128)

        output_file.write(plainblock.get_bitvector_in_ascii())

if __name__ == '__main__':
    
    if sys.argv[1] == '-g':

        p_fp = open(sys.argv[2],'w')
        q_fp = open(sys.argv[3],'w')

        key_generation(p_fp, q_fp)

    if sys.argv[1] == '-e':

        message_text = sys.argv[2]
        p_text = open(sys.argv[3],'r')
        q_text = open(sys.argv[4],'r')
        encrypted_txt = open(sys.argv[5], 'w')

        encrypt(message_text, p_text, q_text, encrypted_txt)

    if sys.argv[1] == '-d':

        ciphertext = sys.argv[2]
        p_text = open(sys.argv[3],'r')
        q_text = open(sys.argv[4],'r')
        decrypted_txt = open(sys.argv[5], 'w', encoding = "utf-8")

        decrypt(ciphertext, p_text, q_text, decrypted_txt)