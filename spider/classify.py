# -*- coding: utf-8 -*-
"""
新闻自动分类：基于标题/正文关键词权重，将稿件归入 10 个标准类别。

类别：时政、国际、社会、科技、健康、教育、文化、娱乐、财经、军事。
入口函数：classify_news_category(title, content, url, origin)
"""

from collections import Counter
import html
import math
import re


CANONICAL_NEWS_CATEGORIES = frozenset(
    {
        "时政",
        "国际",
        "社会",
        "科技",
        "健康",
        "教育",
        "文化",
        "娱乐",
        "财经",
        "军事",
    }
)

CATEGORY_MUTEX_ORDER = [
    "时政",
    "国际",
    "军事",
    "科技",
    "财经",
    "健康",
    "教育",
    "文化",
    "娱乐",
    "社会",
]

_LEGACY_CATEGORY_WEIGHTS = {
    "科技": {
        "科技": 3,
        "科学": 2,
        "技术": 2,
        "创新": 1,
        "研发": 2,
        "科研": 2,
        "研制": 2,
        "实验室": 2,
        "专利": 2,
        "院士": 2,
        "学术": 1,
        "芯片": 3,
        "半导体": 2,
        "人工智能": 3,
        "AI": 2,
        "算法": 2,
        "大模型": 3,
        "互联网": 2,
        "数码": 1,
        "计算机": 2,
        "软件": 1,
        "航天": 2,
        "卫星": 2,
        "火箭": 2,
        "量子": 2,
        "5G": 2,
        "通信": 1,
        "网络": 1,
        "加速器": 3,
        "回旋加速器": 4,
        "同位素": 3,
        "原子能": 3,
        "核电": 2,
        "离子": 1,
        "粒子": 1,
        "材料": 1,
        "能源": 1,
        "新能源": 2,
        "电池": 1,
        "电动车": 1,
        "智能制造": 2,
        "自动化": 1,
        "数字化": 1,
        "光通信": 2,
        "激光": 2,
        "传感器": 2,
        "数控机床": 2,
        "EDA": 2,
        "鸿蒙": 2,
        "安卓": 1,
        "iOS": 1,
        "鸿蒙系统": 2,
    },
    "财经": {
        "财经": 3,
        "金融": 2,
        "股市": 3,
        "A股": 3,
        "港股": 2,
        "证券": 3,
        "基金": 2,
        "期货": 2,
        "银行": 2,
        "保险": 2,
        "理财": 2,
        "央行": 2,
        "降准": 2,
        "降息": 2,
        "汇率": 2,
        "人民币": 1,
        "通胀": 2,
        "物价": 2,
        "上市公司": 2,
        "财报": 3,
        "营收": 2,
        "利润": 1,
        "涨停": 3,
        "收盘": 2,
        "开盘": 2,
        "股指": 2,
        "新三板": 2,
        "创业板": 2,
        "融资融券": 2,
        "消费税改": 2,
        "减税降费": 2,
        "营商环境": 1,
        "反垄断": 2,
        "金融监管": 2,
    },
    "娱乐": {
        "娱乐": 3,
        "电影": 2,
        "电视剧": 2,
        "明星": 2,
        "综艺": 2,
        "音乐": 1,
        "票房": 2,
        "艺人": 2,
        "演唱会": 1,
        "动漫": 2,
        "体育": 3,
        "足球": 2,
        "篮球": 2,
        "奥运": 2,
        "比赛": 1,
        "联赛": 2,
        "世界杯": 2,
        "运动员": 2,
        "CBA": 2,
        "NBA": 2,
        "网球": 1,
        "游泳": 1,
        "排球": 1,
        "田径": 1,
        "马拉松": 1,
        "电竞比赛": 2,
    },
    "军事": {
        "军事": 3,
        "国防": 2,
        "军演": 2,
        "演习": 2,
        "导弹": 2,
        "战机": 2,
        "海军": 2,
        "空军": 2,
        "陆军": 2,
        "武器": 2,
        "军售": 3,
        "护卫舰": 4,
        "驱逐舰": 3,
        "军舰": 3,
        "舰艇": 2,
        "潜艇": 2,
        "航母": 2,
        "装甲": 1,
        "兵力": 1,
        "军费": 1,
        "火箭军": 3,
        "战略支援": 3,
        "空降兵": 2,
        "陆战队": 2,
        "边防": 2,
    },
    "教育": {
        "教育": 2,
        "高校": 2,
        "中小学": 2,
        "高考": 2,
        "考研": 2,
        "招生": 1,
        "课堂": 1,
        "教师": 1,
        "学校": 1,
        "义务教育法": 2,
        "职业教育法": 2,
        "学前教育": 1,
        "特殊教育": 1,
        "师德": 1,
    },
    "社会": {
        "社会": 2,
        "民生": 2,
        "交通": 1,
        "治安": 1,
        "事故": 1,
        "救援": 1,
        "公益": 1,
        "社区": 1,
        "全球": 1,
        "海外": 1,
        "欧洲": 1,
        "中东": 1,
        "舆情": 1,
        "突发事件": 2,
        "自然灾害": 2,
        "应急": 1,
    },
}

