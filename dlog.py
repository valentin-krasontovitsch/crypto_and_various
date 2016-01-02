import gmpy2
from gmpy2 import mpz

### divm(...)
### divm(a, b, m) returns x such that b * x == a modulo m. Raises a ZeroDivisionError exception if no such value x exists.

### invert(...)
### invert(x, m) returns y such that x * y == 1 modulo m, or 0 if no such y exists.

### powmod(...)
### powmod(x, y, m) returns (x ** y) mod m. The exponenent y can be negative, and the correct result will be returned if the inverse of x mod m exists. Otherwise, a ValueError is raised.

p=mpz(13407807929942597099574024998205846127479365820592393377723561443721764030073546976801874298166903427690031858186486050853753882811946569946433649006084171)

g=mpz(11717829880366207009516117596335367088558084999998952205599979459063929499736583746670572176471460312928594829675428279466566527115212748467589894601965568)

h=mpz(3239475104050450443565264378728065788649097520952449527834792452971981976143292558073856937958553180532878928001494706097394108577585732452307673444020333)

B = mpz(2)**20

#p = mpz(104869)
#g = mpz(103221)
#h = mpz(82257)
### x = 52
#B = mpz(2)**3

dict = {}
i = mpz(0)
g_inv = gmpy2.invert(g,p)
tmp = h

while i < B:
  dict[tmp] = i
  tmp = gmpy2.t_mod(gmpy2.mul(tmp,g_inv),p)
  i+=1

print("done with dictionary")
i = mpz(0)
gb = gmpy2.powmod(g,B,p)
tmp = mpz(1)

while i < B:
  if tmp in dict:
    print("x=",i*B + dict[tmp])
    break
  tmp = gmpy2.t_mod(gmpy2.mul(tmp,gb),p)
  i+=1

print("done")