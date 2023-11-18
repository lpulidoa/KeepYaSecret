#Cryptoanalysis de una sola palabra larga?

import math
import random
import sympy

#from algorithms.goodies import InputKeyError
from algorithms.goodies import InputKeyError
"""
Encrypt y Decrypt reciben (size: int, text: str, key: str)
 donde size es la dimensión de las matrices
 y los textos text y key(solo letras mayúsculas)
 En encrypt se puede no escribir key
Devuelven lista [encriptedText, key], ambos valores son strings de letras mayúsculas

Cryptoanalysis recibe size: int, encryptedTexts: list, plainTexts: list
donde size es la dimensión de las matrices
y encryptedTexts y plainTexts son listas de textos encriptados y claros, respectivamente
Cada una debe constar de size palabras, de las cuales solo se toma en cuenta las primera size letras
Devuelve clave
"""

def hillEncrypt(text: str, key = None):
    checkText(text)
    # checkKey(key)
    if key == None:
        if len(text)<4:
            size = 2
        else:
            size = random.randint(2, 4)
        keyMatrix = randomKeyMatrix(size)
    else:
        size = int(math.sqrt(len(key)))
        keyMatrix = getMatrix(key, size)
        isInvertibleMod(keyMatrix, 26, "key")

    textMatrix = getTextMatrix(text, size)
    encryptedMatrix = textMatrix * keyMatrix % 26

    encriptedText = getText(encryptedMatrix)
    keyText = getText(keyMatrix)
    return ("".join(encriptedText), keyText)

def hillDecrypt( text: str, key: str):
    size = int(math.sqrt(len(key)))
    keyMatrix = getMatrix(key, size, True)
    textVector = getTextMatrix(text, size)

    isInvertibleMod(keyMatrix, 26, "key")
    inverseKeyMatrix = keyMatrix.inv_mod(26)
    decipherMatrix = textVector*inverseKeyMatrix % 26

    inverseKey = getText(inverseKeyMatrix)
    decryptedText = getText(decipherMatrix)

    return (decryptedText, inverseKey)

def hillCryptoAnalysis( encryptedLines: str, plainLines: str):
    encryptedTexts = encryptedLines.split("\n")
    plainTexts = plainLines.split("\n")

    encryptedTexts = list(filter(lambda i: i != "", encryptedTexts))
    plainTexts = list(filter(lambda i: i != "", plainTexts))

    size = len(encryptedTexts)
    checkAnalysisInput(encryptedTexts, plainTexts, size)

    encrypted_list = []
    plain_list = []

    for i in range(size):
        encrypted_list.append(getMatrix(encryptedTexts[i][0:size], size))
        plain_list.append(getMatrix(plainTexts[i][0:size], size))

    encrypted_matrix = sympy.Matrix(encrypted_list)
    plain_matrix = sympy.Matrix(plain_list)
    key_matrix = solveKey(encrypted_matrix, plain_matrix)
    y = plain_matrix*key_matrix%26
    return getText(key_matrix)

def randomKeyMatrix(size: int):
    matrix = sympy.randMatrix(size, min=0, max=25, symmetric=True)
    while math.gcd(matrix.det(), 26) != 1:
        matrix = sympy.randMatrix(size, min=0, max=25, symmetric=True)
    return matrix

#---------------> Matrices

def solveKey(encrypted_matrix: sympy.Matrix, plain_matrix: sympy.Matrix):
    isInvertibleMod(plain_matrix, 26, "plaintexts")
    inv_plain = plain_matrix.inv_mod(26)
    y = plain_matrix * inv_plain %26
    key = inv_plain * encrypted_matrix % 26
    return key

def isInvertibleMod(matrix: sympy.Matrix, n: int , s=""):
    if matrix.rows != matrix.cols:
        raise InputKeyError(s + " length must be a squared number")
    det_k = matrix.det()
    if math.gcd(det_k, n) > 1:
        raise InputKeyError(
            "The determinant of the " + s + " associated matrix must be comprime with 26"
        )

#---------------> Checkers

def checkAnalysisInput(encryptedTexts: list, plainTexts: list, n: int):
    if n not in range(2, 5):
        raise InputKeyError("This page works with up to 4 encrypted texts")
    if len(encryptedTexts) != len(encryptedTexts):
        raise InputKeyError("Write the same ammount of plain texts and encrypted texts")

def checkText(text:str):
    if len(text)<2:
        raise InputKeyError("Text to be encrypted must be at least two characters long")

def checkKey(key: str):
    onlyUppercase_letters(key)
    if len(key) > 16:
        raise InputKeyError("We work with keys of up to 16 characters")
    if len(key)<2:
        raise InputKeyError("Key must be at least 2 characters long")
    s = int(math.sqrt(len(key)))
    if s*2!=len(key):
        raise InputKeyError("Key length must be a squared number")
    
def onlyUppercase_letters(s):
    for i in s:
        if (ord(i) < 65 or 91 < ord(i)):
            raise InputKeyError("Key must contain only uppercase letters")
    return True

#---------------> Converters

def getMatrix(text: list, size: int, square=False):
    text_l = list(text)
    matrix_num = []
    for i in range(0, len(text_l), size):
        charList = text_l[i:i+size]
        intList = [ord(j) % 65 for j in charList]
        matrix_num.append(intList)

        #if square and len(intList) != size:
         #   raise InputKeyError("Key lenght must be a square")

    return sympy.Matrix(matrix_num)

def getTextMatrix(text: str, size: int):
    #divide list into strings of size length
    text_l = [text[i:i+size] for i in range(0, len(text), size)]
    if len(text_l[-1]) < size:
        text_l[-1] = text_l[-1] + 'A'*(size-len(text_l[-1]))

    for i in range(len(text_l)):
        text_l[i] = [ord(i) % 65 for i in text_l[i]]

    return sympy.Matrix(text_l)

def getText(keyMatrix: sympy.Matrix):
    return "".join([chr(j+65) for j in keyMatrix])



# # t = "WORLDISFUNINNOS"
# # k = "NINELETTE"

# b = hillEncrypt(t)
# bx = hillDecrypt(b[0], b[1])

# "Example invertible 3x3 matrix mod 26 fxampjtqo"
# p_t = """
# FXA
# MPJ
# TQOV"""
# e_t = """BHB
# XQS
# FWD"""
# y = [hillEncrypt(i, k) for i in p_t]
# x = hillCryptoAnalysis(e_t, p_t) # Debe ser k= NINELETTE
# #print(x)
