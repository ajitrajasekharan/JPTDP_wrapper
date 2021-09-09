#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#
from unidecode import unidecode
import sys
import pdb
#import platform
#print(platform.python_version())

def sbd_handle(inp_str):
    arr = inp_str.split()
    ret_arr = []
    for i in range(len(arr)):
        word = arr[i]
        length = len(word)
        if (length >  1 and word.endswith('.') and (word[length-2].isalpha() or word[length-2].isdigit())):
            ret_arr.append(word[:length-1])
            ret_arr.append('.')
        else:
            ret_arr.append(word)
    return ' '.join(ret_arr)


if __name__ == '__main__':
    try:
        print(sbd_handle(unidecode(str(sys.argv[1]))))
    except:
        print("Unexpected error:", sys.exc_info()[0])
