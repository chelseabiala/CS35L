
#!/usr/bin/env python3

import random, sys, argparse

class shuf:

    def shuffle(self,lines):
        random.shuffle(lines)
        return lines
    
def main():
    version_msg = "%prog 3.10"
    usage_msg = """%prog [OPTION]... FILE
or shuf.py -i LO-HI [OPTION]...

Write a random permutation of the input lines to standard output.

       With no FILE, or when FILE is -, read standard input."""
    
    parser = argparse.ArgumentParser()

    parser.add_argument("-r", "--repeat", action="store_true", dest="repeat", default=False, help="Output the lines more than once.")
    parser.add_argument("-n", "--headcount", action="store", dest="headCount", default=sys.maxsize, help="Output at most COUNT lines.")
    parser.add_argument("-i", "--input-range", action="store", dest="inputRange", help="treat each number LO through HI as an input line.")
    parser.add_argument("-e", "--echo", action="store_true", dest="echo", help="Treat each ARG as an input line.")
    parser.add_argument("input", nargs="*", help="Input stored.")
    
    options, args = parser.parse_known_args()

    lines = []

    if options.inputRange is not None:
        dashes = False
        for character in options.inputRange:
            if character == '-':
                dashes = True
        if not dashes:
            parser.error("invalid input range: {0}".
                         format(options.inputRange))

    if options.echo:
        lines = options.input
    elif options.inputRange:                                                     
        for i in range(len(options.inputRange)):
            if options.inputRange[i] == '-':
                firstNumber = int(options.inputRange[0:i])
                secondNumber = int(options.inputRange[i+1:])
                break
        temp = firstNumber
        for j in range(firstNumber, secondNumber + 1):
            lines.append(str(temp))
            temp = temp + 1
        try:
            firstNumber = int(firstNumber)
        except:
            parser.error("invalid input range: {0}".
                         format(firstNumber))
        try:
            secondNumber = int(secondNumber)
        except:
            parser.error("invalid input range: {0}".
                 format(secondNumber))
                
        if firstNumber > secondNumber:
            parser.error("invalid input range: {0}".
                     format(options.inputRange))                                            
    elif not options.input:
        for i in sys.stdin:
            lines.append(i)
    else:
        for i in range (0,len(options.input)):
            match options.input[i]:
                case "-":
                    for i in sys.stdin:
                        lines.append(i)
                    break
                case _:
                    filename = options.input[0]
                    with open(filename) as file:
                        lines = file.readlines()
                        lines = [line.rstrip() for line in lines]
            
    generator = shuf()
    shuffled = generator.shuffle(lines)

    if options.headCount == sys.maxsize:
        count = len(lines)
    else:
        count = int(options.headCount)
            
    if count < 0:
        parser.error("invalid line count: {0}".
                     format(options.headCount))

    if (len(args) > 0) and options.inputRange is not None:
        parser.error("extra operand: {0}".
                     format(args[0]))

    if options.echo and options.inputRange is not None:
        parser.error("cannot combine -e and -i options")
    
    repeat = options.repeat

    try:
        repeat = bool(options.repeat)
    except:
        parser.error("invalid REPEAT: {0}".
                     format(options.repeat))
    
    for currentLine in shuffled:
        if count > 0 and count < len(lines) + 1:
            sys.stdout.write(currentLine)
            sys.stdout.write("\n")
            count = count - 1

    while repeat and count > 0:
        shuffledFile = generator.shuffle(lines)
        for currLine in shuffledFile:
            sys.stdout.write(currLine)
            sys.stdout.write("\n")
            count = count - 1
    
if __name__ == "__main__":
    main()
