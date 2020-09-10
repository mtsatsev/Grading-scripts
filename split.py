import os
import sys
import zipfile
from math import floor
from builtins import any


TAs = ["Mario","Melle","Nikolai","Sven","Thijmen"]

def chunkIt(list, n,avg):
    out = []
    last = 0.0

    while last < len(list):
        out.append(list[int(last):int(last + avg)])
        last += avg
    return out

temp_assignments = os.listdir("assignments/")
divisor = 5
assignments = []
for submission in temp_assignments:
    if(submission[0:12] not in assignments and not any(submission[0:12] in x for x in assignments)):
        assignments.append(submission)
number_assignments = floor(len(assignments)/5)

splits = chunkIt(assignments,divisor,number_assignments)

for (i,name) in enumerate(TAs):
    zf = zipfile.ZipFile(name+".zip", "w")
    for submission in (splits[i]):
        for dirname, subdirs, files in os.walk("assignments/"+submission):
            zf.write(dirname)
            for filename in files:
                zf.write(os.path.join(dirname,filename))
    zf.close()
