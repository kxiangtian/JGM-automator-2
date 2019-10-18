from target import TargetType

JGM_tag = "com.tencent.jgm"

# 货物的那个叉叉的位置 相对位置
CROSS_POSITIONS = { 1: (0.632, 0.878),
                    2: (0.776, 0.836),
                    3: (991/1080, 1517/1920)}

CONSTANT_ITEM = {
           "便利店"  : TargetType.Bottle,
           "钢结构房": TargetType.Sofa,
           "造纸厂"  : TargetType.Grass,
           "木材厂"  : TargetType.Wood,
           "图书城"  : TargetType.Book,
           "钢铁厂"  : TargetType.矿石,
           "学校"    : TargetType.书包,
           "居民楼"  : TargetType.快递,
           "木屋"    : TargetType.Chair,
           "人オ公寓": TargetType.电脑,
           "平房"    : TargetType.花盆,
           "菜市场"  : TargetType.Vegetable,
           "食品厂"  : TargetType.Food,
           "中式小楼": TargetType.Quilt,
           "媒体之声": TargetType.话筒,
           "民食斋"  : TargetType.烧鸡,
           "空中别墅": TargetType.时尚吊灯,
           "服装店"  : TargetType.cloth,
           "纺织厂"  : TargetType.cotton

           #"电厂":    TargetType.
}