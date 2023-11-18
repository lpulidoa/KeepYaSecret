from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_OAEP
from algorithms.goodies import InputKeyError
import base64

def rsaEncrypt(text, p="", q=""):
    if text == "":
        raise InputKeyError("The message is not valid.")

    if p == "" or q == "":
        key = RSA.generate(2048)
    else:
        raise InputKeyError("Prime integers and keys are randomly generated to increase the security.\nLeave the input fields empty.")

    private_key = key.export_key('PEM')
    public_key = key.publickey().exportKey('PEM')

    text = text.encode()

    rsa_public_key = RSA.importKey(public_key)
    rsa_public_key = PKCS1_OAEP.new(rsa_public_key)
    encrypted_text = rsa_public_key.encrypt(text)

    return (base64.b64encode(encrypted_text).decode(), [public_key.decode(), "", private_key.decode(), ""])


def rsaDecrypt(text, public_key, private_key):
    if text == "":
        raise InputKeyError("The message is not valid.")
    if private_key == "":
        raise InputKeyError("You should enter the private key.")
    
    try:
        rsa_private_key = RSA.importKey(private_key.encode())
    except:
        raise InputKeyError("Private key is not in the correct format.")
    rsa_private_key = PKCS1_OAEP.new(rsa_private_key)
    decrypted_text = rsa_private_key.decrypt(base64.b64decode(text.encode()))

    return (decrypted_text.decode(), [public_key, "", private_key, ""])

