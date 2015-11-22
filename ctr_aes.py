### NOTES NOTES NOTES
### message to be encoded: get it from a file whose location is given as option to script
### for now, get msg from local string...
### END NOTES END NOTES END NOTES

### include AES, Random from crypto lib

from Crypto.Cipher import AES 
from Crypto import Random
from struct import *
import binascii
import sys

def pad(array,block_size):
  i = block_size - len(array)%block_size
  return array + bytes(chr(i),"ascii")*i

def unpad(array):
  return array[:-1*int.from_bytes(array[-1:], byteorder='big')]

### return XOR of bytearrays s,t
def xor(s,t):
  return bytes(x^y for x,y in zip(s,t))

### transfer bytes object to string of hex digits
#def ba_to_hex(s):
  #return "".join("%02x" % b for b in s)


### Encryption Algorithm, CTR, with random IV, using AES-128
### key & plain text should be provided as bytes objects
### returns encrypted padded msg with IV prepended
def encrypt_aes_ctr(key,msg):
  
  ### pad the message
  #msg = pad(msg,AES.block_size)

  ### init empty cipher bytes object
  cipher = bytes()

  ### get IV by random
  iv = Random.new().read(AES.block_size)

  ### prepend IV to cipher
  cipher += iv

  ### init cipher AES in electronic code book mode
  aes = AES.new(key, AES.MODE_ECB)
  
  ### init counter as IV
  ctr = iv
  
  ### actual encoding, block-wise
  
  for j in range(0,len(msg),16):
    if j + 16 > len(msg):
      cipher += xor(msg[j:],aes.encrypt(ctr))
    else:
      cipher += xor(msg[j:j+16],aes.encrypt(ctr))
    ### increase counter
    ctr = (int.from_bytes(ctr,sys.byteorder)+1).to_bytes(16,sys.byteorder)

  return cipher

### Decryption Algorithm, CTR, using AES-128
### key & cipher should be provided as bytes objects
### returns decrypted msg
def decrypt_aes_ctr(key,cipher):

  ### init empty msg bytes object
  msg = bytes()

  ### init cipher AES in electronic code book mode
  aes = AES.new(key, AES.MODE_ECB)
  
  ### init counter as IV, which is first block of cipher
  ctr = cipher[0:AES.block_size]
  
  ### actual decryption, block-wise
  
  for j in range(16,len(cipher),16):
    if j + 16 > len(cipher):
      msg += xor( cipher[j:] , aes.encrypt(ctr))
    else:
      msg += xor( cipher[j:j+16] , aes.encrypt(ctr))
    ### increase counter
    ctr = (int.from_bytes(ctr,byteorder='big', signed=False)+1).to_bytes(16,byteorder='big', signed=False)

  ### return unpadded message
  return msg


### decrypting messages from homework assignment

cbc_key1_hex = "36f18357be4dbd77f050515c73fcf9f2"

cipher1 =  "69dda8455c7dd4254bf353b773304eec0ec7702330098ce7f7520d1cbbb20fc388d1b0adb5054dbd7370849dbf0b88d393f252e764f1f5f7ad97ef79d59ce29f5f51eeca32eabedd9afa9329"

cbc_key2_hex = "36f18357be4dbd77f050515c73fcf9f2"

cipher2 = "770b80259ec33beb2561358a9f2dc617e46218c0a53cbeca695ae45faa8952aa0e311bde9d4e01726d3184c34451"

### transform cipher and key to byte objects, print decrypted msgs
cipher = bytes.fromhex(cipher1)
key = bytes.fromhex(cbc_key1_hex)

print(decrypt_aes_ctr(key,cipher).decode('latin-1'))

cipher = bytes.fromhex(cipher2)
key = bytes.fromhex(cbc_key2_hex)

print(decrypt_aes_ctr(key,cipher).decode('latin-1'))

### test of encryption and decryption

#test_msg = b"Wie lang ist's her - ach wie lang!"

#test_key = Random.new().read(AES.block_size)

#print(test_msg == decrypt_aes_ctr(test_key, encrypt_aes_ctr(test_key,test_msg)))