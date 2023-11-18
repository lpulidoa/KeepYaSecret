def val(c):
    if c >= '0' and c <= '9':
        return ord(c) - ord('0')
    else:
        return ord(c) - ord('A') + 10

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)


def toDeci(str,base): #CONVIERTE BASE N A DECIMAL
    llen = len(str)
    power = 1 #Initialize power of base
    num = 0     #Initialize result
 
    # Decimal equivalent is str[len-1]*1 +
    # str[len-2]*base + str[len-3]*(base^2) + ...
    for i in range(llen - 1, -1, -1):
         
        # A digit in input number must
        # be less than number's base
        if val(str[i]) >= base:
            print('Invalid Number')
            return -1
        num += val(str[i]) * power
        power = power * base
    return num
    
    
def reVal(num):
    if (num >= 0 and num <= 9):
        return chr(num + ord('0'))
    else:
        return chr(num - 10 + ord('A'))


def fromDeci(res, base, inputNum): #CONVIERTE DECIMAL A BASE N
    # Initialize index of result
    while (inputNum > 0):
        res+= reVal(inputNum % base)
        inputNum = int(inputNum / base)
    res = res[::-1]
    return res

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

from algorithms.goodies import InputKeyError, ALPHABET
#from goodies import InputKeyError, ALPHABET
import random
from sympy import randprime, isprime


def rabinEncrypt(message, p = "",q=""):

    try:
        p = int(p)
        q = int(q)
    except:
        pass
    
    if p == "" or q == "":
        p,q = random.sample(primos, 2)
    elif type(p) != int or type(q) != int or not isprime(p) or not isprime(q):
        raise InputKeyError("p and q must be primes numbers.")
    elif p<1000 or q<1000:
        raise InputKeyError("p and q must be greater than 1000.")
    elif p%4!=3 or q%4!=3:
        raise InputKeyError("p and q must be congruent to 3 mod 4.")



    n = p*q
    message=message.upper()
    message=message.replace(" ", "")
    encrypt_text = []
    while(len(message)%3!=0):
      message=message+"C"
    for i in range(0,len(message),3):
          c=(ord(message[i])-64)*(27**2)+(ord(message[i+1])-64)*27+(ord(message[i+2])-64)
          cipher_text = pow(c,2,n)
          encrypt_text.append(cipher_text)
    return((encrypt_text,[p,q,"",""]))

def rabinDecrypt(message,p,q):
    try:
        message = [int(binario) for binario in message[1:-1].replace(" ","").split(',')]
    except:
        raise InputKeyError("The message is not a encrypted text")
    try:
        p = int(p)
        q = int(q)
    except:
        pass 
    if p == "" or q == "" :
        raise InputKeyError("For decrypt must have p and q ")
    elif type(p) != int or type(q) != int or not isprime(p) or not isprime(q):
        raise InputKeyError("p and q must be primes numbers")

    


    decrypt_list=[] #guarda los decifrados en números
    decrypt_text = ""   #se guarda el decifrado letra por letra
    decrypt_textlist=[] # guarda el decifrado de los 4 residuos
    decrypt_end=[] #guarda todos los decifrados por cada resiudos segun el número de bloques
   # convert10=0
    for k in range(0,len(message)):
        c = message[k]
        # Use Extended Euclid's Algorithm to find x and y such that px+qy=1
        (g, x, y)=egcd(p,q)
        n=p*q
        # Calculate square roots in Zp and Zq
        r=(pow(c,((p+1)//4),p))
        s=(pow(c,((q+1)//4),q))
        ###3
        #decrypt_letter = (c**priv_key)%r
         # Use the Chinese Remainder Theorem to find 4 square roots in Zn
        r1=((x*p*s)+(y*q*r))%n
        r2=((x*p*s)-(y*q*r))%n
        r3=(-r1)%n
        r4=(-r2)%n

        decrypt_list.append([r1,r2,r3,r4]) ###Lista con los números decifrados sin convertir en letras
        #convertimos cada reisudo a base 26 
        convert27_1 = fromDeci("", 27, r1)
        convert27_2 = fromDeci("", 27, r2)
        convert27_3 = fromDeci("", 27, r3)
        convert27_4 = fromDeci("", 27, r4)
        residuos27=[convert27_1,convert27_2,convert27_3,convert27_4] #construimos una lista de esos residuos base26 que será modificada por cada 3 letras
        #recorremos cada residuo 
        for j in range(0,4):
          #recorremos cada letra de cada uno de los residuos
          for i in range(0,len(residuos27[j])):
               #convertimos cada letra base 27 a ascci
               convert10= toDeci((residuos27[j][i]),27)
               convertascci=chr(convert10+64)
               decrypt_text=decrypt_text+convertascci
          decrypt_textlist.append(decrypt_text) 
          decrypt_text="" 
        decrypt_end.append(decrypt_textlist) 
        decrypt_textlist=[] 
        posibleText = ""
        text = decrypt_end
        for i in text:
            for j in i:
                if len(j)==3:
                    posibleText=posibleText+j
        text=posibleText

    return((text,[p,q,"",""]))

# mensaje = "Hola leo lindo"
# text,p1,p2 =rabinEncrypt(mensaje)
# print(text,rabinDecrypt(text,p1,p2))
#print(rabinDecrypt("[35748441, 84217329]",100931 ,105071))