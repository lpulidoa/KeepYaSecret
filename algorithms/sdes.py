import math
import random
from algorithms.goodies import InputKeyError
#from algorithms.goodies import InputKeyError


p8_table = [6, 3, 7, 4, 8, 5, 10, 9]
p10_table = [3, 5, 2, 7, 4, 10, 1, 9, 8, 6]
p4_table = [2, 4, 3, 1]
IP = [2, 6, 3, 1, 4, 8, 5, 7]
IP_inv = [4, 1, 3, 5, 7, 2, 8, 6]
expansion = [4, 1, 2, 3, 2, 3, 4, 1]
s0 = [[1, 0, 3, 2], [3, 2, 1, 0], [0, 2, 1, 3], [3, 1, 3, 2]]
s1 = [[0, 1, 2, 3], [2, 0, 1, 3], [3, 0, 1, 0], [2, 1, 0, 3]] 



"""

    DES
    Reciben 3 parametros: texto plano, funciona con Mayusculas y signos
    la llave que es una cadena binaria de longitud 10, opcional
    un modo que sabrá dios que es.

    Retorna un diccionario con lista de longitud del texto original (incluye espacios) donde cada elemento es una cadena binaria
    y la llave  de la siguiente forma {'encrypted_text': valor, 'key': valor}

    EJEMPLO:
    SdesEncrypt("h ola","1010100000","ECB")
    {'encrypted_text': ['11101010', '11111111', '10101111', '01011111'], 'key': '1110000000'}


    DECODIFICADO  

    NECESARIO HABER CORRIDO EL CODIGO PARA CODIFICAR  ANTEEES SI NO NO DECODIFICA
    Recibe una lista de textos binarios
    llave de desencriptamiento, opcional
    Modo

    retorna un string

    EJEMPLO
    desDecrypt(['01001110', '01100000', '00111111', '11001111', '10011111'],"","ECB")
    {'encrypted_text': 'hola', 'key': '1101111011'}



"""

def sdesEncrypt(text, key, mode):
    
    if(key==""):
        for i in range(10):
            key+=str(random.randint(0, 1))
    else:
        if not (all([item.isdigit() for item in key]) and len(key) == 10):
            raise InputKeyError(f"Key must be a binar number with length 10 ")

    keys = GeneratedKey(key)

    file_out = open("key.txt", "w")
    file_out.write(key)
    file_out.close()

    textCript=None

    if(mode == 'ECB'):
        return ( S_DES_ENCRYPT_ECB(text, keys) ,  key)
    elif(mode == 'CBC'):
        textCript, ivk = S_DES_ENCRYPT_CBC(text, keys)
    elif(mode == 'CFB'):
        textCript, ivk = S_DES_ENCRYPT_CFB(text, keys)
    elif(mode == 'OFB' or mode == 'CTR'):
        textCript, ivk = S_DES_ENCRYPT_OFB(text, keys)

    file_out = open("ivk.txt", "w")
    file_out.write(ivk)
    file_out.close()

    return ( textCript ,  key)



def sdesDecrypt(text, key, mode):

    if(key == ""):
      raise InputKeyError("It is not possible decrypt with out a key :(")
    else:
        if not (all([item.isdigit() for item in key]) and len(key) == 10):
          raise InputKeyError(f"Key must be a binar number with length 10")
    keys = GeneratedKey(key)

    if(mode == 'ECB'):
        return (S_DES_DESENCRYPT_ECB(text, keys),key)
    else:
        file_in = open("ivk.txt", "r")
        ivk = file_in.read()
        file_in.close()
        textCript = None
        if(mode == 'CBC'):
            textCript = S_DES_DESENCRYPT_CBC(text, keys,ivk)

        elif(mode == 'CFB'):
            textCript = S_DES_DESENCRYPT_CFB(text, keys,ivk)
        elif(mode == 'OFB' or mode == 'CTR'):
            textCript = S_DES_DESENCRYPT_OFB(text, keys,ivk)
        return (textCript,key)



def apply_table(inp, table):
    #pa las permutaciones
    res = ""
    for i in table:
        res += inp[i - 1]
    return res


