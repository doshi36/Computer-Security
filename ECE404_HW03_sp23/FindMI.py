# Homework Number: 03
# Name: Parth R Doshi 
# ECN Login: doshi36 
# Due Date: 2/2/2023
# Credit : Avinash Kak, https://stackoverflow.com/questions/2776211/how-can-i-multiply-and-divide-using-only-bit-shifting-and-adding

#!/usr/bin/env python
## FindMI.py

import sys

def MI(num, mod):
    '''
    This function uses ordinary integer arithmetic implementation of the
    Extended Euclid's Algorithm to find the MI of the first-arg integer
    vis-a-vis the second-arg integer.
    '''
    NUM = num; MOD = mod
    x, x_old = 0, 1
    y, y_old = 1, 0
    while mod:
        q = division(num, mod)
        num, mod = mod, num % mod
        x, x_old = x_old - multiply(q, x), x
        y, y_old = y_old - multiply(q, y), y
    if num != 1:
        print("\nNO MI. However, the GCD of %d and %d is %u\n" % (NUM, MOD, num))
    else:
        MI = (x_old + MOD) % MOD
        print("\nMI of %d modulo %d is: %d\n" % (NUM, MOD, MI))


def multiply(a,b):
    #Arguments:
    # * a: int value_1 to be multiplied
    # * b: int value_2 to be multiplied
    #
    # Function Decomposition: 
    #   Performs multiplication using bit shifting and returns an int

    result = 0
    is_negative = 0
    if (((a < 0) and (b >= 0)) or ((a >= 0) and (b < 0))) is True:
        is_negative = 1

    a, b = abs(a), abs(b)

    while (b != 0):
        # print(b)
        if (b % 2):
            result += a
        #leftshift
        a = a << 1
        #rightshift
        b = b >> 1
    if is_negative is 1:
        #Makes the result negative by if it is a negative result
        result = 0 - result
    return result 

def division(a, b):
    #Arguments:
    # * a: int dividend
    # * b: int divisor
    #
    # Function Decomposition: 
    #   Performs division using bit shifting and returns an int

    result = 0
    is_negative = 0

    if (((a < 0) and (b >= 0)) or ((a >= 0) and (b < 0))) is True:
        is_negative = 1
    a, b = abs(a), abs(b)

    while b <= a:
        #variable to create a copy of the divisor
        carry = b 
        #temporary variable storing the multiple of a value
        temp = 1
        #print (temp)
        while (carry << 1) <= a :
            #leftshift
            carry = carry << 1
            #leftshift
            temp = temp << 1
        result = result + temp
        a = a - carry

    if is_negative is 1:
        #Makes the result negative by if it is a negative result
        result = 0 - result
    return result

if __name__ == "__main__":
    if len(sys.argv) != 3:  
        sys.stderr.write("Usage: %s   <integer>   <modulus>\n" % sys.argv[0]) 
        sys.exit(1) 
    NUM = int(sys.argv[1])
    MOD = int(sys.argv[2])
    MI(NUM, MOD)