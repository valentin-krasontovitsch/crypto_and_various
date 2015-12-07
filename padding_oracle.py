import urllib.request, urllib.error, urllib.parse
import sys

def batoh( byte_arr ):
    return ''.join( [ "%02x" % x for x in byte_arr ] )

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

if __name__ == "__main__":
  po = PaddingOracle()
  #po.query(sys.argv[1])       # Issue HTTP query with the given argument
  
  block_size = 16

  # original url which is to be decrypted
  
  orig = "f20bdba6ff29eed7b046d1df9fb7000058b1ffb4210a580f748b4ac714c001bd4a61044426fb515dad3f21f18aa577c0bdf302936266926ff37dbf7035d5eeb4"

  # initialize things
  
  # make url into bytearray which will be modified and tested
  #mod = bytearray.fromhex(orig)
  
  # guess of current block
  guess = bytearray([0 for i in range(0,block_size)])
  
  # pad, to be applied to current block
  pad = bytearray([0 for i in range(0,block_size)])
  
  # pad - just last byte for now
  pad[-1] = 1
  for i in range(0,16):
    mod = bytearray.fromhex(orig)
    
    guess[-1] = i
    #print(guess[-1])
    
    # apply guess and pad to original thing
    
    for i in range(0,block_size):
        mod[-2*block_size+i] ^= pad[i] ^ guess[i]
    
    if po.query(batoh(mod)):       # Issue HTTP query with the given argument
      break
  print((guess[-1]))