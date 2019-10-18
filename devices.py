import sys
import wda
import re
from util import *

wda.DEBUG = False # default False

class Devices:
	def __init__(self, config):
		# Set for Android or Emulator
		self._device = config["Deivce"]

		# Set for IOS
		self._devicetype = config["IOS"]
		self._IP = config["IP"]
		self._s = self.Set_IOS()

		# Determine ScreenSize
		self._ScreenSize = self.get_screen_size()

		# 游戏配置 Configuration
		self._position,self._goods,self._features = Assign_Position(self._ScreenSize)
		 
		# Automatic upgrade by calculation | disable uBL uBlL
		self._aU = config["Auto_Upgrade"] 
		self._aT = config["Auto_task"]
		self._aP = config["Auto_policy"]
		self._aR = config["Auto_redpacket"] 
		self._aPz = config["Auto_puzzle"] 

		self._uBL = config["Upgrade_Building"] #empty for all
		self._uBlL= config["Upgrade_Building_Level"] #empty for each once
		self._hFL = config["Harvest_filter"] #len(0) = everything

	def features(self):
		return self._features

	def goods(self):
		return self._goods

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
	GOODS = dict()
	FEATURES = dict()
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
		GOODS = {
		1: (0.609,0.854),
        2: (0.758,0.815),
        3: (0.896,0.766)
		}
		FEATURES = {
		"P_Train": (575/1242,1940/2208),
		"B_Upgrade" : (1213/1242,1377/2208),
		"B_Store" : (515/1242,2103/2208),
		"B_Build" : (49/1242,2107/2208),
		"B_Task" : (191/1242,1861/2208),
		"B_Policy" : (255/1242,228/2208),
		"R_gold": AREA(287,56,461,116),
		"R_Names" : AREA(339,1563,877,1635),
		"R_Levels" : AREA(339,1688,471,1750)
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
		GOODS = {
		1: (618/1080,1813/2248),
		2: (772/1080,1723/2248),
		3: (939/1080,1645/2248)
		}
		FEATURES = {
		"P_Train": (421/1080,1940/2248),
		"B_Upgrade" : (1059/1080,1367/2248),
		"B_Store" : (522/1080,2151/2248),
		"B_Build" : (181/1080,2142/2248),
		"B_Task" : (184/1080,1825/2248),
		"B_Policy" : (221/1080,403/2248),
		"R_gold": AREA(247,128,407,190),
		"R_Names" : AREA(339,1680,819,1755),
		"R_Levels" : AREA(339,1688,471,1750)
		}
	elif Ss == 2:
		BUILDING_POSITIONS = {

		}
		GOODS = {
		}
		FEATURES = {

		}
	elif Ss == 3:
		BUILDING_POSITIONS = {
		1: (297/1242, 1463/2208),
		2: (611/1242, 1306/2208),
		3: (917/1242, 1137/2208),
		4: (325/1242, 1159/2208),
		5: (619/1242, 961/2208),
		6: (905/1242, 819/2208),
		7: (323/1242, 837/2208),
		8: (615/1242, 685/2208),
		9: (927/1242, 537/2208)
		}
		GOODS = {
		1: (0.609,0.854),
        2: (0.758,0.815),
        3: (0.896,0.766)
		}
		FEATURES = {
		"P_Train": (575/1242,1940/2208),
		"B_Upgrade" : (1213/1242,1377/2208),
		"B_Store" : (515/1242,2103/2208),
		"B_Build" : (49/1242,2107/2208),
		"B_Task" : (191/1242,1861/2208),
		"B_Policy" : (255/1242,228/2208),
		"R_gold": AREA(287,56,461,116),
		"R_Names" : AREA(339,1565,880,1650),
		"R_Levels" : AREA(339,1565,579,1650)
		}
	else:
		print("没有找到对应屏比对应位置")
		sys.exit()
	return BUILDING_POSITIONS,GOODS,FEATURES

# get Scale of Screen
def Scale(Ss):
	return "{:0.1f}:{:0.0f}".format(int(Ss[0])/120,int(Ss[1])/120)



