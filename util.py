import time,json,os,sys,re

DEBUG = True

def load_configure(file: str):
    f=open(file,encoding='utf-8')
    content=f.read()
    res=json.loads(content)
    Pout(res)
    return(res)

# 三个车厢货物的位置
GOODS_POSITIONS = { 1: (661/1080,1841/2248),
                    2: (821/1080,1767/2248),
                    3: (957/1080,1689/2248)}

# 货物的那个叉叉的位置 相对位置
CROSS_POSITIONS = { 1: (681/1080, 1893/2248),
                    2: (839/1080, 1813/2248),
                    3: (989/1080, 1727/2248)}


JGM_tag = "com.tencent.jgm"

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
    