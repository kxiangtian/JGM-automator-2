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
		self._adp = config["Auto_deploy"] 
		self._uBL = config["Upgrade_Building"] #empty for all
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
			return self._uBL

	def adp(self):
		return self._adp

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
		    return self._s.window_size()

def Assign_Position(Ss):
	# 各号建筑的位置
	Pout("屏幕比例:",Ss,Ss == (375,812),"\nIphone X,Xs"
		,Ss == (375,667),"\nIphone 8,7,6s,6,SE"
		,Ss == (414,736) or Ss == (375,667),"\nIphone 8P,7P,6sP,6P")
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
		"P_NoMoreTrain":(525/1080,1744/2248),
		"P_Train": (575/1242,1940/2208),
		"B_Upgrade" : (1213/1242,1377/2208),
		"B_Store" : (515/1242,2103/2208),
		"B_Build" : (49/1242,2107/2208),
		"B_Task" : (191/1242,1861/2208),
		"B_Policy" : (255/1242,228/2208),
		"R_gold": AREA(287,56,461,116),
		"R_Names" : AREA(339,1563,877,1635),
		"R_Levels" : AREA(339,1688,471,1750),
		"B_Finish_Task":(0,0),
		"B_Upgrade_B" :(0,0),
		"B_NoMoreTrain":(0,0),
		"P_redpacket":[(0,0),(0,0),(0,0),(0,0)]
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
		1: (657/1080,1857/2248),
		2: (821/1080,1770/2248),
		3: (968/1080,1690/2248)
		}
		FEATURES = {
		"P_NoMoreTrain":(525/1080,1744/2248),
		"P_Train": (413/1080,1952/2248),
		"B_Upgrade" : (1059/1080,1367/2248),
		"B_Store" : (522/1080,2151/2248),
		"B_Build" : (181/1080,2142/2248),
		"B_Task" : (184/1080,1825/2248),
		"B_Policy" : (221/1080,403/2248),
		"R_gold": AREA(247,128,407,190),
		"R_Names" : AREA(339,1680,819,1755),
		"R_Levels" : AREA(339,1688,471,1750),
		"B_Finish_Task":(0,0),
		"B_Upgrade_B" :(0,0),
		"B_NoMoreTrain":(861/10808,2089/2248),
		"P_redpacket":[(290/1080,724/2248),(652/1080,724/2248),(1000/1080,724/2248),(625/1080,1148/2248)]
		}
	elif Ss == 2:
		BUILDING_POSITIONS = {

		}
		GOODS = {
		}
		FEATURES = {

		}
	elif Ss == (414,736) or Ss == (375,667):
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
		1: (760/1242,1888/2208),
        2: (940/1242,1793/2208),
        3: (1117/1242,1698/2208)
		}
		FEATURES = {
		"P_NoMoreTrain":(0,0),
		"P_Train": (575/1242,1940/2208),
		"B_Upgrade" : (1213/1242,1377/2208),
		"B_Store" : (515/1242,2103/2208),
		"B_Build" : (49/1242,2107/2208),
		"B_Task" : (191/1242,1861/2208),
		"B_Policy" : (255/1242,228/2208),
		"R_gold": AREA(287,56,461,116),
		"R_Names" : AREA(339,1565,880,1650),
		"R_Levels" : AREA(339,1565,579,1650),
		"B_Finish_Task":(0,0),
		"B_Upgrade_B" :(0,0),
		"B_NoMoreTrain":(0,0),
		"P_redpacket":[(0,0),(0,0),(0,0),(0,0)]
		}

	elif Ss == (375,812):
		BUILDING_POSITIONS = {
		1: (327/1125, 1460/2436),
		2: (572/1125, 1341/2436),
		3: (846/1125, 1197/2436),
		4: (314/1125, 1210/2436),
		5: (578/1125, 1071/2436),
		6: (838/1125, 945/2436),
		7: (321/1125, 943/2436),
		8: (567/1125, 828/2436),
		9: (824/1125, 687/2436)
		}
		GOODS = {
		1: (684/1125,1984/2436),
        2: (849/1125,1895/2436),
        3: (1017/1125,1801/2436)
		}
		FEATURES = {
		"P_NoMoreTrain":(550/1125,1867/2436),
		"P_Train": (447/1125,2025/2436),
		"B_Upgrade" : (1092/1125,1483/2436),
		"B_Store" : (605/1125,2265/2436),
		"B_Build" : (56/1125,2314/2436),
		"B_Task" : (270/1125,1888/2436),
		"B_Policy" : (244/397,228/2436),
		"R_gold": AREA(287,56,461,116),
		"R_Names" : AREA(339,1565,880,1650),
		"R_Levels" : AREA(339,1565,579,1650),
		"B_Finish_Task":(455/1125,1854/2436),
		"B_Upgrade_B" :(894/1125,2266/2436),
		"B_NoMoreTrain":(421/1125,1733/2436),
		"P_redpacket":[(304/1125,792/2436),(652/1125,792/2436),(1000/1125,794/2436),(650/1125,1515/2436)]
		}
	else:
		print("没有找到对应屏比对应位置")
		sys.exit()
	return BUILDING_POSITIONS,GOODS,FEATURES

# get Scale of Screen
def Scale(Ss):
	return "{:0.1f}:{:0.0f}".format(int(Ss[0])/120,int(Ss[1])/120)



