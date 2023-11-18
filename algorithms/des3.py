
import random as r
from PIL import Image
import numpy as np
from Cryptodome.Util.Padding import pad, unpad
from Cryptodome.Cipher import DES3
from algorithms.goodies import InputKeyError, ALPHABET

import os

dir_encr = 'web/static/uploads/encrypted/'
dir_des = 'web/static/uploads/decrypted/'

"Recibe nombre de la imagen su path, el modo y una llave que es de 24 bits"

#"""ejemplo: Des3Cifrar(fractal.png,crypto-flask\uploads\img\fractal.png,'ECB', '') 
#Nos va a guardar todo en la carpeta :
#crypto-flask\uploads\encrypted\fractal.png
#RETORNA LA LLAVE DE LA FORMA: b'\xc3\xba\x0c\x7f \xf7\x9b\x03\x97\rN(\xc3L?\xe8'
#PARA DESENCRIPTAR LA IMAGEN DEBE ESTAR EN ENCRYPTED


#"""


def des3Encrypt(nombre, mode, key, ivk):
    if(key==""):
        key = "".join(r.sample(ALPHABET, 24)).encode() 
    elif (len(key)!=24):
        raise InputKeyError("Key must have a length of 24 letters.")
    
    if(ivk==""):
        ivk = "".join(r.sample(ALPHABET, 8)).encode()
    elif (len(ivk)!=8):
        raise InputKeyError("Initial vector must have a length of 8 letters.")

    if(mode == 'ECB'):
        mod = DES3.MODE_ECB
    elif(mode == 'CBC'):
        mod = DES3.MODE_CBC
    elif(mode == 'CFB'):
        mod = DES3.MODE_CFB
    elif(mode == 'OFB'):
        mod = DES3.MODE_OFB
    elif(mode == 'CTR'):
        mod = DES3.MODE_CTR

    img_path = os.path.join(os.getcwd(), "web/static/uploads/uploaded", nombre)

    image = Image.open(img_path)
    size = image.size
    image = np.array(image)
    
    cipher = None
    if(mod != DES3.MODE_ECB and mod != DES3.MODE_CTR):
        cipher = DES3.new(key, mod, ivk)
    elif mod == DES3.MODE_CTR:
        cipher = DES3.new(key, mod, nonce=b"")
    else:
        cipher = DES3.new(key, mod)


    cripbytes = cipher.encrypt(pad(image.tobytes(), DES3.block_size))
    imgData = np.frombuffer(cripbytes)
    im = Image.frombuffer("RGB", size, imgData)
    im.save(os.path.join(os.getcwd(), dir_encr, nombre))

    return {'key': key.decode(), 'inicial_vector': ivk.decode()}




def des3Decrypt(nombre, mode, key, ivk):
    if (len(key)!=24):
        raise InputKeyError("Key must have a length of 24 letters.")
    if (len(ivk)!=8):
        raise InputKeyError("Initial vector must have a length of 8 letters.")

    if(mode == 'ECB'):
        mod = DES3.MODE_ECB
    elif(mode == 'CBC'):
        mod = DES3.MODE_CBC
    elif(mode == 'CFB'):
        mod = DES3.MODE_CFB
    elif(mode == 'OFB'):
        mod = DES3.MODE_OFB
    elif(mode == 'CTR'):
        mod = DES3.MODE_CTR

    img_path = os.path.join(os.getcwd(), "web/static/uploads/uploaded", nombre)
    image = Image.open(img_path)
    size = image.size
    image = np.array(image)
        
    cipher = None
    if(mod != DES3.MODE_ECB and mod != DES3.MODE_CTR):
        cipher = DES3.new(key, mod, ivk)
    elif mod == DES3.MODE_CTR:
        cipher = DES3.new(key, mod, nonce=b"")
    else:
        cipher = DES3.new(key, mod)

    imagebytes = image.tobytes()
    decrypbytes = cipher.decrypt(imagebytes)
    imgData = np.frombuffer(decrypbytes)
    imgData = np.frombuffer(decrypbytes, dtype="int32")
    # Image.frombuffer("RGB", size, imgData).save(dir_des + nombre)
    im = Image.frombuffer("RGB", size, imgData)
    im.save(os.path.join(os.getcwd(), dir_des, nombre))

    return {'key': key.decode(), 'inicial_vector': ivk.decode()}

