from Cryptodome.PublicKey import ECC
import random
from sympy import randprime, isprime
import random
import math
from algorithms.goodies import InputKeyError, ALPHABET,primos
import random
import ast

p = 2**255 - 19

def charToCoord(char_):
    m = str(ord(char_))
    if ((len(m) % 2) != 0):
        m1 = int(m[:(len(m)//2)+1])
        m2 = int(m[len(m)//2+1:])
    else:
        m1 = int(m[:(len(m)//2)])
        m2 = int(m[len(m)//2:])

    return m1, m2


def EGECEncrypt(text, k, a):
    encrypted = []
    alpha = ECC.generate(curve='ed25519')

    if k == "":
        k = random.randint(0, 10000)
    if a == "":
        a = random.randint(2, p-1)
    elif int(a)>p:
        raise InputKeyError("a must be a number between 0 and (2**255) - 19.")

    a = int(a)
    k = int(k)

    alpha_x = int(alpha.pointQ.x)
    alpha_y = int(alpha.pointQ.y)

    beta_x = (alpha_x*a) % p
    beta_y = (alpha_y*a) % p

    k = random.randint(1, 10000)

    y0_x = k*alpha_x
    y0_y = k*alpha_y

    for char_ in text:
        x1, x2 = charToCoord(char_)
        y1 = k * beta_x * x1
        y2 = k * beta_y * x2
        encrypted.append((y1, y2))

    return (encrypted, ["", "", a, (y0_x, y0_y)])
# {"a": a,
#             "y0": (y0_x, y0_y),
#             "encrypted": encrypted
#             }


def EGECDecrypt(text, y0, a):
    if text == "":
        raise InputKeyError("You must enter a ciphered text to decrypt.")
    
    if a == "":
        raise InputKeyError("You must enter a private key, a.")
    else:
        a = int(a)
    
    try: 
        text = ast.literal_eval(text)
    except:
        raise InputKeyError("Ciphered text is not a string representation of a list.")
    
    try:
        y0 = ast.literal_eval(y0)
    except:
        raise InputKeyError("y0 point is not in its tuple representation.")
    
    decrypted = ""
    c1 = a*y0[0]
    c2 = a*y0[1]

    c1_inv = pow(c1, -1, p)
    c2_inv = pow(c2, -1, p)
    
    for y1, y2 in text:
        s = str((y1 * c1_inv) % p) + str((y2 * c2_inv) % p)
        decrypted += chr(int(s))
        
    return (decrypted, ["", "", a, y0])

