from automator import *
from IOS_automator import *
from util import *
from devices import *
import subprocess




MUMU = False


if __name__ == '__main__':
    d = Devices(load_configure("config.json"))
    
    if MUMU and b'connected' in subprocess.check_output('adb connect '+ d.MuMu()):
        print("Successfully connected to", d.MuMu())

    instance = None
    if d.IOS():
    	instance = IOS_automator(d)
    else:
        instance = Automator(d)
    #instance = Automator(Device, up_list, harvest_filter,auto_policy=policy,auto_task=task,speedup=speed_up)
    #instance.start()
    ## 启动脚本。
    #instance.start()

