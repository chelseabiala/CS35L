/* Generate N bytes of random output.  */

/* When generating output this program uses the x86-64 RDRAND
   instruction if available to generate random numbers, falling back
   on /dev/random and stdio otherwise.

   This program is not portable.  Compile it with gcc -mrdrnd for a
   x86-64 machine.

   Copyright 2015, 2017, 2020 Paul Eggert

   This program is free software: you can redistribute it and/or
   modify it under the terms of the GNU General Public License as
   published by the Free Software Foundation, either version 3 of the
   License, or (at your option) any later version.

   This program is distributed in the hope that it will be useful, but
   WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
   General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program.  If not, see <http://www.gnu.org/licenses/>.  */

#include <cpuid.h>
#include <errno.h>
#include <ctype.h>
#include <immintrin.h>
#include <limits.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include "options.h"
#include "output.h"
#include "rand64-hw.h"
#include "rand64-sw.h"
#include "mrand48_r.h"

/* Main program, which outputs N bytes of random data.  */
int
main (int argc, char **argv)
{
  /* Check arguments.
  bool valid = true;
  long long nbytes;
  if (argc == 2)
    {
      char *endptr;
      errno = 0;
      nbytes = strtoll (argv[1], &endptr, 10);
      if (errno)
	perror (argv[1]);
      else
	valid = !*endptr && 0 <= nbytes;
      valid = true;
    }
  else
    {
      char *endptr;
      nbytes = strtoll (argv[1], &endptr, 10);
      valid = true;
    }
  if (!valid)
    {
      fprintf (stderr, "%s: usage: %s NBYTES\n", argv[0], argv[0]);
      return 1;
      }  */

  int c;
  long long nbytes;
  char *inputArg;
  char *outputArg;
  bool useRdrand = true;
  bool useMrand = false;
  bool useFile = false;
  bool useStdio = true;

  while ((c = getopt(argc, argv, ":i:o:")) != -1) {
        switch(c) {
        case 'i':
	    if (argc != 4 && argc != 6)
	      {
		fprintf (stderr, "%s: usage: %s NBYTES\n", argv[0], argv[0]);                                 return 1;
	      }
	    if (optarg[0]=='/') {
	      useFile = true;
	      useRdrand = false;
	    }
	    else if (strcmp("mrand48_r", optarg) == 0) {
              useRdrand = false;
              useMrand = true;
            }
	    else if (strcmp("rdrand", optarg) != 0) {
		fprintf(stderr,
              "Unrecognized option: '-%c'\n", optopt);
               return 1;
	    }
	    inputArg = optarg;
	    break;
        case 'o':
	    if (isdigit(*optarg))
            {
               useStdio = false;
            }
	    else if (strcmp("stdio", optarg) != 0)
            {
               fprintf(stderr,
               "Unrecognized option: '-%c'\n", optopt);
                return 1;
            }
            outputArg = optarg;
            break;
        case ':':       /* -f or -o without operand */
            fprintf(stderr,
                "Option -%c requires an operand\n", optopt);
            return 1;
        case '?':
            fprintf(stderr,
		    "Unrecognized option: '-%c'\n", optopt);
	    return 1;
        }
    }

  nbytes = atol(argv[optind]);
  
  /* If there's no work to do, don't worry about which library to use.  */
  if (nbytes == 0)
    return 0;

  /* Now that we know we have work to do, arrange to use the
     appropriate library.  */
  void (*initialize) (void);
  unsigned long long (*rand64) (void);
  void (*finalize) (void);
  if (useRdrand && rdrand_supported () && !useFile)
    {
      if(useMrand)
	{
	  initialize = mrand48_ralt_init;
          rand64 = mrand48_ralt;
          finalize = mrand48_ralt_fini;
	}
      else
	{
          initialize = hardware_rand64_init;
          rand64 = hardware_rand64;
          finalize = hardware_rand64_fini;
	}
    }
  else
    {
      initialize = software_rand64_init;
      if (useFile)
	{
        	reassignFile(inputArg);
	}
      rand64 = software_rand64;
      finalize = software_rand64_fini;
    }

  initialize ();
  int wordsize = sizeof rand64 ();
  int output_errno = 0;
  unsigned long long num = rand64 ();

  if(!useStdio)
    {
      int len = atoi(outputArg);
      if(len == 0)
	return 0;
      char* buffer = malloc(len);
      do
	{
          int outbytes = nbytes < len ? nbytes : len;
	  for(int i = 0; i < outbytes; i++)
	    {
	      num = rand64();
	      buffer[i] = num;
	    }
	  write(1, buffer, outbytes);
	  nbytes -= outbytes;
	} while(0 < nbytes);
      free(buffer);
    }
    else {
  do
    {
      unsigned long long x = rand64 ();
      int outbytes = nbytes < wordsize ? nbytes : wordsize;
      if (!writebytes (x, outbytes))
	{
	  output_errno = errno;
	  break;
	}
      nbytes -= outbytes;
    }
  while (0 < nbytes);
    }

  if (fclose (stdout) != 0)
    output_errno = errno;

  if (output_errno)
    {
      errno = output_errno;
      perror ("output");
    }

  finalize ();
  return !!output_errno;
}
