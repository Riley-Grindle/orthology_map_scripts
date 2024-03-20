#!/usr/bin/python3

import os
import glob

path = "./"
pattern = path + "*"
result = glob.glob(pattern)



for file in result:

    if file == "./capitalize_files.py":
        continue

    else:

        count = 0
        backwards = file[::-1]
        for i in range(len(backwards)):
            if backwards[i] == ".":
                count = i
                break
        old = file[:-count]
        suffix = file[-count:]
        new = old.upper() + suffix
        os.rename(file, new)

