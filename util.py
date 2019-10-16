import time,json,os,sys,re

DEBUG = True

def load_configure(file: str):
    f=open(file,encoding='utf-8')
    content=f.read()
    res=json.loads(content)
    Pout(res)
    return(res)

# def get_upgrade_list(json_list: dict):
#     return list(zip(json_list['要升级的建筑物'], json_list['对应升级次数']))

# def clip_triangle()

# 三个车厢货物的位置
GOODS_POSITIONS = { 1: (0.609,0.854),
                    2: (0.758,0.815),
                    3: (0.896,0.766)}

# 货物的那个叉叉的位置 相对位置
CROSS_POSITIONS = { 1: (0.632, 0.878),
                    2: (0.776, 0.836),
                    3: (991/1080, 1517/1920)}





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
def s(time = 0.1):
    time.sleep(time)

def ms():
    time.sleep(0.5)

def ss():
    time.sleep(1)
    