from target import TargetType
import math

JGM_tag = "com.tencent.jgm"

CONSTANT_ITEM = {
           "服装店"  : TargetType.Cloth,
           "便利店"  : TargetType.Bottle,
           "钢结构房": TargetType.Sofa,
           "造纸厂"  : TargetType.Grass,
           "木材厂"  : TargetType.Wood,
           "图书城"  : TargetType.Book,
           "钢铁厂"  : TargetType.矿石,
           "学校"    : TargetType.书包,
           "居民楼"  : TargetType.快递,
           "木屋"    : TargetType.Chair,
           "人オ公寓" : TargetType.电脑,
           "平房"    : TargetType.花盆,
           "菜市场"  : TargetType.Vegetable,
           "食品厂"  : TargetType.Food,
           "中式小楼": TargetType.Quilt,
           "媒体之声": TargetType.话筒,
           "民食斋"  : TargetType.烧鸡,
           "空中别墅": TargetType.时尚吊灯,
           "纺织厂"  : TargetType.cotton
           #"电厂":    TargetType.
}

TRAIN_COLOR_IOS = (144,147,180)
TASK_FINISH_IOS = (255,192,58)
TASK_B_FINISH_IOS = (254,211,44)
NO_MORE_TRAIN_IOS = (252,231,2)
RED_PACKET = (193, 44, 38)
BLUE_MENU = (50, 116, 174)

def r_color(c1,c2,diff = 5):
    return abs(c1[0] - c2[0]) <= diff and abs(c1[1] - c2[1])  <= diff and abs(c1[1] - c2[1]) <= diff


def diff_situation(good,target):
    if (good == 1) and (
        target == TargetType.Cloth or 
        target == TargetType.电脑
            
        ):
            return 0.70
    elif (good == 3) and (
        target == TargetType.Food
        ):
            return 0.83
    elif target == TargetType.电脑:
        return 0.75

    elif target == TargetType.矿石:
        return 0.75

    return 0.82