_TECH_BODY_PLATFORM_NOISE = (
    "哔哩哔哩",
    "小红书",
    "拼多多",
    "抖音",
    "快手",
    "淘宝",
    "天猫",
    "京东商城",
    "京东",
    "美团",
    "微信",
    "微博",
    "支付宝",
    "B站",
    "Ｂ站",
)

_TECH_WEAK_BODY_DEMOTE = {
    "互联网": 0.22,
    "网络": 0.35,
    "数字化": 0.45,
    "智能": 0.5,
}

CLASSIFY_STOP_WORDS = frozenset(
    {
        "我们",
        "你们",
        "他们",
        "这个",
        "那个",
        "进行",
        "有关",
        "表示",
        "记者",
        "新闻",
        "中国",
        "一个",
        "可以",
        "没有",
        "已经",
        "现在",
        "这样",
        "这种",
        "通过",
        "作为",
        "因为",
        "所以",
        "如果",
        "但是",
        "还是",
        "或者",
        "以及",
        "什么",
        "如何",
        "怎么",
        "为什么",
        "是否",
        "不能",
        "需要",
        "认为",
        "指出",
        "介绍",
        "根据",
        "目前",
        "今日",
        "今年",
        "去年",
        "近日",
        "今天",
        "昨天",
        "明天",
        "相关",
        "之一",
        "随着",
        "同时",
        "此外",
        "其中",
        "部分",
        "一些",
        "出现",
        "发现",
        "问题",
        "情况",
        "工作",
        "方面",
        "领域",
        "时间",
        "地点",
        "人员",
        "公司",
        "市场",
        "企业",
        "平台",
        "用户",
        "内容",
        "信息",
        "数据",
        "服务",
        "产品",
        "方式",
        "过程",
        "结果",
        "影响",
        "关注",
        "报道",
        "显示",
        "提供",
        "发布",
        "称",
        "说",
        "到",
        "在",
        "和",
        "与",
        "及",
        "等",
        "对",
        "为",
        "将",
        "被",
        "从",
        "向",
        "由",
        "把",
        "给",
        "让",
        "使",
        "之",
        "其",
        "该",
        "此",
        "某",
        "者",
        "吗",
        "呢",
        "吧",
        "啊",
        "嘛",
        "谁在给",
        "之类",
        "那样",
    }
)

TITLE_STRONG_MUL = 4.2
TITLE_WEAK_MUL = 1.75
BODY_STRONG_MUL = 1.05
BODY_WEAK_MUL = 0.28
TFIDF_TOPIC_WEIGHT = 2.4
TITLE_TOKEN_REPEAT = 3
CLASSIFY_SCORE_FLOOR = 0.22
CLASSIFY_TIE_DELTA = 0.45

