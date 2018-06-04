#!/usr/bin/python

import sys

inputdir = sys.argv[1]
outputdir = sys.argv[2]

sides = ['Front', 'Left', 'Right', 'Back']

for side in sides:
    inputfile = inputdir + '/' + side.lower() + '.cfg'
    f = open (inputfile, 'r')
    color = f.readline().split(None, 1)[0]
    f.close()

    output_h  = '#ifndef WINDOW_' + side + '_H_\n'
    output_h += '#define WINDOW_' + side + '_H_\n'
    output_h += 'class ' + side + '\n'
    output_h += '{\n'
    output_h += 'public:\n'
    output_h += '    ' + side + '();\n'
    output_h += '    virtual ~' + side + '();\n'
    output_h += '    virtual const char* getColor();\n'
    output_h += '};\n'
    output_h += '#endif\n'
    f = open(outputdir + '/' + side + '.gen.h', 'w')
    f.write(output_h)
    f.close()

    output_cpp  = '#include "' + side + '.gen.h"\n'
    output_cpp += side + '::' + side + '()\n'
    output_cpp += '{\n'
    output_cpp += '}\n'
    output_cpp += side + '::~' + side + '()\n'
    output_cpp += '{\n'
    output_cpp += '}\n'
    output_cpp += 'const char* ' + side + '::getColor()\n'
    output_cpp += '{\n'
    output_cpp += '    return "' + color + '";\n'
    output_cpp += '}\n'
    f = open(outputdir + '/' + side + '.gen.cpp', 'w')
    f.write(output_cpp)
    f.close()
