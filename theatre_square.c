#include <stdio.h>
#include <stdlib.h>

/*
Theatre Square in the capital city of Berland has a rectangular shape with the size n × m meters. On the occasion of the city's anniversary, a decision was taken to pave the Square with square granite flagstones. Each flagstone is of the size a × a.

What is the least number of flagstones needed to pave the Square? It's allowed to cover the surface larger than the Theatre Square, but the Square has to be covered. It's not allowed to break the flagstones. The sides of flagstones should be parallel to the sides of the Square.

Input
The input contains three positive integer numbers in the first line: n,  m and a (1 ≤  n, m, a ≤ 109).

Output
Write the needed number of flagstones.*/


int main(int argc, char** args) {

  unsigned long long n,m,a;
  char *s;
  s = malloc(sizeof(char)*100);
  scanf(" %[^\n]", s);
  n = strtoull(s,&s,10);
  m = strtoull(s,&s,10);
  a = strtoull(s,&s,10);
  
  unsigned long long x = ( (n+a-1) / a ) * ( (m+a-1) / a );

//   on linux machine, use ldd instead of I64d!
  
  printf("%I64d\n",x);
  
  return 0;
}
