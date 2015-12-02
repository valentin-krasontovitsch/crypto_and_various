### NOTES NOTES NOTES
### do we want to create a hashed file? maybe later
### what would a checker look like?
### END NOTES END NOTES END NOTES
### 
### hash a (e.g.) video file block wise
### starting with the last block
### and appending the hash of n-th block to (n-1)-st 
### block - this way file can be checked for authenticity
### blockwise instead of being downloaded completely
### and a video may start playing although being incomplete
### 
### so far only implementation of computing the hash
### of a file given by command line arg

### include SHA256 from crypto lib

from Crypto.Hash import SHA256

### include command line arguments parsing package

import argparse

### include os to access file size

import os

### set up argparser

parser = argparse.ArgumentParser()
parser.add_argument("file", help="file whose hash is to be computed; return hash h_0")
args = parser.parse_args()

### note block size in which file is to be read and hashed, in bytes

block_size = 1024

### open file

with open(args.file,'rb') as f:
  
  ### jump to beginning of last block of file
  ### which may be shorter than block_size
  ### and deal with it
  
  ### get file size
  
  f_size = os.path.getsize(args.file)
  
  ### determine size of last block
  
  last_block_size = f_size%block_size
  if last_block_size == 0:
    last_block_size = block_size
  
  ### move to last block, read and hash last block
  
  f.seek(-1*last_block_size,2)
  h = SHA256.new(f.read(last_block_size))

  ### if only one block, print hash

  if f_size <= block_size:
    print(h.hexdigest())
    quit()
  
  ### move file handler to beginning of 
  ### second to last block
  
  f.seek(-1*block_size-last_block_size,1)
  
  ### deal with other blocks
  
  while True:
    h = SHA256.new(f.read(block_size)+h.digest())
    if f.tell() == block_size:
      break
    f.seek(-2*block_size,1)

  ### print hash
  
  print(h.hexdigest())
