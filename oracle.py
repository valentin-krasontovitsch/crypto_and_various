import urllib.request, urllib.error, urllib.parse
import sys

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
    po.query(sys.argv[1])       # Issue HTTP query with the given argument