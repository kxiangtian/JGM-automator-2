from cv import UIMatcher
from PIL import Image
from util import *
from devices import *
from constant import *
import uiautomator2 as u2
import wda
import numpy as np
import cv2
import threading
import random
from target import *


class Automator:
    def __init__(self, d: Devices, BUILDING = None):
        self._DEBUG = True


        print("-"*20 + "Automator Init" + "-"*20)
        self._IOS = d.IOS()

        if self._IOS:
            self.d = d.session()
        else:
            self.d = u2.connect(d.device())

        self.dWidth, self.dHeight = self.d.window_size()
        print("Screen (",self.dWidth,"x",self.dHeight,")")

        self.pos = d.pos()
        self._pos_good = d.goods()
        self._btn = d.features()
        print("Initialized Position of building")
        #print_d(self.pos)

        self._count = {"swipe" : 0,
                        "upgrade" : 0,
                        "harvest" : 0,
                        "money"   : 0}
        print("Initialized Counts")

        self._bd= {
            "pos": {},
            "lvl": {},
            "gds": {}
        }
        if BUILDING is not None:
            self._bd["pos"] = BUILDING
        # harvest_filter:list
        self.harvest_filter = d.hFL() if len(d.hFL()) <= 3 else [1,2,3]
        print("Position of goods: ",self.harvest_filter)
        
        self.auto_task = d.aT()
        print("auto_task",self.auto_task)

        # auto_policy = True
        #self.auto_policy = d.aP()
        #print("自动升级政策",self.auto_policy)

        # upgrade_list: list
        #self.upgrade_list = [] if d.aU() == True else d.aU()[0]
        #print("升级列表", self.upgrade_list)



        # speedup = True
        #self.loot_speedup = False
        #print("物资加速",self.loot_speedup)

        print("-"*55)
    
    """
    启动脚本，请确保已进入游戏页面。
    """
    def start(self):
        NomoreTrain = False
        n = random.randint(95,105)
        n2 = 0

        # Initial Building pos and their level
        self._Initial_Building()
        self._AssignGoodsPosition()

        #UIMatcher.saveScreen(self._Sshot())
    
        # Test crop the goods
        if self._DEBUG:
            #self._Test()
            pass

        while True:
            if n2%n == 0:
                print(self)
            # Check if it is in the game
            self._runApp()

            # Swipe the screen to get the gold
            self._swipe()

            # Harvest the goods
            
            if not NomoreTrain:
                if self._No_more_train():
                    msg("No more Train, Turn off harvest")
                    NomoreTrain = True
            self._harvest(NomoreTrain)

            # 判断是否可升级政策
            #self.check_policy()

            # 判断是否可完成任务
            self._check_task()
            
            # 简单粗暴的方式，处理 “XX之光” 的荣誉显示。
            # 不管它出不出现，每次都点一下 确定 所在的位置
            #self.d.click(0.8, 0.90)
            

            n2 += 1


    '''
    Crop the good from specific position then compare
    '''
    def _Test(self):
        for good in self.harvest_filter:
            img = UIMatcher.getLittleSquare(self._Sshot(),self._pos_good[good])
            UIMatcher.saveScreen(img,good)
            #imageB = cv2.imread("test2.png")
            #UIMatcher.compare(img,imageB)


    def _Cross_out(self, times = 3):
        for i in range(times):
            p = random.randint(-5,10)
            q = random.randint(-5,10)
            self._tap(10 + p ,10 + q)

    def _check_task(self):
        if not self.auto_task:
            return
        x,y = self._btn["B_Task"]
        R, G, B = UIMatcher.getPixel(self._Sshot(),x,y)
        if not self._IOS and (R,G,B) == (253,237,0):
            return True
        elif self._IOS and r_color((R,G,B),TASK_FINISH_IOS):
            self._tap(x,y)
            s(2)
            x2,y2 = self._btn["B_Finish_Task"]
            R2, G2, B2 = UIMatcher.getPixel(self._Sshot(),x2,y2)
            if r_color((R2,G2,B2),TASK_B_FINISH_IOS):
                self._tap(x2,y2)
                ss()
                self._Cross_out()

            elif self._DEBUG:
                msg("Finished Task (" + str(R2) + "," + str(G2) +"," + str(B2) + ")") 


        if self._DEBUG:
            msg("Task Finished Color(" + str(R) + "," + str(G) +"," + str(B) + ")") 
        return False


    def _Move_good_IOS(self):
        goods = self._bd["gds"]
        for good in self.harvest_filter:
            img = UIMatcher.getLittleSquare(self._Sshot(),self._pos_good[good],scale = 2)
            UIMatcher.saveScreen(img,good)
            for target in goods.keys():
                imageB = cv2.imread(target.value,1)
                #msg("SSIM: {}  Target {}".format(score,str(target)))
                result = UIMatcher.find(img,imageB,diff_situation(good,targe))
    
                if result:
                    msg(str(target) + " move to " + str(goods[target]))
                    position = self.pos[goods[target]]
                    #Pout(sx,sy,ex,ey)
                    self._move_good_by_id(good, position, times = 4)
                    #self._drag(sx, sy, ex , ey,0.5)
                    break

    '''
    IOS has the different version of harvest
    '''
    def _harvest(self,NomoreTrain = False):
        if self._has_train() and not NomoreTrain:
            msg("Found train - harvest")
            if self._IOS:
                self._Move_good_IOS()
            else:
                self._Move_good_Android()
            self._count["harvest"] += 1

    def _Move_good_Android(self):
        for good in self.harvest_filter:
            pos_id = self._DeterminePos_Android(good)
            if pos_id != 0 and pos_id in self.pos:
                self._move_good_by_id(good, self.pos[pos_id], times = 4)

    ''' 
    self._pos_good
    按住货物，探测绿光出现的位置
    这一段应该用numpy来实现，奈何我对numpy不熟。。。
    '''
    def _DeterminePos_Android(self, pos, pressed_time = 0.2):
        screen_before = self._Sshot()
        x,y = self._pos_good[pos]
        x,y = (x * self.dWidth, y * self.dHeight)
        self.d.touch.down(x,y)
        time.sleep(pressed_time)
        screen_after = self._Sshot()
        self.d.touch.up(x,y)
        diff_screens = (screen_before,screen_after)
        result = UIMatcher.findGreenLight(diff_screens,self.pos)
        return  result

    def _move_good_by_id(self, good: int, source, times = 1):
        try:
            sx, sy = self._pos_good[good]
            ex, ey = source
            #Pout(sx,sy,ex,ey)
            for i in range(times):
                self._drag(sx, sy, ex, ey)
                s()
        except(Exception):
            pass

    def _No_more_train(self):
        x,y = self._btn["P_NoMoreTrain"]
        screen = self._Sshot()
        R, G, B = UIMatcher.getPixel(screen,x,y)
        if not self._IOS and (R,G,B) == (253,237,0):
            return True
        elif self._IOS and (R,G,B) == (53,106,111):
            return True
        if self._DEBUG:
            msg("No More train (" + str(R) + "," + str(G) +"," + str(B) + ")") 
        return False

    '''
    If there is train here (Easy way just determine the color of a pixel)
    '''
    def _has_train(self):
        x,y = self._btn["P_Train"]
        screen = self._Sshot()
        R, G, B = UIMatcher.getPixel(screen,x,y)
        if not self._IOS and R == 74 and G == 160 and B == 161:
            return True
        elif self._IOS and (R,G,B) == TRAIN_COLOR_IOS:
            return True
        if self._DEBUG:
            msg("No train (" + str(R) + "," + str(G) +"," + str(B) + ")") 
        return False

    '''
    Assign each Type of items into dict for IOS
    '''
    def _AssignGoodsPosition(self):
        for b in self._bd["pos"].keys():
            key = self._bd["pos"][b]
            if key in CONSTANT_ITEM:
                self._bd["gds"][CONSTANT_ITEM[key]] = b
        #print_d(self._bd["gds"])
        #print_2d(self._bd)

    '''
    Initiliaze building with position with their level
    '''
    def _Initial_Building(self):
        if self._bd["pos"] == None:
            x,y = self._btn["B_Upgrade"]
            if not self._Is_Btn_Upgrade():
                self._tap(x,y)

            for i in range(9):
                sx, sy = self.pos[i + 1]
                self._tap(sx,sy)
                building = UIMatcher.BdOrc(self._Sshot(),self._btn["R_Names"])
                if not building == None and type(building) is str:
                    self._bd["lvl"][i + 1],self._bd["pos"][i + 1] = building.split("级")
            
            self._tap(x,y)    
            if self._Is_Btn_Upgrade():
                self._tap(x,y)
        else:
            for i in range(9):
                self._bd["lvl"][i + 1] = 0

        #print_d(self._bd["pos"])
        #print_d(self._bd["lvl"])
        #print("-"*23 + "Building" + "-"*23)

    '''
    To determine if it is in upgrade
    '''
    def _Is_Btn_Upgrade(self):
        x,y = self._btn["B_Upgrade"]
        R, G, B = UIMatcher.getPixel(self._Sshot(),x,y)
        if B > R:
            return False
        elif B < R:
            return True

    def _tap(self,sx,sy):
        self.d.click(sx, sy)
        time.sleep(random.randint(1,5) * 0.1)

    """
    Screen shot compatiable Version for both IOS and Android
    """
    def _Sshot(self, png = "s"):
        if self._IOS:
            self.d.screenshot().save(png + ".png")
            return cv2.imread(png + ".png")
        else:
            return self.d.screenshot(format="opencv")

    """
    This function will perform the drag
    """
    def _drag(self, sx, sy, ex, ey, times = 0.1):
        if self._IOS:
            self.d.swipe(sx, sy, ex, ey, times)
        else:
            self.d.drag(sx, sy, ex, ey, duration = times)

    """
    Run App if App is not front.
    """
    def _runApp(self):
        # 判断jgm进程是否在前台, 最多等待20秒，否则唤醒到前台
        if not self._IOS and not self.d.app_wait(JGM_tag, front=True,timeout=20):
            # 从后台换到前台，留一点反应时间
            msg("App is not front. Start App and run in 5 seconds")
            self.d.app_start(JGM_tag)
            time.sleep(5)

        elif self._IOS and not self.d.app_current()["bundleId"] == JGM_tag:
            msg("App is not front. Start App and run in 5 seconds")
            self.d.app_activate(JGM_tag)
            time.sleep(5)

    """
    Random Swipe for getting Money
    Flip a coin to determine swipe horizontally or vertically
    (Android === IOS) Simulate swipe
    swipe(x1, y1, x2, y2, 0.5) # 0.5s(IOS, Android?)
    swipe(0.5, 0.5, 0.5, 1.0)  # swipe middle to bottom
    """
    def _swipe(self):
        try:
            if 1 == random.randint(0,1):
                #msg("Slide horizontally to collect gold COINS")
                for i in range(3):
                    sx, sy = self.pos[i * 3 + 1]
                    ex, ey = self.pos[i * 3 + 3]
                    self.d.swipe(sx-0.1, sy+0.05, ex, ey)
            else:
                #msg("Swipe vertically to collect gold COINS")
                for i in range(3):
                    sx, sy = self.pos[i + 1]
                    ex, ey = self.pos[i + 7]
                    n = random.uniform(-0.003,0.003)
                    #Pout(sx, sy,ex, ey,sx-n, sy+n)
                    self.d.swipe(sx - n , sy + n, ex, ey)
            self._count["swipe"] += 1
        except(Exception):
            # wait for 10s
            s(10)

    def _tap(self,sx,sy):
        self.d.click(sx, sy)
        time.sleep(random.randint(1,5) * 0.1)

    def __str__(self):
        print("="*23 + "Info" + "="*23)
        print_d(self._count)
        print_2d(self._bd)
        return "="*50