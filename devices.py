import sys
import wda
import re
from util import *

wda.DEBUG = False # default False

class Devices:
	def __init__(self, config):
		# Set for Android or Emulator
		self._device = config["Deivce"]
		self._MuMu   = config["MuMu"]

		# Set for IOS
		self._devicetype = config["IOS"]
		self._IP = config["IP"]
		self._s = self.Set_IOS()

		# Determine ScreenSize
		self._ScreenSize = self.get_screen_size()

		# 游戏配置 Configuration
		self._position = Assign_Position(self._ScreenSize)
		# Automatic upgrade by calculation | disable uBL uBlL
		self._aU = config["Auto_Upgrade"] 
		self._aT = config["Auto_task"]
		self._aP = config["Auto_policy"]
		self._aR = config["Auto_redpacket"] 
		self._aPz = config["Auto_puzzle"] 

		self._uBL = config["Upgrade_Building"] #empty for all
		self._uBlL= config["Upgrade_Building_Level"] #empty for each once
		self._hFL = config["Harvest_filter"] #len(0) = everything

	def hFL(self):
		return self._hFL

	def aU(self):
		if self._aU:
			return True
		else:
			return (self._uBL,self._uBlL)

	def aPz(self):
		return self._aPz

	def aR(self):
		return self._aR

	def aP(self):
		return self._aP

	def aT(self):
		return self._aT

	def pos(self):
		return self._position

	def session(self):
		return self._s

	def IOS(self):
		return self._devicetype

	def device(self):
		return self._device

	def MuMu(self):
		return self._MuMu

	def Set_IOS(self):
		if self.IOS():
			screenshot_backup_dir = 'screenshot_backups/'
			if not os.path.isdir(screenshot_backup_dir):
				os.mkdir(screenshot_backup_dir)
			self._c = wda.Client('http://' + self._IP + ':8100/')
			return self._c.session()

	# get screen size
	def get_screen_size(self):
		if not self.IOS():
			size_str = os.popen('adb shell wm size').read()
			if not size_str:
				print('请安装 ADB 及驱动并配置环境变量')
				sys.exit()
			m = re.search(r'(\d+)x(\d+)', size_str)
			if m:
				return Scale((m.group(2),m.group(1)))
		        #return "{height}x{width}".format(height=m.group(2), width=m.group(1))
			return Scale((1920,1080))
		else:
		    # TODO get IOS size later
		    Pout("IOS - UIKit Size: ", self._s.window_size())
		    return self._s.scale

def Assign_Position(Ss):
	# 各号建筑的位置
	Pout("屏幕比例:",Ss,Ss == 3,"\nIphone X,Xs,8P,7P,6sP,6P"
		,Ss == 2,"\nIphone 8,7,6s,6,SE")
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

	elif Ss == 3:
		BUILDING_POSITIONS = {

		}
	elif Ss == 2:
		BUILDING_POSITIONS = {

		}
	else:
		print("没有找到对应屏比对应位置")
		sys.exit()
		return BUILDING_POSITIONS

# get Scale of Screen
def Scale(Ss):
	return "{:0.1f}:{:0.0f}".format(int(Ss[0])/120,int(Ss[1])/120)



