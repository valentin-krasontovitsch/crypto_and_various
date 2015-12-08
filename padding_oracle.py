import urllib.request, urllib.error, urllib.parse
import sys

def batoh( byte_arr ):
    return ''.join( [ "%02x" % x for x in byte_arr ] )

block_size = 16

TARGET = 'http://crypto-class.appspot.com/po?er='
#--------------------------------------------------------------
# padding oracle
#--------------------------------------------------------------
class PaddingOracle(object):
  def query(self, q):
    target = TARGET + urllib.parse.quote(q)    # Create query URL
    req = urllib.request.Request(target)         # Send HTTP request to server
    try:
      f = urllib.request.urlopen(req)          # Wait for response
    except urllib.error.HTTPError as e:          
      print("We got: %d" % e.code)       # Print response code
      if e.code == 404:
        return True # good padding
      return False # bad padding


# determine the k-th to last block 
# return plain text as bytearray
def det_block(orig,k):

  # initialize guess of current block, pad
  guess = bytearray([0 for i in range(0,block_size)])
  pad = bytearray([0 for i in range(0,block_size)])

  # k=1 -> last block, determine padding first
  if k == 1:
    # intialize the to be sent url
    mod = bytearray.fromhex(orig)
    # xor mod with pad (of length 1)
    mod[-block_size-1] ^= 1
    # try pad lengths
    for i in range(1,17):
      # small debug msg
      print("trying %i:",i)
      # xor mod with guess of pad length
      mod[-1*block_size-1] ^= i
      # check modified mod success: break
      if po.query(batoh(mod)):       # Issue HTTP query with the given argument
        break
      # failure: revert xor, try next
      mod[-1*block_size-1] ^= i
      print("-------------")
    # revert pad xor
    mod[-1*block_size-1] ^= 1
    # xor rest of mod with padding (i.e. our successful guess)
    for j in range(1,i):
      mod[-1*block_size-1-j] ^= i
    # update guess with padding
    for j in range(i):
      guess[-1-j] = i
    # set starting index for estimated pad
    start = i+1

  else:
    # ... and for no pad (not last block)
    start = 1
    # initialize mod array from orig, cutting down to k-th block
    mod = bytearray.fromhex(orig[:(-k+1)*block_size*2])
  
  # loop (backwards) through and modify block k-1 in order to guess block k
  # starting at position start, counted from the end
  for j in range(start,block_size+1):
    
    # small debug msg
    print("Trying position %i, counted backwards",j)
    
    # iterate through mod and xor with pad
    for l in range(j):
      mod[-block_size-l-1] ^= j   # last j bytes in (k-1)-st block
    
    
    # loop through all guesses for j-th byte
    for char in range(256):
      # update j-th byte of guess (backwards...)
      guess[-j] = char
      
      # small debug msg
      print("Trying character %i", char)
      
      # xor with guess
      mod[-block_size-j] ^= guess[-j]
      # check modified url; success: break out of loop, byte was guessed
      # guess has the byte saved, mod is xored with guess up to that byte
      if po.query(batoh(mod)):
        break
      # ... failure: revert xor on mod with guess, go on guessing
      mod[-block_size-j] ^= guess[-j]
      
    # revert pad xor, proceed with next byte
    for l in range(j):
      mod[-block_size-l-1] ^= j   # last j bytes in (k-1)-st block
    
  return guess



if __name__ == "__main__":
  po = PaddingOracle()
  #po.query(sys.argv[1])       # Issue HTTP query with the given argument
  

  # original url which is to be decrypted
  
  orig = "f20bdba6ff29eed7b046d1df9fb7000058b1ffb4210a580f748b4ac714c001bd4a61044426fb515dad3f21f18aa577c0bdf302936266926ff37dbf7035d5eeb4"
  
  # saving already cracked information
  
  last_block="sifrage\t\t\t\t\t\t\t\t\t"
  plain_text="The Magic Words are Squeamish Ossifrage"
  msg_hex = "546865204d6167696320576f726473206172652053717565616d697368204f7373696672616765090909090909090909"
  
  # intialize msg
  msg_b = bytearray()
  
  # looping through all blocks, decrypting all but first block of orig
  
  for k in range(1,int(len(orig)/32)):
    msg_b = det_block(orig,k) + msg_b
  
  # print out result in utf-8 #and in hex
  
  print(msg_b.decode("utf-8"))
  #print(batoh(msg_b))
  
  
  
  
  
  