KEYWORD_LEXICON_EXTRA = {
    "时政": {
        "strong": {
            "全国人大常委会": 6.0,
            "全国人大": 5.5,
            "全国政协": 5.5,
            "两会": 6.0,
            "立法": 4.0,
            "修法": 4.0,
            "依法治国": 5.0,
            "反腐": 4.0,
            "中央纪委": 5.0,
            "巡视": 3.5,
            "外交部": 4.5,
            "国防部": 4.5,
            "国台办": 4.5,
            "台海": 4.0,
            "一国两制": 4.0,
            "国安": 4.0,
            "总体国家安全观": 5.0,
            "乡村振兴": 4.0,
            "共同富裕": 4.0,
            "深化改革": 4.0,
            "自贸试验区": 3.5,
            "一带一路": 4.0,
            "会见": 3.0,
            "出访": 3.5,
            "国事访问": 4.0,
            "公报": 3.5,
            "中央财经委员会": 5.0,
            "中纪委": 5.0,
            "检察院": 6.0,
            "检察机关": 6.0,
            "人民检察院": 6.0,
            "公诉": 6.0,
            "依法起诉": 6.0,
            "审查起诉": 5.5,
            "纪委监委": 6.0,
            "监委": 5.5,
            "腐败": 5.0,
            "受贿": 5.0,
            "违纪违法": 5.5,
            "政协": 4.5,
            "常委会": 4.0,
        },
        "weak": {
            "常委会": 2.0,
            "文件精神": 2.0,
            "贯彻落实": 1.8,
            "工作部署": 1.8,
            "党组": 2.0,
            "人大代表": 2.0,
            "政协委员": 2.0,
        },
    },
    "国际": {
        "strong": {
            "联合国安理会": 7.0,
            "联合国大会": 6.5,
            "中国常驻联合国": 6.5,
            "国际秩序": 5.0,
            "国际安全": 5.0,
            "国际争端": 4.5,
            "停火谈判": 4.5,
            "外交斡旋": 5.5,
            "地区局势": 4.8,
            "涉台": 4.5,
            "台海和平": 4.5,
            "东海局势": 4.2,
            "南海局势": 4.2,
            "跨境": 3.5,
            "国际组织": 4.5,
            "驻外大使": 4.8,
            "使馆发言人": 4.2,
            "国际会议": 4.0,
            "外事活动": 4.0,
        },
        "weak": {
            "外方": 1.8,
            "双边": 2.2,
            "多边": 2.0,
            "倡议": 1.8,
            "代表团": 1.8,
        },
    },
    "社会": {
        "strong": {
            "火灾": 3.5,
            "地震": 3.5,
            "洪涝": 3.5,
            "台风": 3.0,
            "安全生产": 3.5,
            "交通事故": 3.0,
            "欠薪": 3.0,
            "志愿服务": 2.5,
            "慈善": 2.5,
            "留守儿童": 3.0,
            "老龄化": 2.5,
            "户籍改革": 3.0,
            "社保": 2.5,
            "养老金": 2.5,
            "医保异地": 3.0,
            "就业": 2.0,
            "讨薪": 3.0,
            "家暴": 3.5,
            "拐卖": 3.5,
            "电信诈骗": 3.5,
            "扫黑除恶": 3.5,
        },
        "weak": {
            "暖心": 1.2,
            "感动": 1.0,
            "寻人": 2.0,
            "失踪": 2.0,
            "辟谣": 2.0,
            "通报": 1.5,
            "警情": 2.0,
            "消防": 2.5,
            "交警": 2.0,
            "城管": 1.5,
            "基层治理": 2.0,
            "网格化": 1.8,
        },
    },
    "科技": {
        "strong": {
            "载人航天": 4.0,
            "空间站": 4.0,
            "北斗": 3.5,
            "嫦娥": 3.5,
            "神舟": 3.5,
            "天宫": 3.5,
            "深空探测": 4.0,
            "光刻机": 4.0,
            "操作系统": 3.0,
            "开源": 2.5,
            "区块链": 3.0,
            "元宇宙": 2.5,
            "工业互联网": 3.5,
            "物联网": 3.0,
            "云计算": 3.0,
            "边缘计算": 3.0,
            "自动驾驶": 3.5,
            "光伏": 2.5,
            "储能": 2.5,
            "工业机器人": 3.5,
            "无人机": 3.0,
            "3D打印": 3.0,
            "超算": 3.5,
            "纳米": 2.5,
            "石墨烯": 3.0,
            "可控核聚变": 4.0,
            "DeepSeek": 3.0,
            "ChatGPT": 3.0,
        },
        "weak": {
            "数字化转型的": 1.5,
            "信息化": 1.5,
            "国产替代": 2.0,
            "卡脖子": 2.5,
            "攻关": 1.5,
            "产学研": 2.0,
            "高新技术企业": 2.0,
            "专精特新": 2.5,
            "数据中心": 2.0,
            "算力": 2.5,
        },
    },
    "健康": {
        "strong": {
            "新冠疫情": 4.0,
            "流感病毒": 3.5,
            "肿瘤": 3.5,
            "癌症": 3.5,
            "心脑血管": 3.5,
            "糖尿病": 3.0,
            "高血压": 2.5,
            "中医药": 3.5,
            "抗生素": 3.0,
            "处方药": 3.0,
            "医保谈判": 3.5,
            "集采": 3.5,
            "分级诊疗": 3.5,
            "家庭医生": 3.0,
            "互联网医院": 3.5,
            "核酸检测": 3.0,
            "发热门诊": 3.0,
            "ICU": 3.5,
            "急诊科": 3.0,
            "儿科": 2.5,
            "妇产科": 2.5,
            "精神卫生": 4.0,
            "抑郁症": 3.5,
            "阿尔茨海默": 3.5,
        },
        "weak": {
            "医嘱": 1.5,
            "复查": 1.5,
            "挂号": 1.5,
            "门诊": 1.5,
            "住院": 1.5,
            "慢病": 2.0,
            "亚健康": 2.0,
            "戒烟": 1.5,
            "膳食": 1.5,
        },
    },
    "教育": {
        "strong": {
            "义务教育": 3.5,
            "双减": 4.0,
            "职业教育": 3.5,
            "双一流": 4.0,
            "学科评估": 3.0,
            "师德师风": 3.5,
            "校园欺凌": 3.5,
            "校车安全": 3.0,
            "学位论文": 2.5,
            "中考": 3.0,
            "小升初": 2.5,
            "学区房": 2.5,
            "校外培训": 3.5,
            "在线教育": 3.0,
            "职业教育法": 3.5,
        },
        "weak": {
            "班主任": 1.5,
            "家长会": 1.2,
            "课后服务": 1.8,
            "减负": 2.0,
            "素质教育": 2.0,
            "美育": 1.8,
            "劳动教育": 2.0,
            "家校共育": 2.0,
        },
    },
    "文化": {
        "strong": {
            "世界遗产": 4.0,
            "文化遗产": 4.0,
            "古籍保护": 3.5,
            "美术馆": 3.0,
            "文化馆": 3.0,
            "交响乐团": 3.0,
            "京剧": 3.5,
            "昆曲": 3.5,
            "诗词大会": 3.0,
            "国学热": 3.0,
            "纪录片": 2.5,
            "文物保护": 4.0,
            "石窟": 3.5,
            "敦煌": 3.5,
        },
        "weak": {
            "书香": 1.5,
            "文脉": 2.0,
            "文创": 2.0,
            "文旅": 2.0,
            "研学": 1.8,
            "非遗传承人": 3.0,
            "传承人": 2.5,
        },
    },
    "娱乐": {
        "strong": {
            "真人秀": 3.0,
            "脱口秀": 3.0,
            "收视率": 2.5,
            "票房冠军": 3.0,
            "档期": 2.0,
            "红毯": 2.5,
            "粉丝应援": 2.5,
            "电竞": 3.5,
            "电子竞技": 3.5,
            "主机游戏": 2.5,
            "手游": 3.0,
            "网游": 3.0,
            "MV": 2.0,
            "专辑销量": 2.5,
            "冬奥会": 3.5,
            "亚运会": 3.5,
            "全运会": 3.0,
            "斯诺克": 2.5,
            "乒乓球": 2.5,
            "羽毛球": 2.5,
        },
        "weak": {
            "追剧": 1.5,
            "路透": 1.5,
            "番位": 1.5,
            "塌房": 2.0,
            "吃瓜": 1.2,
            "路透图": 1.5,
            "花絮": 1.5,
        },
    },
    "财经": {
        "strong": {
            "美联储": 3.5,
            "加息": 3.0,
            "GDP": 3.0,
            "CPI": 3.0,
            "PPI": 3.0,
            "科创板": 3.5,
            "北交所": 3.5,
            "IPO": 3.5,
            "并购重组": 3.0,
            "债券违约": 3.5,
            "信托产品": 2.5,
            "房地产税": 3.5,
            "消费税": 3.0,
            "数字货币": 3.0,
            "比特币": 2.5,
            "原油": 2.5,
            "大宗商品": 3.0,
            "供给侧改革": 3.5,
            "消费升级": 2.5,
            "外贸": 2.5,
            "顺差": 2.5,
            "逆差": 2.5,
            "外汇储备": 3.0,
        },
        "weak": {
            "财报季": 2.0,
            "业绩快报": 2.0,
            "股东": 1.5,
            "减持": 2.0,
            "增持": 2.0,
            "分红": 2.0,
            "估值": 2.0,
            "市盈率": 2.0,
            "做空": 2.5,
            "多头": 1.5,
            "空头": 1.5,
        },
    },
    "军事": {
        "strong": {
            "歼20": 4.5,
            "歼击机": 4.0,
            "辽宁舰": 4.0,
            "山东舰": 4.0,
            "福建舰": 4.0,
            "航母编队": 4.0,
            "东风导弹": 4.5,
            "洲际弹道导弹": 4.5,
            "核潜艇": 4.0,
            "军工集团": 4.0,
            "武器贸易": 3.5,
            "防空识别区": 4.0,
            "联合作战": 4.0,
            "信息化战争": 4.0,
            "无人作战": 3.5,
            "南海局势": 3.5,
            "东海防空": 3.5,
            "台海军演": 4.5,
            "绕台": 4.0,
            "美日军演": 3.5,
        },
        "weak": {
            "国防部发言人": 3.0,
            "军迷": 1.2,
            "军援": 2.5,
            "军贸": 2.5,
            "兵棋": 1.5,
            "军衔": 1.5,
            "授衔": 2.0,
        },
    },
}


