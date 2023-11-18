from algorithms.goodies import ALPHABET, InputKeyError
import random

def caesarEncrypt(text:str, key=None):
  if key == None:
    key = random.randint(1, len(ALPHABET)-1)
  elif key.isdigit():
    key = int(key) 

  if isinstance(key, int) and 1 <= key <=25:
    # Devuelve el texto encriptado y la llave
    return (''.join([ALPHABET[(ALPHABET.find(c) + key) % len(ALPHABET)] for c in text]), key)
  else:
    raise InputKeyError("Your key should be an integer between 0 and 25.")

def caesarDecrypt(text:str, key=None)->list:
  if key == None:
    return [
      dict(
        key=i, 
        message=''.join([ALPHABET[(ALPHABET.find(c) - i) % len(ALPHABET)] for c in text])
        ) for i in range(1, len(ALPHABET))
    ]

  if key.isdigit():
    key = int(key)
    return (''.join([ALPHABET[(ALPHABET.find(c) - key) % len(ALPHABET)] for c in text]), key)
  else:
    raise InputKeyError("Your key should be an integer between 0 and 25.")