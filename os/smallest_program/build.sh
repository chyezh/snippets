#!/bin/bash

gcc hello.c -c
ld hello.o -e main
objdump -d a.out

# a.out will segment fault because the pc return from stack is not valid
