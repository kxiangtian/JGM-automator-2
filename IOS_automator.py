import random
import wda
from cv import UIMatcher
from util import *
from devices import *

class IOS_automator:
	def __init__(self, d: Devices):
		print("-"*20 + "IOS Init" + "-"*20)
		self.d = d.session()