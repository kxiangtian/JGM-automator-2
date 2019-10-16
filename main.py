from automator import *
from util import *
from devices import *
import subprocess




MUMU = False


if __name__ == '__main__':
    d = Devices(load_configure("config.json"))
    
    if MUMU and b'connected' in subprocess.check_output('adb connect '+ d.MuMu()):
        print("Successfully connected to", d.MuMu())

    instance = Automator(d)
    
    ## 启动脚本。
    instance.start()