def _merge_keyword_lexicon_extra(layers: dict) -> dict:
    for cat, pack in KEYWORD_LEXICON_EXTRA.items():
        if cat not in layers:
            continue
        for kw, wt in pack.get("strong", {}).items():
            layers[cat]["strong"][kw] = float(wt)
            layers[cat]["weak"].pop(kw, None)
        for kw, wt in pack.get("weak", {}).items():
            if kw not in layers[cat]["strong"]:
                layers[cat]["weak"][kw] = float(wt)
    return layers


def _init_category_keyword_layers():
    layers = {}
    for cat, wdict in _LEGACY_CATEGORY_WEIGHTS.items():
        layers[cat] = {"strong": {}, "weak": dict(wdict)}

    layers["健康"] = {
        "strong": {
            "医院": 4.0,
            "诊疗": 4.0,
            "疾控": 4.0,
            "公共卫生": 4.0,
            "医保": 3.0,
            "康复": 3.0,
            "营养": 2.5,
            "养生": 2.0,
            "体检": 3.0,
            "心理健康": 4.0,
            "流行病": 3.5,
            "中成药": 3.0,
            "手术": 3.0,
        },
        "weak": {
            "健康": 2.5,
            "医疗": 2.5,
            "患者": 1.5,
            "症状": 1.5,
            "护理": 1.5,
        },
    }
    health_from_tech = {
        "疫苗": 4.0,
        "生物医药": 3.5,
        "医疗器械": 3.5,
        "临床": 2.5,
        "诊断": 2.5,
        "药物": 2.5,
        "医用": 2.5,
        "核医学": 3.5,
    }
    for k, w in health_from_tech.items():
        if k in layers["科技"]["weak"]:
            layers["科技"]["weak"].pop(k)
            layers["健康"]["strong"][k] = w

    layers["文化"] = {
        "strong": {
            "文学": 3.5,
            "非遗": 4.0,
            "博物馆": 4.0,
            "文物": 3.5,
            "出版": 2.5,
            "传统文化": 4.0,
            "艺术": 3.0,
            "展览": 2.5,
            "阅读": 2.5,
            "书法": 2.5,
            "戏剧": 2.5,
            "民俗": 3.0,
            "考古": 3.0,
            "读书": 2.0,
        },
        "weak": {"文化": 2.5, "历史": 1.5, "典籍": 2.0},
    }

    layers["时政"] = {
        "strong": {
            "人民网观点": 10.0,
            "人民时评": 9.0,
            "人民网评": 8.5,
            "人民日报": 7.0,
            "新华社": 8.0,
            "新华网": 7.0,
            "新华视点": 7.5,
            "光明日报": 6.0,
            "经济日报": 6.0,
            "学习强国": 6.0,
            "求是": 6.0,
            "评论员": 5.0,
            "评论员文章": 6.0,
            "政策解读": 5.0,
            "国务院": 6.0,
            "部委": 4.0,
            "党务": 5.0,
            "党建": 5.0,
            "政务": 5.0,
            "督察": 4.0,
            "专项整治": 4.0,
            "清朗": 4.0,
            "意识形态": 4.0,
            "舆论监督": 4.0,
            "网信": 4.0,
            "禁播": 3.0,
            "时政": 5.0,
            "外交": 4.0,
            "联合国": 3.5,
        },
        "weak": {
            "政策": 2.0,
            "监管": 1.8,
            "舆情": 1.5,
            "关切": 1.2,
            "治理": 1.8,
            "合规": 1.5,
            "国际": 1.8,
        },
    }

    layers["国际"] = {
        "strong": {
            "国际": 6.0,
            "国际局势": 6.0,
            "国际关系": 5.5,
            "外交": 5.0,
            "外交部": 5.5,
            "驻外使馆": 5.0,
            "联合国": 6.0,
            "安理会": 6.0,
            "联大": 5.0,
            "多边机制": 4.5,
            "国际法": 4.5,
            "地缘政治": 4.5,
            "地区冲突": 4.5,
            "停火": 4.0,
            "斡旋": 4.0,
            "东海": 4.2,
            "南海": 4.2,
            "台海": 4.6,
            "亚太": 4.0,
            "欧盟": 4.0,
            "北约": 4.2,
            "中东": 4.0,
            "金砖": 4.5,
            "上合组织": 4.5,
            "G20": 4.0,
            "世界银行": 4.0,
            "国际原子能机构": 4.0,
            "峰会": 3.5,
            "会晤": 3.5,
            "出访": 3.5,
        },
        "weak": {
            "海外": 2.0,
            "全球": 2.0,
            "国际社会": 2.5,
            "跨国": 2.0,
            "外长": 2.0,
            "使节": 2.0,
            "驻华": 1.8,
            "边境": 1.8,
            "海域": 1.8,
            "局势": 1.6,
            "和平稳定": 2.0,
        },
    }

    for k in (
        "芯片",
        "半导体",
        "大模型",
        "人工智能",
        "算法",
        "量子",
        "专利",
        "航天",
        "卫星",
        "火箭",
        "回旋加速器",
        "同位素",
        "原子能",
    ):
        if k in layers["科技"]["weak"]:
            layers["科技"]["strong"][k] = layers["科技"]["weak"].pop(k)
    for k in ("电影", "电视剧", "明星", "综艺", "演唱会", "动漫"):
        if k in layers["娱乐"]["weak"]:
            layers["娱乐"]["strong"][k] = layers["娱乐"]["weak"].pop(k)
    for k in ("足球", "篮球", "奥运", "世界杯", "联赛", "运动员", "CBA", "NBA"):
        if k in layers["娱乐"]["weak"]:
            layers["娱乐"]["strong"][k] = layers["娱乐"]["weak"].pop(k)
    for k in ("股市", "A股", "财报", "涨停", "证券", "期货"):
        if k in layers["财经"]["weak"]:
            layers["财经"]["strong"][k] = layers["财经"]["weak"].pop(k)

    _merge_keyword_lexicon_extra(layers)
    if set(layers.keys()) != CANONICAL_NEWS_CATEGORIES:
        raise RuntimeError(
            "CATEGORY_KEYWORD_LAYERS keys must match CANONICAL_NEWS_CATEGORIES: "
            f"{sorted(layers.keys())}"
        )
    return layers


