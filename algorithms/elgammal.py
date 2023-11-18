from sympy import randprime, isprime
import random
import math
from algorithms.goodies import InputKeyError, ALPHABET

#Elgamal
#For key generation i.e. large random number

primos = [100003,100019,100043,100103,100151,100183,100207,100267,100271,100279,
100291,100343,100363,100379,100391,100403,100411,100447,100459,100483,
100511,100519,100523,100547,100559,100591,100699,100703,100747,100787,
100799,100811,100823,100847,100907,100927,100931,100943,100987,100999,
101027,101051,101063,101107,101111,101119,101159,101183,101203,101207,
101267,101279,101287,101323,101347,101359,101363,101383,101399,101411,
101419,101467,101483,101503,101527,101531,101599,101603,101611,101627,
101663,101719,101723,101747,101771,101807,101839,101863,101879,101891,
101939,101963,101987,101999,102019,102023,102031,102043,102059,102071,
102079,102103,102107,102139,102191,102199,102203,102251,102259,102299,
102359,102367,102407,102451,102499,102503,102523,102539,102547,102551,
102559,102563,102587,102607,102611,102643,102647,102667,102679,102763,
102811,102859,102871,102911,102931,102967,102983,103007,103043,103067,
103079,103087,103091,103099,103123,103171,103183,103231,103291,103307,
103319,103387,103391,103399,103423,103451,103471,103483,103511,103567,
103583,103591,103619,103643,103651,103687,103699,103703,103723,103787,
103811,103843,103867,103903,103919,103951,103963,103967,103979,103991,
104003,104047,104059,104087,104107,104119,104123,104147,104179,104183,
104207,104231,104239,104243,104287,104311,104323,104327,104347,104383,
104399,104459,104471,104479,104491,104527,104543,104551,104579,104623,
104639,104651,104659,104683,104707,104711,104723,104743,104759,104779,
104803,104827,104831,104851,104879,104891,104911,104947,104959,104971,
104987,104999,105019,105023,105031,105071,105107,105143,105167,105199,
105211,105227,105239,105251,105263,105319,105323,105331,105359,105367,
105379,105407,105467,105491,105499,105503,105527,105563,105607,105619,
105667,105683,105691,105727,105751,105767,105863,105871,105883,105899,
105907,105943,105967,105971,105983,106019,106031,106087,106103,106123,
106163,106187,106207,106219,106243,106279,106291,106303,106307,106319,
106331,106363,106367,106391,106411,106427,106451,106487,106531,106543]

def generatePrime(a=0):
    if a!=0:
        return randprime(2**(a-2),2**(a-1))
    return randprime(2**(256),2**(512))


def generatePrime(a=0):
    if a!=0:
        return randprime(2**(a-2),2**(a-1))
    return randprime(2**(256),2**(512))

def gcd(p,q):
    while q != 0:
        p, q = q, p%q
    return p

def gen_key(p):
    key= random.randint(0,p)
    while gcd(p,key)!=1:
        key=random.randint(0,p)
    return key

def exp_modular(a,b,c):
    x=1
    y=a
    while b>0:
        if b%2==0:
            x=(x*y)%c
        y=(y*y)%c
        b=int(b/2)
    return x%c

#For asymetric encryption
def elgammalEncrypt(msg,p="",g = ""):
    try:
        p = int(p)
    except:
        pass
    try:
        g = int(g)
    except:
        pass

    if p == "" :
        p = generatePrime(50)
    elif type(p) != int  or not isprime(p) :
        raise InputKeyError("p must be prime number")
    
    if g == "":
       g = random.randint(1,p-1)
    elif type(g) != int or not( 1 <= g and g <= p-1 ):
        raise InputKeyError(f"generator must be an integer between 1 and {p-1}")
    
   

    
    ct=[]
    key=gen_key(p)
    a_k=exp_modular(g,key,p)
    #h=exp_modular(a_k,key,p)
    h= exp_modular(g,key,p)
    a_k_k=exp_modular(h,key,p)
    for i in range(0,len(msg)):
        ct.append(msg[i])
    for i in range(0,len(ct)):
        ct[i]=str(a_k_k*ord(ct[i]))
    return ((ct,[p,"",key,g])) #tal vez sea a_k_k
#For decryption
def elgammalDecrypt(ct,p,key,g = ""):
    if ct == "":
        raise InputKeyError("The message is not a encrypted text")
    try:
        p = int(p)
    except:
        pass
    try:
        g = int(g)
    except:
        pass
    try:
        key = int(key)
    except:
        pass


    if p == "":
        raise InputKeyError("For decrypt must have p")
    if type(p) != int or not isprime(p):
        raise InputKeyError("p must be prime number")

    if key == "":
        raise InputKeyError("For decrypt must have the prived key")
    elif type(key) != int or not( 1 <= key and key <= p-1 ):
        raise InputKeyError(f"prived key must be an integer between 1 and {p-1}")

    if g == "":
       raise InputKeyError("For decrypt must have the generator")
    elif type(g) != int or not( 1 <= g and g <= p-1 ):
        raise InputKeyError(f"generator must be an integer between 1 and {p-1}")


    a_k = exp_modular(g,key,p)
    pt=[]
    h=exp_modular(a_k,key,p)
    for i in range(0,len(ct)):
        pt.append(chr(int(int(ct[i])/h)))

    text = ""
    for let in pt:
        text += let
    return ((text,[p,"",key,g]))


def generateGamalData(p, alpha=0):
    if alpha==0:
        alpha=random.randint(2,p) #generador
    a = gen_key(p) # clave privada
    alpha_a=exp_modular(alpha,a,p) #alpha^a
    keys = {'public_key' : [str(p),str(alpha),str(alpha_a)], 'private_key' : str(a)}
    return (keys)

# mensaje = "funciona :)"
# text, keys= elgammalEncrypt(mensaje)
# p,k,g = int(keys[0]), int(keys[1]), int(keys[2])
# print(text,p,k,g)
# print(elgammalDecrypt(text,p,k,g))




