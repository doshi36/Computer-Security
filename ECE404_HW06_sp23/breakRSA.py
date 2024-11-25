# Homework Number: 06 - Part 2
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

def solve_pRoot(p, x): 
	'''
	Implement binary search to find the pth root of x. The logic is as follows:
	1). Initialize upper bound to 1
	2). while u^p <= x, increment u by itself
	3). Intialize lower bound to u//2
	4). While the lower bound is smaller than the upper bound:
        a). Compute the midpoint as (lower + upper) / 2
        b). Exponentiate the midpoint by p
        c). if lower bound < midpoint and midpoint < x, then set the new lower bound to midpoint
        d). else if upperbown > midpoint and midpoint > x, then set the new upper bown to midpoint
        e). else return the midpoint
	5). If while loop breaks before returning, return midpoint + 1

	Author: Joseph Wang
		wang3450 at purdue edu

	'''

	u = 1
	while u ** p <= x: u *= 2

	l = u // 2
	while l < u:
		mid = (l + u) // 2
		mid_pth = mid ** p
		if l < mid and mid_pth < x:
			l = mid
		elif u > mid and mid_pth > x:
			u = mid
		else:
			return mid
	return mid + 1

def gcd(a,b):

    a,b = int(a),int(b)
    while b:                                             
        a,b = b, a % b
    return a

def key_generation():  

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
    
    return(p,q)

def encrypt(plaintext_file, enc1_file, enc2_file, enc3_file, n_file):

    e = 3

    for i in range(3):
        p,q = key_generation()
        plaintext_bits = BitVector(filename = plaintext_file)

        while plaintext_bits.more_to_read:

            plaintext_bv = plaintext_bits.read_bits_from_file(128)
            if plaintext_bv._getsize() > 0:
                if plaintext_bv._getsize() < 128:
                    plaintext_bv.pad_from_right(128 - plaintext_bv._getsize())
            
            n = p * q
            
            cipherblock = pow(int(plaintext_bv),e,n)
            cipherblock = BitVector(intVal = cipherblock, size = 256)
            if i == 0: 
                enc1_file.write(cipherblock.get_hex_string_from_bitvector())
            if i == 1:
                enc2_file.write(cipherblock.get_hex_string_from_bitvector())
            if i == 2:
                enc3_file.write(cipherblock.get_hex_string_from_bitvector())
                
        n_file.write(str(n))
        n_file.write('\n')

def cracked(enc1_file, enc2_file, enc3_file, n_file, cracked_file):

    n1 = int(n_file.readline())
    n2 = int(n_file.readline())
    n3 = int(n_file.readline())

    N = n1 * n2 * n3

    N1 = (n2 * n3)
    n1_bv = BitVector(intVal = N1)
    N2 = n1 * n3
    n2_bv = BitVector(intVal = N2)
    N3 = n1 * n2
    n3_bv = BitVector(intVal = N3)

    c1 = int(n1_bv.multiplicative_inverse(BitVector(intVal = n1))) * N1
    c2 = int(n2_bv.multiplicative_inverse(BitVector(intVal = n2))) * N2
    c3 = int(n3_bv.multiplicative_inverse(BitVector(intVal = n3))) * N3

    cipher_fp_1 = open(enc1_file,'r')
    cipher_fp_2 = open(enc2_file,'r')
    cipher_fp_3 = open(enc3_file,'r')

    ciphertext_bits_1 = BitVector(hexstring = cipher_fp_1.read())
    ciphertext_bits_2 = BitVector(hexstring = cipher_fp_2.read())
    ciphertext_bits_3 = BitVector(hexstring = cipher_fp_3.read())

    for i in range(len(ciphertext_bits_1)//256):
        ciphertext_bv_1 = ciphertext_bits_1[256*i:256*(i+1)]
        ciphertext_bv_2 = ciphertext_bits_2[256*i:256*(i+1)]
        ciphertext_bv_3 = ciphertext_bits_3[256*i:256*(i+1)]

        m_cube =  c1 * int(ciphertext_bv_1) + c2 * int(ciphertext_bv_2) + c3 * int(ciphertext_bv_3)
        output = solve_pRoot(3, m_cube % N)
        output1 = BitVector(intVal = output, size = 256)
        cracked_file.write(output1[128:].get_bitvector_in_ascii())

if __name__ == '__main__':

    if sys.argv[1] == '-e':

        message_text = sys.argv[2]
        enc1_txt = open(sys.argv[3], 'w')
        enc2_txt = open(sys.argv[4], 'w')
        enc3_txt = open(sys.argv[5], 'w')
        n_1_2_3_txt = open(sys.argv[6], 'w')

        encrypt(message_text, enc1_txt, enc2_txt, enc3_txt, n_1_2_3_txt)

    if sys.argv[1] == '-c':

        enc1_txt = sys.argv[2]
        enc2_txt = sys.argv[3]
        enc3_txt = sys.argv[4]
        n_1_2_3_txt = open(sys.argv[5], 'r')
        cracked_txt = open(sys.argv[6], 'w', encoding = "utf-8")

        cracked(enc1_txt, enc2_txt, enc3_txt, n_1_2_3_txt, cracked_txt)