# Falta analysis
import random, itertools

from algorithms.goodies import ALPHABET, InputKeyError


"""
Tanto Encrypt como Decrypt 
reciben texto cualquiera y clave(con espacios)
retornan [texto, clave]
"""


def permutationEncrypt(t: str, key=None):

    if key == None:
        key = randomKeyPermutation()
        
    k = key
    text = t
    
    if not "".join(key.split()).isdigit():
        raise InputKeyError("Key must be a permutation where numbers are separated by an space. Ex: '2 3 5 4 1'") #InputKeyError

    else:
            
        key = [int(x) for x in k.split(" ")]

        if not isNumberPermutation(key):
            raise InputKeyError("Key must be a permutation where numbers are separated by an space Ex: '2 3 5 4 1'") #InputKeyError

        text = completeWithAs(text, len(key))
        encrypted_text = performPermutation(text, key)

        return [encrypted_text, k]

def permutationDecryptKey(t: str, key: str):
    text = t
    k = key
    
    if not "".join(key.split()).isdigit():
      raise InputKeyError("ERROR : Key must be a permutation where numbers are separated by an space Ex: '2 3 5 4 1'") #InputKeyError
    else:
        key = [int(x) for x in k.split()]

        if not isNumberPermutation(key):
            raise InputKeyError("Key must be a permutation where numbers are separated by an space Ex: '2 3 5 4 1'") #InputKeyError
        if not len(text)%len(key) == 0:
            raise InputKeyError("Length of key must divide length of text") 

        inverse_key = inversePermutation(key)
        encrypted_text = performPermutation(text,inverse_key)
        k = " ".join([str(x) for x in inverse_key])

        return [encrypted_text,k]
      

# --------------------------->
# Funciones de Encrypt y Decrypt


def everyNumberJustOnce(s: list):
    for i in range(1, len(s) + 1):
        x: int = s.count(i)
        if 1 < x:
            raise InputKeyError("The key must be a permutation where numbers are separated by an space Ex: '2 3 5 4 1'") #raise
        elif x < 1:
            raise InputKeyError("The key must be a permutation where numbers are separated by an space Ex: '2 3 5 4 1'") #raise + cambiar print  por InputKeyError

    return True


def isNumberPermutation(s: list):
    if (not everyNumberJustOnce(s)):
        return False
    return True


def randomKeyPermutation():
    x = random.randint(4, 7)
    s = list(range(1, x))
    random.shuffle(s)
    if (s == list(range(1, x))):
        random.shuffle(s)
    s = [str(x) for x in s]
    s = " ".join(s)
    return s

def completeWithAs(text:list, period:int):
    total = len(text)
    if (total % period != 0):
        new_num = period - (total % period)
        text += 'A' * new_num
    return text

def performPermutation(text: list, key:list):
    total = len(text)
    period = len(key)

    encrypted_text = ""
    for i in range(int(total / period)):
        # A partir de text[i*periodo]

        for j in range(period):
            objective = key[j] - 1
            newElement = text[i * period + objective]
            encrypted_text += newElement

    return encrypted_text

def inversePermutation(key:list):
    inverse_key = [0]*len(key)
    for i in range(len(key)):
        value = key[i]
        inverse_key[value-1] = i+1
    return inverse_key


#--------------- DESENCRIPTADO --------------

#Retorna una lista de listas con los posibles mensjes y su respectiva clave:
# [['posibleMensaje1, clave1],['posibleMensaje2, clave2]]


subCadenas = ['TH','HE','IN','ER']
def frecuenciaSubString(cadena):
  frecuencias = {}
  for sub in subCadenas:
    frecuencias[sub] = ( cadena.count(sub) * 100 ) / ( len(cadena)/2 )
  return frecuencias


def permutationDecrypt(textoCifrado, key=None):

    divisores = []

    if key == None:

        for num in [4,5,6]:
            if len(textoCifrado) % num == 0:
                divisores.append(num)

        if len(divisores) == 0:
            raise InputKeyError("ERROR: Text lenght is not valid, must be 4,5 or 6 multiply") #cambiar print  por InputKeyError

        else:           
            rangeDivisores =[]

            for i in divisores:
                rangeDivisores.append(list(range(i)))

            permutaciones = []
            permutacionesStr = []

            for lista in rangeDivisores:
                permutaciones.append(list(itertools.permutations(lista)))
            
            for divisor in permutaciones:
                
                for permutacion in divisor:
                    
                    llave = ''
                    for numero in permutacion:
                        llave += str(numero +1 ) + ' '
            
                    permutacionesStr.append(llave.rstrip(llave[-1])) #Todas las posibles permutaciones
                
                    
                posiblesTextosDecifrados = []

                for posibleClave in permutacionesStr:
                    t = permutationDecryptKey(textoCifrado, posibleClave)
                
                    posiblesTextosDecifrados.append(t)

            try:
                return(posiblesTextosDecifrados)
            except:
                raise InputKeyError("Message imposible to decrypt") #cambiar print  por InputKeyError

    else:
        return permutationDecryptKey(textoCifrado,key)
    


