### NOTES NOTES NOTES
### message to be encoded: get it from a file whose location is given as option to script
### for now, get msg from local string...
### END NOTES END NOTES END NOTES

### include AES, Random from crypto lib

from Crypto.Cipher import AES 
from Crypto import Random
from struct import *
import binascii

def pad(array,block_size):
  i = block_size - len(array)%block_size
  return array + bytes(chr(i),"ascii")*i

def unpad(array):
  return array[:-1*int.from_bytes(array[-1:], byteorder='big')]

### return XOR of bytearrays s,t
def xor(s,t):
  return bytes(x^y for x,y in zip(s,t))

### transfer bytes object to string of hex digits
def ba_to_hex(s):
  return "".join("%02x" % b for b in s)


### Encryption Algorithm, CBC, with random IV, using AES-128
### key & plain text should be provided as bytes objects
### returns encrypted padded msg with IV prepended
def encrypt_aes_cbc(key,msg):
  
  ### pad the message
  msg = pad(msg,AES.block_size)

  ### init empty cipher bytes object
  cipher = bytes()

  ### get IV by random
  iv = Random.new().read(AES.block_size)

  ### prepend IV to cipher
  cipher += iv

  ### Initialize cipher AES in electronic code book mode
  aes = AES.new(key, AES.MODE_ECB)

  for j in range(0,len(msg),16):
    cipher += aes.encrypt(xor(cipher[-16:],msg[j:j+16]))

  return cipher

### Decryption Algorithm, CBC, using AES-128
### key & cipher should be provided as bytes objects
### returns decrypted msg
def decrypt_aes_cbc(key,cipher):

  ### init empty msg bytes object
  msg = bytes()

  ### Initialize cipher AES in electronic code book mode
  aes = AES.new(key, AES.MODE_ECB)

  for j in range(16,len(cipher),16):
    msg += xor( cipher[j-16:j] , aes.decrypt(cipher[j:j+16]))

  ### return unpadded message
  return unpad(msg)


### decrypting messages from homework assignment

cbc_key1_hex = "140b41b22a29beb4061bda66b6747e14"

cipher1 =  "4ca00ff4c898d61e1edbf1800618fb2828a226d160dad07883d04e008a7897ee2e4b7465d5290d0c0e6c6822236e1daafb94ffe0c5da05d9476be028ad7c1d81"

cbc_key2_hex = "140b41b22a29beb4061bda66b6747e14"

cipher2 = "5b68629feb8606f9a6667670b75b38a5b4832d0f26e1ab7da33249de7d4afc48e713ac646ace36e872ad5fb8a512428a6e21364b0c374df45503473c5242a253"

### transform cipher and key to byte objects, print decrypted msgs
cipher = bytes.fromhex(cipher1)
key = bytes.fromhex(cbc_key1_hex)

print(decrypt_aes_cbc(key,cipher).decode('utf-8'))

cipher = bytes.fromhex(cipher2)
key = bytes.fromhex(cbc_key2_hex)

print(decrypt_aes_cbc(key,cipher).decode('utf-8'))
