import sys
from util import *

class Devices:
	def __init__(self, config):
		self._device = config["Deivce"]
		self._MuMu   = config["MuMu"]
		self._devicetype = config["IOS"]

		self._ScreenSize = Scale(get_screen_size(self._devicetype))
		self._position = Assign_Position(self._ScreenSize)
		

	def IOS(self):
		return self._devicetype

	def position(self):
		return self._position

	def device(self):
		return self._device

	def MuMu(self):
		return self._MuMu

def Assign_Position(Ss):
	# 各号建筑的位置
	Pout("分辨率",Ss)
	BUILDING_POSITIONS = dict()
	if Ss == "16.0:9":
		BUILDING_POSITIONS = {
		1: (294/1080, 1184/1920),
		2: (551/1080, 1061/1920),
		3: (807/1080, 961/1920),
		4: (275/1080, 935/1920),
		5: (535/1080, 810/1920),
		6: (799/1080, 687/1920),
		7: (304/1080, 681/1920),
		8: (541/1080, 568/1920),
		9: (787/1080, 447/1920)
		}
	elif Ss == "18.7:9":
		BUILDING_POSITIONS = {
		1: (294/1080, 1471/2248),
		2: (551/1080, 1285/2248),
		3: (807/1080, 1169/2248),
		4: (303/1080, 1163/2248),
		5: (535/1080, 1033/2248),
		6: (799/1080, 945/2248),
		7: (304/1080, 915/2248),
		8: (595/1080, 795/2248),
		9: (787/1080, 681/2248)
		}
	else:
		print("没有找到对应屏比对应位置")
		sys.exit()
		return BUILDING_POSITIONS

# get Scale of Screen
def Scale(Ss):
	return "{:0.1f}:{:0.0f}".format(int(Ss[0])/120,int(Ss[1])/120)

# get screen size
def get_screen_size(IOS):
	if not IOS:
		size_str = os.popen('adb shell wm size').read()
		if not size_str:
			print('请安装 ADB 及驱动并配置环境变量')
			sys.exit()
			m = re.search(r'(\d+)x(\d+)', size_str)
			if m:
				return (m.group(2),m.group(1))
	            #return "{height}x{width}".format(height=m.group(2), width=m.group(1))
			return (1920,1080)
	else:
	    # TODO get IOS size later
	    print("IOS Screen Size")
	    return (1920,1080)