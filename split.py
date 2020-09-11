import os
import sys
import zipfile
import pathlib
import smtplib
import random
from math import floor
from builtins import any
from email import encoders
from getpass import getpass
from string import Template
from itertools import groupby
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText


server="mail.ru.nl"
port=587
username = "mario.tsatsev@student.ru.nl"
TAs = ["mario.tsatsev@student.ru.nl","mellestarke@gmail.com","dastaurin@gmail.com","sven@8x10.de","tvbuuren@science.ru.nl"]
subject = "Exercises to be graded this week"
recipients = ["mario.tsatsev@student.ru.nl", "mellestarke@gmail.com", "sven@8x10.de", "tvbuuren@science.ru.nl", "dastaurin@gmail.com"]
sender = username
#pasword = getpass()
divisor = 5


def split_assignments(list, n,avg):
    out = []
    last = 0.0

    while last < len(list):
        out.append(list[int(last):int(last + avg)])
        last += avg
    return out

loaded_assignments = sorted(os.listdir("assignments/"))

grouped_assignments = [list(i) for j, i in groupby(loaded_assignments, lambda a: a[21:23])]

temp_assignments = []
for i in grouped_assignments:
    temp_assignments.append(i[-1])

assignments = []


for submission in temp_assignments:
    if(submission[0:12] not in assignments and not any(submission[0:12] in x for x in assignments)):
        assignments.append(submission)
number_assignments = floor(len(assignments)/5)
random.shuffle(assignments)

splits = split_assignments(assignments,divisor,number_assignments)

for (i,name) in enumerate(TAs):
    zf = zipfile.ZipFile(name+".zip", "w")
    for submission in (splits[i]):
        for dirname, subdirs, files in os.walk("assignments/"+submission):
            zf.write(dirname)
            for filename in files:
                zf.write(os.path.join(dirname,filename))
    zf.close()



"""
zips = [x for x in os.listdir(pathlib.Path().absolute()) if x.endswith(".zip")]
print(zips)

def send_msg(zips):
    smtp = smtplib.SMTP(host=server,port=587)
    smtp.starttls()
    smtp.login(username,pasword)

    for (zip,mail) in zip(zips,TAs):
        if mail in zip:
            msg = MIMEMultipart()

            msg['From']=sender
            msg['To']  = mail
            smg['Subject']=subject

            attached_zip = zip
            attachment = open(pathlib.Path().absolute()+attached_zip,"rb")
            base = MIMEBase('application','octet-stream')
            base.set_payload((attachment).read())
            encoders.encode_base64(base)
            base.add_header('content-Disposition', "attachment= %s" % attached_zip)
            msg.attach(base)

            smtp.send_message(msg)
            del msg
    smtp.quit()

try:
    send_msg(zips)
except AssertionError:
    print("This is bullshit!")
"""
