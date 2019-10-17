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
    
    if MUMU and b'connected' in subprocess.check_output('adb connect '+ d.MuMu()):
        print("Successfully connected to", d.MuMu())
        config["Deivce"] = "127.0.0.1:7555"

    d = Devices(config)

    ## 启动脚本。
    if not IOSandAndroid: 
        instance = Automator(d)
        instance.start()
    else:
        instance = Automator(d)
        t1 = threading.Thread(target=START, args=(instance,)) 
        config["IOS"] = True
        instance2 = Automator(Devices(config))
        t2 = threading.Thread(target=START, args=(instance2,))
        t1.start()
        t2.start()



