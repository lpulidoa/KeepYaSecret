import random
import string
from algorithms.goodies import InputKeyError

abecedario = list(string.ascii_uppercase)

"""
Tanto Encrypt como Decrypt reciben texto y clave(opcional)
Y devuelven lista [texto, clave]

Cryptoanalysis recibe texto
Y devuelve lista [lista_frecuencia_de_letras, dict_frecuencia_de_digramas]
"""


def substitutionEncrypt(t: str, k=None):
    """
    Recibe texto t de solo letras mayúsculas
    e.g. HOLAMUNDO

    Puede recibir clave k permutación del abecedario en mayúsculas
    e.g. BACDEFGHIJKLMNOPQRSTUVWXYZ
         ABCDEFGHIJKLMNOPQRSTUVWXYZ

    Devuelve lista de texto encriptado y clave
    [texto,clave]
    e.g. HOLBMUNDO
    """
    encrypted_text = ""
    text = list(t)

    if k is None:
        key = randomKey()
        # print("key:", "".join(key))
    else:
        key = list(k)

    if not isPermutation(key):
        raise InputKeyError("The key must be a permutation of the 26-letters latin alphabet.")

    if not onlyUppercase_letters(text):
        InputKeyError("The key must be all in caps.")

    for i in text:
        place: int = ord(i) - ord('A')
        b = key[place]
        encrypted_text += key[place]

    key_text = ""
    for letter in key:
        key_text += letter + " "

    return (str(encrypted_text), key_text)


def substitutionDecrypt(t: str, k=" "):
    """
    Recibe texto t de solo letras mayúsculas
    e.g. HOLBMUNDO
    Recibe clave k permutación del abecedario en mayúsculas
    e.g. BACDEFGHIJKLMNOPQRSTUVWXYZ

    Devuelve lista de texto desencriptado y clave
    e.g. [HOLAMUNDO,BACDEFGHIJKLMNOPQRSTUVWXYZ]
    """

    decrypted_text = ""
    text = list(t)

    if k == " ":
        key = abecedario.copy()
        random.shuffle(key)
        print("key:", key)
    else:

        key = [x for x in k.split()]
        print(key)
    if (not isPermutation(key) or not onlyUppercase_letters(text)):
        return

    for i in text:
        place: int = key.index(i)
        decrypted_text += chr(place + ord('A'))
    
    key_text = ""
    for letter in key:
        key_text += letter + " "


    return [str(decrypted_text), key_text]


def substitutionCryptanalysis(text: str):
    return [frequencyOfLetters(text), mostCommon(frequencyOfDigraphs(text))]


# --------------------------->
# Funciones de Encrypt y Decrypt


def onlyUppercase_letters(s):
    for i in s:
        if (ord(i) < 65 or 91 < ord(i)):
            raise InputKeyError("The key and text must contain only uppercase letters")
            return False
    return True


def everyElementJustOnce(s: list):
    for i in abecedario:
        x: int = s.count(i)
        if (x > 1):
            raise InputKeyError("There's a duplicated '" + i + "' in key")
            return False
        elif (x < 1):
            raise InputKeyError("The letter '" + i + "' is missing from key")

    return True


def isPermutation(s: list):
    if len(s) != 26:
        raise InputKeyError("Lenght must be 26")
        # return False
    if onlyUppercase_letters(s) and everyElementJustOnce(s):
        return True
    return False


def randomKey():
    s = abecedario.copy()
    random.shuffle(s)
    return s


# --------------------------->
# Funciones de criptoanalisis

def mostCommon(d:dict):
    newD = {}
    for key, value in d.items():
        if value > 1:
            newD[key] = value
    return newD


def frequencyOfLetters(t: str):
    dict = {}
    for i in t:
        if dict.get(i) == None:
            dict[i] = 1
        else:
            dict[i] += 1
    return dict


def frequencyOfDigraphs(t: str):
    # List of 10 most common pairs
    # 1 time doesnt count
    dict = {}
    for i in range(len(t) - 1):
        digraph = t[i:i + 2]
        if dict.get(digraph) == None:
            dict[digraph] = 1
        else:
            dict[digraph] += 1

    return dict


# a = substitutionEncrypt("XUA", "VKWBXLYFZMDNOCPHGERISATJUQ")
# b = subtitutionEncrypt("XA")
# ax = substitutionDecrypt(a[0], a[1])
#ay = substitutionCryptoanalysis("AAACBABA")

