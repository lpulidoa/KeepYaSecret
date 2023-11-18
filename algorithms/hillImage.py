import cv2 as cv
import numpy as np
import os
from algorithms.goodies import InputKeyError
# from flask import url_for
#from goodies import InputKeyError



"""
dir = 'crypto-flask/algorithms/hill-images/'
img_dir = 'img/'
key_dir = 'key-img/'
enc_dir = 'encrypted-img/'
dec_dir = 'decrypted-img/'
"""

dir = 'web/static/uploads/'
img_dir = 'uploaded/'
key_dir = 'key/'
enc_dir = 'encrypted/'
dec_dir = 'decrypted/'

#ejemplo de llave: b'\xc3\xba\x0c\x7f \xf7\x9b\x03\x97\rN(\xc3L?\xe8'

"""
hillEncrypt recibe (s: str, path, k="") donde s es el nombre de la imagen a encriptar, path el path   y k es el nombre de la imagen clave
devuelve la llave y  guarda las imagenes encrypted y key en la carpeta hill-images
hillDecrypt recibe (s: str,path, k: str) donde s y k son los descritos arriba.
devuelve la llave y guarda las imagenes decrypted y key en la carpeta hill-images



NECESARIO SIEMPRE PONER ESTO ANTES:

b = os.getcwd() + '/'
os.chdir(b+dir)

EJEMPLO


b = os.getcwd() + '/'
os.chdir(b+dir)
hillImgEncrypt('regalo.png')
hillImgDecrypt('regalo.png','regalo.png')
"""



def isInvolutory(a: np.ndarray, mod: int):
    isSquare(a)
    y = np.identity(a.shape[0])
    x = np.matmul(a % mod, a % mod) % mod
    if np.array_equal(x, y):
        return
    raise InputKeyError("Error de código")


def involutoryMatrixOf(a11: np.ndarray):
    a22 = -a11
    y = np.identity(a11.shape[0])
    a12 = y - a11
    a21 = y + a11
    a1 = np.concatenate((a11, a21))
    a2 = np.concatenate((a12, a22))
    a = np.concatenate((a1, a2), axis=1)
    return a


def isSquare(a: np.ndarray):
    if a.shape[0] != a.shape[1]:
        raise InputKeyError("Encrypted image and key image must be squared")


def read(s: str):
    if s.split(".")[-1] != "png":
        raise InputKeyError(s+"image format must be png")

    coloredIm = cv.imread(s)

    if coloredIm is None:
        raise InputKeyError("There´s no image with the name "+s+" in " + os.getcwd())

    return coloredIm


def hillImgEncrypt(s: str, k=""):
    mod = 256
    img_path = os.path.join(os.getcwd(), "web/static/uploads/uploaded", s)
    colored_img = read(img_path)

    n = min(colored_img.shape[0], colored_img.shape[1])
    if n % 2 != 0:
        n = n-1
    colored_img = colored_img[0:n, 0:n]

    if k == "":
        m = int(n/2)
        key_orig = np.random.randint(0, mod, (m, m, 3))
        cv.imwrite(os.path.join(os.getcwd(), "web/static/uploads/key", s), key_orig)
        key_folder = "key/"

    else:
        m = int(n/2)
        key_img_path = os.path.join(os.getcwd(), "web/static/uploads/uploaded_key", k)
        key_orig = read(key_img_path)
        key_orig = cv.resize(key_orig, (m, m))
        key_folder = "uploaded_key/"

    key = [involutoryMatrixOf(i) for i in cv.split(key_orig)]
    [isInvolutory(i, mod) for i in key]

    e = [np.matmul(i, j) % mod for i, j in zip(cv.split(colored_img),key)]
    encrypted = cv.merge(e)

    cv.imwrite(os.path.join(os.getcwd(), "web/static/uploads/encrypted", s), encrypted)
    # return (cv.imencode('.png', encrypted), cv.imencode('.png', key_orig))
    return key_folder


def hillImgDecrypt(s: str, k: str):
    if k=="":
        raise InputKeyError("Key required")
    mod = 256
    img_path = os.path.join(os.getcwd(), "web/static/uploads/uploaded", s)
    encrypted = read(img_path)

    n = encrypted.shape[0]
    if n % 2 != 0:
        n = n-1

    m = int(n/2)
    key_img_path = os.path.join(os.getcwd(), "web/static/uploads/uploaded_key", k)
    key_orig = read(key_img_path)
    key_orig = cv.resize(key_orig, (m, m))

    isSquare(encrypted)
    isSquare(key_orig)

    key = [involutoryMatrixOf(i) for i in cv.split(key_orig)]
    [isInvolutory(i, mod) for i in key]

    d = [np.matmul(i, j) % mod for i, j in zip(cv.split(encrypted),key)]
    decrypted = cv.merge(d)

    cv.imwrite(os.path.join(os.getcwd(), "web/static/uploads/decrypted", s), decrypted)
    
    return "uploaded_key/"





# hillImgEncrypt('image.png')
