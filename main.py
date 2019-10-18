from automator import *
from util import *
from devices import *
import subprocess

MUMU = False
IOSandAndroid = False

def START(instance):
    instance.start()

if __name__ == '__main__':
    config = load_configure("config.json")
    
    '''
    building = {
        1 : "空中别墅" ,
        2 : "人オ公寓" ,
        3 : "钢结构房" ,
        4 : "学校"     ,
        5 : "菜市场"   ,
        6 : "图书城"   ,
        7 : "食品厂"   ,
        8 : "造纸厂"   ,
        9 : "钢铁厂"
    }
    '''
    building = {
        1 : "人オ公寓" ,
        2 : "居民楼" ,
        3 : "钢结构房" ,
        4 : "服装店"     ,
        5 : "便利店"   ,
        6 : "菜市场"   ,
        7 : "纺织厂"   ,
        8 : "钢铁厂"   ,
        9 : "食品厂"
    }

    if MUMU and b'connected' in subprocess.check_output('adb connect '+ d.MuMu()):
        print("Successfully connected to", d.MuMu())
        config["Deivce"] = "127.0.0.1:7555"

    d = Devices(config)

    ## 启动脚本。
    if not IOSandAndroid: 
        instance = Automator(d, building)
        instance.start()
    else:
        instance = Automator(d)
        t1 = threading.Thread(target=START, args=(instance,)) 
        config["IOS"] = True
        instance2 = Automator(Devices(config))
        t2 = threading.Thread(target=START, args=(instance2,))
        t1.start()
        t2.start()



