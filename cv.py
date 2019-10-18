import imutils,cv2,numpy as np
from util import *
from Orc import *
from PIL import Image
from aip import AipOcr
from skimage.measure import compare_ssim
import pytesseract
import os

WIN10 = True
tessdata_dir_config = '--tessdata-dir "C:\\Program Files (x86)\\Tesseract-OCR\\tessdata"'
aipOcr  = AipOcr(APP_ID, API_KEY, SECRET_KEY)

class UIMatcher:

    @staticmethod
    def findGreenArrow(screen):
        '''
        检测政策界面中 绿箭头的中心位置
        @return: 绿箭头坐标list
        '''
        # 增加判断screen，也就是截图是否成功的判断
        if screen.size:
            dstPoints = []
            img2 = cv2.split(screen)
            # 分离R 二值化
            ret, dst1 = cv2.threshold(img2[0], 20, 255, cv2.THRESH_BINARY_INV)
            # 分离G 二值化
            ret, dst2 = cv2.threshold(img2[1], 220, 255, cv2.THRESH_BINARY)
            # 分离B 二值化
            ret, dst3 = cv2.threshold(img2[2], 20, 255, cv2.THRESH_BINARY_INV)
            img2 = dst1&dst2&dst3 # 相与
            # 模糊边界
            # img2 = cv2.GaussianBlur(img2, (5, 5), 0)
            # import matplotlib.pyplot as plt
            # plt.imshow(img2,cmap='gray')
            # plt.show()
            # 找轮廓
            cnts = cv2.findContours(img2, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
            cnts = cnts[1] if imutils.is_cv3() else cnts[0]
            if len(cnts):
                for c in cnts:
                    # 获取中心点
                    M = cv2.moments(c)
                    cX = int(M["m10"] / M["m00"])
                    cY = int(M["m01"] / M["m00"])
                    #
                    dstPoints.append((cX,cY))

                    # 画出轮廓和中点
                    # cv2.drawContours(img2, [c], -1, (0, 255, 0), 2)
                    # cv2.circle(img2, (cX, cY), 20, (255, 255, 255), 1)
                    # cv2.putText(img2, "center", (cX - 20, cY - 20),
                    # cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                    # plt.imshow(img2,cmap='gray')
                    # plt.show()
            return dstPoints
        else:
            raise Exception('Screen process is unsuccessful')
    
    @staticmethod
    def findTaskBubble(screen):
        '''
        检测城市任务那块区域黄色气泡是否出现
        @return: 是否出现
        '''
        dstPoints = []
        h=len(screen)
        w=len(screen[0])
        # 截取气泡周围区域
        img2 = cv2.split(screen[int(0.777*h):int(0.831*h),int(0.164*w):int(0.284*w)])
        ret, B = cv2.threshold(img2[0], 120, 255, cv2.THRESH_BINARY_INV)
        ret, G = cv2.threshold(img2[1], 210, 255, cv2.THRESH_BINARY_INV)
        ret, R = cv2.threshold(img2[2], 230, 255, cv2.THRESH_BINARY)
        img2 = R&B&G # 相与
        # 模糊边界
        img2 = cv2.GaussianBlur(img2, (5, 5), 0)
        # 找轮廓
        cnts = cv2.findContours(img2, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        if cnts == None :#len(cnts[1]) True
            return False
        else:
            return True

    @staticmethod
    def findGreenLight(diff_screens,pos , th=100):
        screen_before, screen_after = diff_screens
        # 转换成有符号数以处理相减后的负值
        screen_before = screen_before.astype(np.int16)
        screen_after = screen_after.astype(np.int16)

        diff = screen_after - screen_before
        h=len(diff)
        w=len(diff[0])
        B,G,R = cv2.split(diff)
        # 负值取0
        G[G < 0] = 0
        G = G.astype(np.uint8)
        # 二值化后相与, 相当于取中间范围内的值
        ret, G1 = cv2.threshold(G, 140, 255, cv2.THRESH_BINARY_INV)
        ret, G2 = cv2.threshold(G, 22, 255, cv2.THRESH_BINARY)
        img0 = G1&G2
        # 均值模糊(降噪 好像也没啥卵用) 
        img0 = cv2.medianBlur(img0,9)
        # import matplotlib.pyplot as plt
        # plt.imshow(img0,cmap='gray')
        # plt.show()
        buildings = []
        for building_ID in range(1,10):
            square = UIMatcher.getLittleSquare(img0,pos[building_ID],edge=0.1)
            buildings.append(np.mean(square))
        # 返回平均亮度最强的建筑物
        return buildings.index(max(buildings))+1
    
    '''
    探测叉叉是否出现, 先截取叉叉所在的小方块,然后对灰度图二值化,再求平均值判断
    @staticmethod
    def detectCross(screen, th = 5):
        screen = cv2.cvtColor(screen,cv2.COLOR_RGB2GRAY)
        good_id_list = []
        for good_id in CROSS_POSITIONS.keys():
            square = UIMatcher.getLittleSquare(screen,CROSS_POSITIONS[good_id])
            ret, W = cv2.threshold(square, 250, 255, cv2.THRESH_BINARY)
            # import matplotlib.pyplot as plt
            # plt.imshow(W,cmap='gray')
            # plt.show()
            # 二值化后求平均值
            if np.mean(W) > th:
                good_id_list.append(good_id)
        # print(good_id_list)
        return good_id_list
    '''

    @staticmethod
    def getLittleSquare(img, rel_pos, edge=0.01):
        '''
        截取rel_pos附近一个小方块
        '''
        rx,ry = rel_pos
        h=len(img)
        w=len(img[0])
        scale = h/w
        x0 = int((rx-edge*scale)*w)
        x1 = int((rx+edge*scale)*w)
        y0 = int((ry-edge)*h)
        y1 = int((ry+edge)*h)
        return img[y0:y1,x0:x1]



    """
    获取某一坐标的RGB值(灰度图会报错)
    """
    @staticmethod
    def getPixel(img, rx, ry):
        pixel = []
        if type(rx) is float and type(ry) is float:
            pixel = img[int(ry*len(img)), int(rx*len(img[0]))]
        else:
            pixel = img[int(ry), int(rx)]
        return pixel[2],pixel[1],pixel[0]

    '''
    Baidu Orc
    '''
    @staticmethod
    def BdOrc(screen,area: AREA,Accurate = False):
        # 定义参数变量
        options = {
          'detect_direction': 'true',
          'language_type': 'CHN_ENG',
          "detect_language" : "true",
          "probability" : "false"
        }

        cropped = screen[area.y1:area.y2, area.x1:area.x2]

        gray = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)
        cv2.imwrite("cropped.png", gray)

        # 调用通用文字识别接口
        result = aipOcr.basicGeneral(get_file_content("cropped.png"), options) if not Accurate else aipOcr.basicAccurate(get_file_content("cropped.png"), options)
        result = result["words_result"]
        if type(result) is list and len(result) > 0:
            result = result[0]["words"]

        os.remove("cropped.png")
        return result

    '''
    Orc by tesseract
    '''
    @staticmethod
    def orcbyArea(screen,area: AREA):
        cropped = screen[area.y1:area.y2, area.x1:area.x2]
        #cv2.imwrite('out.jpg', cropped)
        gray = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)
        cv2.imwrite("cropped.png", gray)
        if WIN10:
            text = pytesseract.image_to_string(Image.open("cropped.png"), config=tessdata_dir_config)
        else:
            text = pytesseract.image_to_string(Image.open("cropped.png"))
        os.remove("cropped.png")
        #print("<"*5,text)
        return text

    @staticmethod
    def saveScreen(screen,*args):
        n = len(args)
        if n == 1 and type(args[0]) is int:
           cv2.imwrite('s' + str(args[0]) + '.png', screen)
           return

        if n >= 1 and isinstance(args[0], AREA):
            screen = screen[args[0].y1:args[0].y2, args[0].x1:args[0].x2]
        if n >= 2 and args[1] == 'g':
            gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
            if n >= 3:
                cv2.imwrite('g' + str(args[2]) + '.png', gray)  
            else:
                cv2.imwrite('g.png', gray) 
        cv2.imwrite('s.png', screen)

    @staticmethod
    def compare(imageA,imageB):
        grayA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
        grayB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)
        # compute the Structural Similarity Index (SSIM) between the two
        # images, ensuring that the difference image is returned
        (score, diff) = compare_ssim(grayA, grayB, full=True)
        diff = (diff * 255).astype("uint8")
        print("SSIM: {}".format(score))

    @staticmethod
    def read(path):
        return cv2.imread(path)


    @staticmethod
    def find(screen, target, criteria = 0.85):
        # 获取对应货物的图片。
        # 有个要点：通过截屏制作货物图片时，请在快照为实际大小的模式下截屏。
        template = cv2.imread(target.value)
        # 获取货物图片的宽高。    
        th, tw = template.shape[:2]
        # 调用 OpenCV 模板匹配。
        res = cv2.matchTemplate(screen, template, cv2.TM_SQDIFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        # 矩形左上角的位置。
        tl = min_loc
        # 阈值判断。
        if criteria > 1 - min_val:
            return None
        print("-"*30,target,"-"*30)
        print("阈值判断:",1 - min_val,criteria)
        print("坐标点:",tl[0] + tw / 2 + 15, tl[1] + th / 2 + 15)
        print("-"*70)

        # 这里，我随机加入了数字（15），用于补偿匹配值和真实位置的差异。
        return tl[0] + tw / 2 + 15, tl[1] + th / 2 + 15

