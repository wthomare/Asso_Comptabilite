# -*- coding: utf-8 -*-

from wx.tools import img2py
import os

"""
Tranform bmp image in a python scrypt. It can be loaded into a program at
runtime.
"""


command_lines = []

for file in os.listdir("img"):
    name = file.split('.', 1)[0]
    path = os.path.join("img", file)
    command_lines.append("-a -F -c -n %s %s images.py" %(name, path))
    
if __name__ == "__main__":
    for line in command_lines:
        args = line.split()
        img2py.main(args)