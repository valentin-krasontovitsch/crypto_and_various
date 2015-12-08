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
  mod = bytearray.fromhex(orig)
  #po.query(batoh(orig))
  # k=1 -> last block, determine padding first
  
  if k == 1:
    # xor mod with pad (of length 1)
    mod[-1*block_size-1] ^= 1
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
    # xor rest of mod with padding
    for j in range(1,i):
      mod[-1*block_size-1-j] = i
    # update guess with padding
    for j in range(i):
      guess[-1-j] = i
    # set starting index for estimated pad
    start = i+1
  else:
    # ... and for no pad (not last block)
    start = 1
  
  # debug end point !!!
  return guess

  # loop (backwards) through and modify block k-1 in order to guess block k
  # starting at position start, counted from the end
  for j in range(start,block_size+1):
    
    # small debug msg
    print("Trying position %i, counted backwards",j)
    
    ## prepare pad
    #for l in range(j):
      #pad[-l-1] = j
    
    # iterate through mod and xor with pad
    for l in range(j):
      mod[-k*block_size-l-1] ^= j   # last j bytes in (k-1)-st block
    
    # loop through all guesses for j-th byte
    for char in range(254):
      # update j-th byte of guess (backwards...)
      guess[-j] = char
      ## reinitialize 
      #mod = bytearray.fromhex(orig)
      
      # small debug msg
      print("Trying character ",char)
      
      for j in range(i):
        mod[-1*(k)*block_size-1-j] ^= guess[-j] ^ char
        if check(mod):
          break
    # revert pad xor
    for l in range(j):
      mod[-k*block_size-l-1] ^= j   # last j bytes in (k-1)-st block
  return guess

#def det_byte(orig,k):
  ## pad - just last byte for now
  #pad[-1] = 1
  #for i in range(0,16):
    #mod = bytearray.fromhex(orig)
    
    #guess[-1] = i
    ##print(guess[-1])
    
    ## apply guess and pad to original thing
    
    #for i in range(0,block_size):
        #mod[-2*block_size+i] ^= pad[i] ^ guess[i]
    
    #if po.query(batoh(mod)):       # Issue HTTP query with the given argument
      #break
  #pad_length = guess[-1]



if __name__ == "__main__":
  po = PaddingOracle()
  #po.query(sys.argv[1])       # Issue HTTP query with the given argument
  

  # original url which is to be decrypted
  
  #orig = "f20bdba6ff29eed7b046d1df9fb7000058b1ffb4210a580f748b4ac714c001bd4a61044426fb515dad3f21f18aa577c0bdf302936266926ff37dbf7035d5eeb4"
  
  orig = "f20bdba6ff29eed7b046d1df9fb7000058b1ffb4210a580f748b4ac714c001bd4a61044426fb515dad3f21f18aa577c0bdf302936266926ff37dbf7035d5eeb4"
  
  # initialize things
  #po.query(orig)
  # make url into bytearray which will be modified and tested
  #orig_b = bytes.fromhex(orig)
  #po.query(batoh(orig_b))
  last_block = det_block(orig,1)
  print(last_block)
  #print(batoh(last_block))
  #print(last_block.decode("utf-8"))
  
  ## guess of current block
  #guess = bytearray([0 for i in range(0,block_size)])
  
  ## pad, to be applied to current block
  #pad = bytearray([0 for i in range(0,block_size)])
  #po.query(batoh(orig_b))
  #print("just tried it - did it print anything?")
  ## pad - just last byte for now
  #pad[-1] = 1
  #for i in range(0,16):
    #mod = orig_b
    #print("trying %i:",i)
    #guess[-1] = i
    ##print(guess[-1])
    
    ## apply guess and pad to original thing
    #print(batoh(mod[-2*block_size:-1*block_size]))
    ##for i in range(0,block_size):
    #mod[-1*block_size-1] ^= pad[-1] ^ guess[-1]
    #print(mod == orig_b)
    #print(batoh(mod[-2*block_size:-1*block_size]))
    #if po.query(batoh(mod)):       # Issue HTTP query with the given argument
      #break
  #pad_length = guess[-1]
