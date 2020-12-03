#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  1 17:43:21 2020

@author: jorgesilveyra
"""

import re
import os
Id =0
flag = False
with open("cran.all.1400") as f:
    for line in f:
        m = re.search(r'(\.I) (\d+)', line)
        if m is not None:
            if Id != m.group(2):
                if int(Id)>0:
                    fo.close()
                Id = m.group(2)
                path = os.path.dirname(os.path.abspath(__file__)) + '/separated'
                
                filename = "cranfield" +m.group(2)+".txt"
                filename = os.path.join(path, filename)
                fo = open(filename, "w")
			    
                flag = True
        if flag == True:
            fo.write(line)