def left_shift(data):
   # pa mover a la izquierda
    return data[1:] + data[0]


def XOR(a, b):
    res = ""
    for i in range(len(a)):
        if a[i] == b[i]:
            res += "0"
        else:
            res += "1"
    return res


def apply_sbox(s, data):
    row = int("0b" + data[0] + data[-1], 2)
    col = int("0b" + data[1:3], 2)
    return bin(s[row][col])[2:]


def function(expansion, s0, s1, key, message):
    left = message[:4]
    right = message[4:]
    temp = apply_table(right, expansion)
    temp = XOR(temp, key)
    l = apply_sbox(s0, temp[:4])  # noqa: E741
    r = apply_sbox(s1, temp[4:])
    l = "0" * (2 - len(l)) + l  # noqa: E741
    r = "0" * (2 - len(r)) + r
    temp = apply_table(l + r, p4_table)
    temp = XOR(left, temp)
    return temp + right


def toBinary(a):
  l,m=[],[]
  for i in a:
    l.append(ord(i))
  for i in l:
    m.append(int(bin(i)[2:]))
  return m
def toString(bits):
 n = int(bits, 2)
 return(n.to_bytes((n.bit_length() + 7) // 8, 'big').decode())
 

def SDES_ENCRIPTAR(message,keys):
    message=message.replace(" ", "")
    key1=keys[0]
    key2=keys[1]
    # encryption
    temp = apply_table(message, IP)
    temp = function(expansion, s0, s1, key1, temp)
    temp = temp[4:] + temp[:4]
    temp = function(expansion, s0, s1, key2, temp)
    CT = apply_table(temp, IP_inv)
    return CT

def SDES_DESENCRIPTAR(CT,keys):
    # decryption
    key1=keys[0]
    key2=keys[1]
    temp = apply_table(CT, IP)
    temp = function(expansion, s0, s1, key2, temp)
    temp = temp[4:] + temp[:4]
    temp = function(expansion, s0, s1, key1, temp)
    PT = apply_table(temp, IP_inv)
    return PT

def GeneratedKey(key):
    temp = apply_table(key, p10_table)
    left = temp[:5]
    right = temp[5:]
    left = left_shift(left)
    right = left_shift(right)
    key1 = apply_table(left + right, p8_table)
    left = left_shift(left)
    right = left_shift(right)
    left = left_shift(left)
    right = left_shift(right)
    key2 = apply_table(left + right, p8_table)
    keys=[key1,key2]
    return keys

def S_DES_ENCRYPT_ECB(message,keys):
  TextoEncriptado=[]
  message2=toBinary(message)
  for i in range(len(message2)):
    while(len(str(message2[i]))!=8):
     message2[i]=("0"+str(message2[i]))
    TextoEncriptado.append(SDES_ENCRIPTAR(str(message2[i]),keys))
  return(TextoEncriptado)

def S_DES_DESENCRYPT_ECB(TextoEncriptado,keys):
  plaintexto=''
  for i in range(len(TextoEncriptado)):
   plaintextobinary=SDES_DESENCRIPTAR(TextoEncriptado[i],keys)
   plaintexto=toString(plaintextobinary)+plaintexto
  return(plaintexto[::-1])

def S_DES_ENCRYPT_CBC(message,keys):
  IV=''
  for i in range(8):
     IV=str(random.randint(0, 1))+IV
  TextoEncriptado=[]
  message3=toBinary(message)
  while(len(str(message3[0]))!=8):
     message3[0]=("0"+str(message3[0]))
  message3[0]=XOR(str(message3[0]),IV)
  for i in range(len(message3)):
    if(i>0):
     while(len(str(message3[i]))!=8):
      message3[i]=("0"+str(message3[i]))
     TextoEncriptado.append(SDES_ENCRIPTAR(XOR((str(message3[i])),TextoEncriptado[i-1]),keys))
    elif(i==0):
      TextoEncriptado.append(SDES_ENCRIPTAR((str(message3[i])),keys))
  return TextoEncriptado,IV

def S_DES_DESENCRYPT_CBC(TextoEncriptado,keys,IV):
  plaintexto=''
  for i in range(len(TextoEncriptado)):
    if(i==0):
     plaintextobinary=XOR(SDES_DESENCRIPTAR(TextoEncriptado[i],keys),IV)
     plaintexto=toString(plaintextobinary)+plaintexto
    else:
     plaintextobinary=XOR(SDES_DESENCRIPTAR(TextoEncriptado[i],keys),TextoEncriptado[i-1])
     plaintexto=toString(plaintextobinary)+plaintexto
  return(plaintexto[::-1])

def S_DES_ENCRYPT_CFB(message,keys):
  VI=''
  for i in range(8):
     VI=str(random.randint(0, 1))+VI
  message4=toBinary(message)
  TextoEncriptado=[]
  for i in range(len(message4)):
    if(i==0):
        while(len(str(message4[0]))!=8):
          message4[0]=("0"+str(message4[i]))
        TextoEncriptado.append(XOR((SDES_ENCRIPTAR(VI,keys)),str(message4[0])))
    else:
        while(len(str(message4[i]))!=8):
           message4[i]=("0"+str(message4[i]))
        TextoEncriptado.append(XOR(SDES_ENCRIPTAR(TextoEncriptado[i-1],keys),str(message4[i])))
  return(TextoEncriptado,VI)

def S_DES_DESENCRYPT_CFB(TextoEncriptado,keys,VI):
  plaintexto=''
  for i in range(len(TextoEncriptado)):
    if(i==0):
      letraEncriptada=SDES_ENCRIPTAR(VI,keys)
      plaintextobinary=XOR(letraEncriptada,TextoEncriptado[0])
      plaintexto=toString(plaintextobinary)
    else:
       plaintextobinary=XOR(SDES_ENCRIPTAR(TextoEncriptado[i-1],keys),TextoEncriptado[i])
       plaintexto=toString(plaintextobinary)+plaintexto
  return(plaintexto[::-1])

def S_DES_ENCRYPT_OFB(message,keys):
  VI=''
  for i in range(8):
     VI=str(random.randint(0, 1))+VI
  message4=toBinary(message)
  TextoEncriptado=[]
  Cifrado_anterior=[]
  for i in range(len(message4)):
    if(i==0):
        while(len(str(message4[0]))!=8):
          message4[0]=("0"+str(message4[i]))
        cifrado=SDES_ENCRIPTAR(VI,keys)
        Cifrado_anterior.append(cifrado)
        TextoEncriptado.append(XOR(cifrado,str(message4[0])))
    else:
        while(len(str(message4[i]))!=8):
           message4[i]=("0"+str(message4[i]))
        cifrado=SDES_ENCRIPTAR(Cifrado_anterior[i-1],keys)
        Cifrado_anterior.append(cifrado)
        TextoEncriptado.append(XOR(cifrado,str(message4[i])))
  return(TextoEncriptado,VI)

def S_DES_DESENCRYPT_OFB(TextoEncriptado,keys,VI):
  plaintexto=''
  cifrado_anterior=[]
  for i in range(len(TextoEncriptado)):
    if(i==0):
      letraEncriptada=SDES_ENCRIPTAR(VI,keys)
      cifrado_anterior.append(letraEncriptada)
      plaintextobinary=XOR(letraEncriptada,TextoEncriptado[0])
      plaintexto=toString(plaintextobinary)
    else:
       cifrado1=SDES_ENCRIPTAR(cifrado_anterior[i-1],keys)
       cifrado_anterior.append(cifrado1)
       plaintextobinary=XOR(cifrado1,TextoEncriptado[i])
       plaintexto=toString(plaintextobinary)+plaintexto
  return(plaintexto[::-1])

#text = "['10100110', '10001110', '11100011', '00101110']"
#text = [binario[1:-1] for binario in text[1:-1].replace(" ","").split(',') ]
#print(sdesEncrypt('hola','','ECB'))
#print(sdesDecrypt(text,"1101111110","ECB"))