CATEGORY_KEYWORD_LAYERS = _init_category_keyword_layers()


def clean_text_for_classify(s: str) -> str:
    if s is None:
        return ""
    s = html.unescape(str(s))
    s = re.sub(r"[\u200b\u200c\u200d\ufeff]", "", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def _phrase_in_text(phrase: str, text: str) -> bool:
    if not phrase or not text:
        return False
    if phrase.isascii():
        return phrase.lower() in text.lower()
    return phrase in text


def _strip_tech_body_noise(body: str) -> str:
    s = body
    for w in sorted(_TECH_BODY_PLATFORM_NOISE, key=len, reverse=True):
        s = s.replace(w, " ")
    return s


def _official_media_boost(url: str, origin: str, title_c: str) -> dict:
    u = (url or "").lower()
    o = (origin or "") + (title_c or "")
    b = {}
    if "opinion.people.com.cn" in u:
        b["时政"] = b.get("时政", 0) + 5.0
    elif "people.com.cn" in u or "人民网" in o:
        b["时政"] = b.get("时政", 0) + 3.0
    if "xinhuanet.com" in u or "新华社" in o or "新华网" in o:
        b["时政"] = b.get("时政", 0) + 2.5
    if "gov.cn" in u and "国务院" in o:
        b["时政"] = b.get("时政", 0) + 2.0
    if any(k in u for k in ("world.people.com.cn", "news.un.org", "un.org")):
        b["国际"] = b.get("国际", 0) + 3.5
    if any(k in o for k in ("联合国", "安理会", "外交部", "中国常驻联合国", "国际局势")):
        b["国际"] = b.get("国际", 0) + 3.0
    return b


def _tokenize_for_classify(text: str) -> list:
    if not text:
        return []
    text = re.sub(r"[\s\d]+", " ", text)
    out = []
    for m in re.finditer(r"[\u4e00-\u9fff]{2,14}|[A-Za-z][A-Za-z0-9]{2,18}", text):
        w = m.group(0)
        wl = w.lower() if w.isascii() else w
        if wl in CLASSIFY_STOP_WORDS or (w.isascii() and len(w) < 3):
            continue
        out.append(wl)
    return out


def _build_layer_profile_tokens(layers_entry: dict) -> list:
    toks = []
    for ph, wt in layers_entry.get("strong", {}).items():
        toks.extend([ph] * max(1, min(12, int(round(float(wt))))))
    for ph, wt in layers_entry.get("weak", {}).items():
        toks.extend([ph] * max(1, min(6, int(round(float(wt))))))
    return _tokenize_for_classify(" ".join(toks))


def _compute_idf(corpus_docs: list) -> dict:
    n_docs = len(corpus_docs) or 1
    df = Counter()
    for doc in corpus_docs:
        df.update(set(doc))
    idf = {}
    for token, count in df.items():
        idf[token] = math.log((n_docs + 1.0) / (count + 1.0)) + 1.0
    return idf


def _tfidf_vector(tokens: list, idf: dict) -> dict:
    if not tokens:
        return {}
    tf = Counter(tokens)
    total = sum(tf.values()) or 1
    vec = {}
    for token, count in tf.items():
        if token in idf:
            vec[token] = (count / total) * idf[token]
    return vec


def _vec_dot(a: dict, b: dict) -> float:
    if not a or not b:
        return 0.0
    score = 0.0
    for key in a:
        if key in b:
            score += a[key] * b[key]
    return score


def _vec_norm(v: dict) -> float:
    return math.sqrt(sum(x * x for x in v.values())) if v else 0.0


def _cosine_sparse(a: dict, b: dict) -> float:
    na = _vec_norm(a)
    nb = _vec_norm(b)
    if na <= 0 or nb <= 0:
        return 0.0
    return _vec_dot(a, b) / (na * nb)


def _build_tfidf_profiles():
    cats = list(CATEGORY_KEYWORD_LAYERS.keys())
    corpus = [_build_layer_profile_tokens(CATEGORY_KEYWORD_LAYERS[c]) for c in cats]
    idf = _compute_idf(corpus)
    profiles = {}
    for cat, doc in zip(cats, corpus):
        profiles[cat] = _tfidf_vector(doc, idf)
    return idf, profiles


_CLASSIFY_IDF, _CLASSIFY_CAT_TFIDF = _build_tfidf_profiles()


def classify_news_category(title: str, content: str, url: str = "", origin: str = "") -> str:
    title_c = clean_text_for_classify(title)
    body_c = clean_text_for_classify(content)
    body_tech = _strip_tech_body_noise(body_c)
    if not title_c and not body_c:
        return "综合"

    scores = {cat: 0.0 for cat in CATEGORY_KEYWORD_LAYERS}
    for cat, layers in CATEGORY_KEYWORD_LAYERS.items():
        for phrase, weight in layers.get("strong", {}).items():
            w = float(weight)
            in_title = _phrase_in_text(phrase, title_c)
            in_body = _phrase_in_text(phrase, body_tech if cat == "科技" else body_c)
            if in_title:
                scores[cat] += w * TITLE_STRONG_MUL
            if in_body:
                scores[cat] += w * BODY_STRONG_MUL
        for phrase, weight in layers.get("weak", {}).items():
            w = float(weight)
            in_title = _phrase_in_text(phrase, title_c)
            in_body = _phrase_in_text(phrase, body_tech if cat == "科技" else body_c)
            if in_title:
                scores[cat] += w * TITLE_WEAK_MUL
            if in_body:
                body_weight = w
                if cat == "科技" and phrase in _TECH_WEAK_BODY_DEMOTE:
                    body_weight *= _TECH_WEAK_BODY_DEMOTE[phrase]
                scores[cat] += body_weight * BODY_WEAK_MUL

    for cat, add in _official_media_boost(url, origin, title_c).items():
        scores[cat] = scores.get(cat, 0.0) + add

    doc_tokens = _tokenize_for_classify(title_c) * TITLE_TOKEN_REPEAT + _tokenize_for_classify(body_c)
    query_vector = _tfidf_vector(doc_tokens, _CLASSIFY_IDF)
    for cat in scores:
        sim = _cosine_sparse(query_vector, _CLASSIFY_CAT_TFIDF.get(cat, {}))
        scores[cat] += TFIDF_TOPIC_WEIGHT * max(0.0, sim)

    governance_text = (title_c + " " + body_c).lower()
    if re.search(r"(检察|公诉|审查起诉|纪委|监委|违纪|受贿|政协|人大常委会|依法起诉)", governance_text):
        scores["时政"] = scores.get("时政", 0.0) + 10.0
        scores["财经"] = scores.get("财经", 0.0) * 0.55

    if re.search(r"(联合国|安理会|常驻联合国|外交部|驻外使馆|东海局势|南海局势|台海局势)", governance_text):
        scores["国际"] = scores.get("国际", 0.0) + 8.0
        scores["军事"] = scores.get("军事", 0.0) * 0.7

    best = max(scores.values()) if scores else 0.0
    if best < CLASSIFY_SCORE_FLOOR:
        return "综合"

    top = max(scores, key=scores.get)
    top_score = scores[top]
    near = [cat for cat, score in scores.items() if score >= top_score - CLASSIFY_TIE_DELTA and score > 0]
    if len(near) <= 1:
        return top
    for preferred in CATEGORY_MUTEX_ORDER:
        if preferred in near:
            return preferred
    return top
