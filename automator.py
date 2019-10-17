from cv import UIMatcher
from PIL import Image
from util import *
from devices import *
from constant import *
import uiautomator2 as u2
import wda
import cv2 
import threading
import random


class Automator:
    def __init__(self, d: Devices):
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

        # harvest_filter:list
        self.harvest_filter = d.hFL()
        print("Position of goods: ",self.harvest_filter)
        
        # auto_task = False
        #self.auto_task = d.aT()
        #print("自动任务",self.auto_task)

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
        if DEBUG:
            #self._count['money'] = UIMatcher.orcbyArea(self._Sshot(),AREA(247,128,407,190))
            #UIMatcher.saveScreen(self._Sshot())
            #print(self.d(className="android.widget.FrameLayout", resourceId="android:id/content") \
            #.child(className="android.widget.FrameLayout")\
            #.child(className="android.view.View").info)
            pass

        # Initial Building pos and their level
        self._Initial_Building()
        
        self._AssignGoodsPosition()

        n = random.randint(95,105)
        n2 = 0

        while True:
            if n2%n == 0:
                print(self)
            # Check if it is in the game
            self._runApp()

            # Swipe the screen to get the gold
            self._swipe()

            # Harvest the goods
            self._harvest()

            # 判断是否可升级政策
            #self.check_policy()

            # 判断是否可完成任务
            #self.check_task()
            
            # 简单粗暴的方式，处理 “XX之光” 的荣誉显示。
            # 不管它出不出现，每次都点一下 确定 所在的位置
            #d.click(550/1080, 1650/1920)
            #self._upgrade()
            #self.upgrade(self.upgrade_list)
            n2 += 1

    def upgrade(self, upgrade_list):
        if not len(upgrade_list):
            return
        self._open_upgrade_interface()
        building,count = random.choice(upgrade_list)
        self._upgrade_one_with_count(building,count) 
        self._close_upgrade_interface()

    def check_policy(self):
        if not self.auto_policy:
            return
        # 看看政策中心那里有没有冒绿色箭头气泡
        if len(UIMatcher.findGreenArrow(self._Sshot())):
            # 打开政策中心
            self.d.click(0.206, 0.097)
            ms()
            # 确认升级
            self.d.click(0.077, 0.122)
            # 拉到顶
            self._slide_to_top()
            # 开始找绿色箭头,找不到就往下滑,最多划5次
            for i in range(5):
                screen = self._Sshot()
                arrows = UIMatcher.findGreenArrow(screen)
                if len(arrows):
                    x,y = arrows[0]
                    self.d.click(x,y) # 点击这个政策
                    s()
                    self.d.click(0.511, 0.614) # 确认升级
                    print("[%s] Policy upgraded.    ++++++"%time.asctime())
                    self._back_to_main()

                    return
                # 如果还没出现绿色箭头，往下划
                self.d.swipe(0.482, 0.809, 0.491, 0.516,duration = 0.3)
            self._back_to_main()

    def check_task(self):
        if not self.auto_task:
            return
        # 看看任务中心有没有冒黄色气泡
        screen = self._Sshot()
        if UIMatcher.findTaskBubble(screen):
            self.d.click(0.16, 0.84) # 打开城市任务
            s()
            self.d.click(0.51, 0.819) # 点击 完成任务
            print("[%s] Task finished.    ++++++"%time.asctime())
            self._back_to_main()

    def _open_upgrade_interface(self):
        screen = self._Sshot()
        # 判断升级按钮的颜色，蓝比红多就处于正常界面，反之在升级界面
        R, G, B = UIMatcher.getPixel(screen,1061/1080,1369/2248)
        if B > R:
            self.d.click(1061/1080, 1369/2248)

    def _close_upgrade_interface(self):
        screen = self._Sshot()
        # 判断升级按钮的颜色，蓝比红多就处于正常界面，反之在升级界面
        R, G, B = UIMatcher.getPixel(screen,1061/1080,1369/2248)
        if B < R:
            self.d.click(1061/1080, 1369/2248)

    def _upgrade_one_with_count(self,id,count):
        sx, sy=BUILDING_POSITIONS[id]
        self.d.click(sx, sy)
        time.sleep(0.3)
        for i in range(count):
            self.d.click(859,2053)
            # time.sleep(0.1)

    def _slide_to_top(self):
        for i in range(3):
            self.d.swipe(0.488, 0.302,0.482, 0.822)
            s()

    def _back_to_main(self):
        for i in range(3):
            self.d.click(0.057, 0.919)
            s()


    def _tap(self,sx,sy):
        self.d.swipe(sx, sy, sx + 1, sy + 1)
        time.sleep(random.randint(1,5) * 0.1)
    

    def _upgrade(self):
        #点开升级界面
        self._tap(1045,1373)
        screen = self._Sshot()
        R, G, B = UIMatcher.getPixel(screen,1061/1080,1369/2248)
        if B > R:
            self._tap(983,1830)
            #一次点击建筑
            for i in range(9):
                sx, sy = self.pos[i + 1]
                self._tap(sx,sy)
                self._tap(859,2053)
        screen = self._Sshot()
        R, G, B = UIMatcher.getPixel(screen,1061/1080,1369/2248)
        while (B > R):
            screen = self._Sshot()
            R, G, B = UIMatcher.getPixel(screen,1061/1080,1369/2248)
            self._tap(1045,1373)

    '''
    IOS has the different version of harvest
    def harvest(self,building_filter,goods:list):
        s()
        for good in goods:
            pos_id = self.guess_good(good)
            if pos_id != 0 and pos_id in building_filter:
                # 搬5次
                self._move_good_by_id(good, self.pos[pos_id], times=4)
                s()
    '''
    def _harvest(self):
        if self._has_train():
            if self._IOS:
                pass
            else:
                self._Move_good_Android()
                self._count["harvest"] += 1

    def _Move_good_Android(self):
        ''' self._pos_good
        按住货物，探测绿光出现的位置
        这一段应该用numpy来实现，奈何我对numpy不熟。。。
        '''
        for good in self.harvest_filter:
            pos_id = self._DeterminePos_Android(good)
            if pos_id != 0 and pos_id in self.pos:
                self._move_good_by_id(good, self.pos[pos_id], times = 4)

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

    '''
    If there is train here (Easy way just determine the color of a pixel)
    '''
    def _has_train(self):
        x,y = self._btn["P_Train"]
        screen = self._Sshot()
        R, G, B = UIMatcher.getPixel(screen,x,y)
        if R == 74 and G == 160 and B == 161:
            return True
        msg("No train (" + str(R) + "," + str(G) +"," 
            + str(B) + ")") 
        return False
    '''
    Assign each Type of items into dict for IOS
    '''
    def _AssignGoodsPosition(self):
        if self._IOS:
            for b in self._bd["pos"].values():
                if b in CONSTANT_ITEM:
                    self._bd["gds"][CONSTANT_ITEM[b]] = b
        else:
            pass
        #print_d(self._bd["gds"])
        print_2d(self._bd)

    '''
    Initiliaze building with position with their level
    '''
    def _Initial_Building(self):
        x,y = self._btn["B_Upgrade"]
        if not self._Is_Btn_Upgrade():
            self._tap(x,y)

        for i in range(9):
            sx, sy = self.pos[i + 1]
            self._tap(sx,sy)
            building = UIMatcher.BdOrc(self._Sshot(),self._btn["R_Names"])
            self._bd["lvl"][i + 1],self._bd["pos"][i + 1] = building.split("级")
        
        self._tap(x,y)    
        if self._Is_Btn_Upgrade():
            self._tap(x,y)

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

    def __str__(self):
        print("="*23 + "Info" + "="*23)
        print_d(self._count)
        Print_d(self._bd["pos"])
        Print_d(self._bd["lvl"])
        return "="*50