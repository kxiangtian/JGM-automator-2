from cv import UIMatcher
from util import *
from devices import *
import uiautomator2 as u2
import wda
import random



class Automator:
    def __init__(self, d: Devices):
        print("-"*20 + "Automator Init" + "-"*20)
        if d.IOS():
            self.d = d.session()
        else:
            self.d = u2.connect(d.device())
        self.dWidth, self.dHeight = self.d.window_size()
        print("(",self.dWidth,"x",self.dHeight,")")

        self.pos = d.pos()
        print("建筑位置")
        print_d(self.pos)
        # auto_task = False
        self.auto_task = d.aT()
        print("自动任务",self.auto_task)

        # auto_policy = True
        self.auto_policy = d.aP()
        print("自动升级政策",self.auto_policy)

        # upgrade_list: list
        self.upgrade_list = [] if d.aU() == True else d.aU()[0]
        print("升级列表", self.upgrade_list)

        # harvest_filter:list
        self.harvest_filter = d.hFL()
        print("收割过滤",self.harvest_filter)

        self.appRunning = False
        print("程序运行",self.appRunning)

        # speedup = True
        self.loot_speedup = False
        print("物资加速",self.loot_speedup)

        print("-"*55)

    def start(self):
        """
        启动脚本，请确保已进入游戏页面。
        """
        d = self.d
        while True:
            # 判断jgm进程是否在前台, 最多等待20秒，否则唤醒到前台
            if d.app_wait("com.tencent.jgm", front=True,timeout=20):
                if not self.appRunning:
                    # 从后台换到前台，留一点反应时间
                    print("App is front. JGM agent start in 5 seconds")
                    time.sleep(5) 
                self.appRunning = True
            else:
                d.app_start("com.tencent.jgm")
                self.appRunning = False
                continue
            
            # 判断是否可升级政策
            self.check_policy()
            # 判断是否可完成任务
            self.check_task()
            # 判断货物那个叉叉是否出现

            good_id = self._has_good()
            if len(good_id) > 0:
                print("[%s] Train come."%time.asctime())
                self.harvest(self.harvest_filter, good_id)
            else:
                print("[%s] No Goods! Wait 2s."%time.asctime())
                self.swipe()
                time.sleep(2)
                continue
            
            # 再看看是不是有货没收，如果有就重启app
            good_id = self._has_good()
            if len(good_id) > 0 and self.loot_speedup:
                self.d.app_stop("com.tencent.jgm")
                print("[%s] Reset app."%time.asctime())
                time.sleep(2)
                # 重新启动app
                self.d.app_start("com.tencent.jgm")
                # 冗余等待游戏启动完毕
                time.sleep(15)
                continue

            # 简单粗暴的方式，处理 “XX之光” 的荣誉显示。
            # 不管它出不出现，每次都点一下 确定 所在的位置
            d.click(550/1080, 1650/1920)
            self.upgrade(self.upgrade_list)
            # 滑动屏幕，收割金币。
            self.swipe()

    def upgrade(self, upgrade_list):
        if not len(upgrade_list):
            return
        self._open_upgrade_interface()
        building,count = random.choice(upgrade_list)
        self._upgrade_one_with_count(building,count) 
        self._close_upgrade_interface()

    def harvest(self,building_filter,goods:list):
        '''
        新的傻瓜搬货物方法,先按住截图判断绿光探测货物目的地,再搬
        '''
        s()
        for good in goods:
            pos_id = self.guess_good(good)
            if pos_id != 0 and pos_id in building_filter:
                # 搬5次
                self._move_good_by_id(good, BUILDING_POSITIONS[pos_id], times=4)
                s()
      
    def guess_good(self, good_id):
        '''
        按住货物，探测绿光出现的位置
        这一段应该用numpy来实现，奈何我对numpy不熟。。。
        '''
        diff_screens = self.get_screenshot_while_touching(GOODS_POSITIONS[good_id]) 
        return UIMatcher.findGreenLight(diff_screens)

    def get_screenshot_while_touching(self, location, pressed_time=0.2):
        '''
        Get screenshot with screen touched.
        '''
        screen_before = self.d.screenshot(format="opencv")
        h,w = len(screen_before),len(screen_before[0])
        x,y = (location[0] * w,location[1] *h)
        # 按下
        self.d.touch.down(x,y)
        # print('[%s]Tapped'%time.asctime())
        time.sleep(pressed_time)
        # 截图
        screen = self.d.screenshot(format="opencv")
        # print('[%s]Screenning'%time.asctime())
        # 松开
        self.d.touch.up(x,y)
        # 返回按下前后两幅图
        return screen_before, screen

    def check_policy(self):
        if not self.auto_policy:
            return
        # 看看政策中心那里有没有冒绿色箭头气泡
        if len(UIMatcher.findGreenArrow(self.d.screenshot(format="opencv"))):
            # 打开政策中心
            self.d.click(0.206, 0.097)
            ms()
            # 确认升级
            self.d.click(0.077, 0.122)
            # 拉到顶
            self._slide_to_top()
            # 开始找绿色箭头,找不到就往下滑,最多划5次
            for i in range(5):
                screen = self.d.screenshot(format="opencv")
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
        screen = self.d.screenshot(format="opencv")
        if UIMatcher.findTaskBubble(screen):
            self.d.click(0.16, 0.84) # 打开城市任务
            s()
            self.d.click(0.51, 0.819) # 点击 完成任务
            print("[%s] Task finished.    ++++++"%time.asctime())
            self._back_to_main()

    def _open_upgrade_interface(self):
        screen = self.d.screenshot(format="opencv")
        # 判断升级按钮的颜色，蓝比红多就处于正常界面，反之在升级界面
        R, G, B = UIMatcher.getPixel(screen,0.974,0.615)
        if B > R:
            self.d.click(0.9, 0.57)

    def _close_upgrade_interface(self):
        screen = self.d.screenshot(format="opencv")
        # 判断升级按钮的颜色，蓝比红多就处于正常界面，反之在升级界面
        R, G, B = UIMatcher.getPixel(screen,0.974,0.615)
        if B < R:
            self.d.click(0.9, 0.57)

    def _upgrade_one_with_count(self,id,count):
        sx, sy=BUILDING_POSITIONS[id]
        self.d.click(sx, sy)
        time.sleep(0.3)
        for i in range(count):
            self.d.click(0.798, 0.884)
            # time.sleep(0.1)
       
    def _move_good_by_id(self, good: int, source, times=1):
        try:
            sx, sy = GOODS_POSITIONS[good]
            ex, ey = source
            for i in range(times):
                self.d.drag(sx, sy, ex, ey, duration = 0.1)
                s()
        except(Exception):
            pass    

    def _has_good(self):
        '''
        返回有货的位置列表
        '''
        screen = self.d.screenshot(format="opencv")  
        return UIMatcher.detectCross(screen)

    def _slide_to_top(self):
        for i in range(3):
            self.d.swipe(0.488, 0.302,0.482, 0.822)
            s()

    def _back_to_main(self):
        for i in range(3):
            self.d.click(0.057, 0.919)
            s()

    """
    随机概率滑动模式，滑动屏幕，收割金币。
    Simulate swipe, (Android === IOS)
    swipe(x1, y1, x2, y2, 0.5) # 0.5s(IOS, Android? )
    swipe(0.5, 0.5, 0.5, 1.0)  # swipe middle to bottom
    """
    def swipe(self):
        try:
            msg("滑动收集金币")
            for i in range(3):
                if 1 == random.randint(0,1):
                    sx, sy = self.pos[i * 3 + 1]
                    ex, ey = self.pos[i * 3 + 3]
                else:
                    sx, sy = self._get_position(i + 1)
                    ex, ey = self._get_position(i + 7)
                n = random.randint(-5,5)
                self.d.swipe(sx , sy + n, ex , ey + n)
        except(Exception):
            # 用户在操作手机，暂停10秒
            s(10)
