import time,json,os,sys,re
from GUI import *

DEBUG = True

def load_configure(file: str):
    f=open(file,encoding='utf-8')
    content=f.read()
    res=json.loads(content)
    Pout(res)
    return(res)

def msg(message):
    print("[%s]"%time.asctime(),message)

# customer print for debug
def Pout(*args):
    if DEBUG:
        print("\nDebug" + ">"*45 )
        skip = False
        for i in range(len(args)):
            if type(args[i]) is dict:
                print_d(args[i])
            elif type(args[i]) is bool:
                if not args[i]:
                    skip = True
            elif skip:
                skip = False
                continue;
            else:
                print(args[i],end = " ")
        print()
        print("<"*50)
        print()
    if GUI:
        print("GUI model")


# print dict 
def print_d(res):
    for key in res.keys():
        print(key,":",res[key])

# Sleep function that make program sleep by different times
def s(times = 0.1):
    time.sleep(times)

def ms():
    time.sleep(0.5)

def ss():
    time.sleep(1)
    