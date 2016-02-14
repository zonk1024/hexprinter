#!/usr/bin/env python


import pydoc
import termcolor
import string
from sys import stdin, stdout, stderr


printable_chars = set(string.printable[:-5])
semiprintable_chars = set(string.printable[-5:])
null_chars = set(['\x00'])

def format_line(data):
    output = []
    for d in data:
        if d in printable_chars:
            output.append(termcolor.colored('{:>2}'.format(d), 'red', attrs=['bold']))
        elif d in semiprintable_chars:
            output.append(termcolor.colored('{}'.format(hex(ord(d))[2:].upper().zfill(2)), 'green', attrs=['bold']))
        elif d in null_chars:
            output.append(termcolor.colored('{}'.format(hex(ord(d))[2:].upper().zfill(2)), 'white', attrs=['bold']))
        else:
            output.append(termcolor.colored('{}'.format(hex(ord(d))[2:].upper().zfill(2)), 'blue', attrs=['bold']))
    return ''.join(output)


def print_bytes(data, width=64):
    for i in range(len(data)/width):
        return format_line(data[i*width:(i+1)*width])


def main(options, args):
    for arg in args:
        stderr.write('{}\n'.format(arg))
        with open(arg, 'rb') as f:
            print print_bytes(f.read(), options.width)

    new_bytes = stdin.read(options.width)
    while new_bytes:
        print print_bytes(new_bytes, options.width)
        stdout.flush()
        new_bytes = stdin.read(options.width)


if __name__ == '__main__':
    import optparse
    parser = optparse.OptionParser()
    parser.add_option('-w', '--width', dest='width', action='store', type='int', default=64)
    main(*parser.parse_args())
