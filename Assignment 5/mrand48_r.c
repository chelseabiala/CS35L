#include <cpuid.h>
#include <immintrin.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include "mrand48_r.h"

struct drand48_data buffer = {0};
long int first;
long int second;

void
mrand48_ralt_init (void) {
  srand48_r(time(NULL), &buffer);
}

unsigned long long
mrand48_ralt (void){
  mrand48_r(&buffer, &first);
  mrand48_r(&buffer, &second);
  unsigned long long int result = ((unsigned long long int) first | ((unsigned long long int) second << 32));
  return result;
}
  

void
mrand48_ralt_fini (void){}
