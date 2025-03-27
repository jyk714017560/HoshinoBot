'''公主连接Re:dive的游戏数据'''


'''角色名称

遵照格式： id: [台服官译简体, 日文原名, 英文名(罗马音), B服官译, 常见别称, 带错别字的别称等] （<-依此顺序）
若暂无台服官译则用日文原名占位，台日用全角括号，英文用半角括号
'''
CHARA_NAME = {
    1000: ["未知角色", "未知キャラ", "Unknown"],
    1001: ["日和", "ヒヨリ", "Hiyori", "日和莉", "猫拳", "🐱👊", "猫咪"],
    1002: ["优衣", "ユイ", "Yui", "种田", "普田", "由衣", "结衣", "ue", "↗↘↗↘"],
    1003: ["怜", "レイ", "Rei", "剑圣", "普怜", "伶"],
    1004: ["禊", "ミソギ", "Misogi", "未奏希", "炸弹", "炸弹人", "💣"],
    1005: ["茉莉", "マツリ", "Matsuri", "跳跳虎", "老虎", "虎", "🐅"],
    1006: ["茜里", "アカリ", "Akari", "妹法", "妹妹法"],
    1007: ["宫子", "ミヤコ", "Miyako", "布丁", "布", "🍮"],
    1008: ["雪", "ユキ", "Yuki", "小雪", "镜子", "镜法", "伪娘", "男孩子", "男孩纸"],
    1009: ["杏奈", "アンナ", "Anna", "中二", "煤气罐"],
    1010: ["真步", "マホ", "Maho", "狐狸", "真扎", "咕噜灵波", "真布", "🦊"],
    1011: ["璃乃", "リノ", "Rino", "妹弓"],
    1012: ["初音", "ハツネ", "Hatsune", "hego", "星法", "星星法", "⭐法", "睡法"],
    1013: ["七七香", "ナナカ", "Nanaka", "娜娜卡", "77k", "77香"],
    1014: ["霞", "カスミ", "Kasumi", "香澄", "侦探", "杜宾犬", "驴", "驴子", "🔍"],
    1015: ["美里", "ミサト", "Misato", "圣母"],
    1016: ["铃奈", "スズナ", "Suzuna", "暴击弓", "暴弓", "爆击弓", "爆弓", "政委"],
    1017: ["香织", "カオリ", "Kaori", "琉球犬", "狗子", "狗", "狗拳", "🐶", "🐕", "🐶👊🏻", "🐶👊"],
    1018: ["伊绪", "イオ", "Io", "老师", "魅魔"],

    1020: ["美美", "ミミ", "Mimi", "兔子", "兔兔", "兔剑", "萝卜霸断剑", "人参霸断剑", "天兔霸断剑", "🐇", "🐰"],
    1021: ["胡桃", "クルミ", "Kurumi", "铃铛", "🔔"],
    1022: ["依里", "ヨリ", "Yori", "姐法", "姐姐法"],
    1023: ["绫音", "アヤネ", "Ayane", "熊锤", "🐻🔨", "🐻"],

    1025: ["铃莓", "スズメ", "Suzume", "女仆", "妹抖"],
    1026: ["铃", "リン", "Rin", "松鼠", "🐿", "🐿️"],
    1027: ["惠理子", "エリコ", "Eriko", "病娇"],
    1028: ["咲恋", "サレン", "Saren", "充电宝", "青梅竹马", "幼驯染", "院长", "园长", "🔋", "普电"],
    1029: ["望", "ノゾミ", "Nozomi", "偶像", "小望", "🎤"],
    1030: ["妮诺", "ニノン", "Ninon", "妮侬", "扇子"],
    1031: ["忍", "シノブ", "Shinobu", "普忍", "鬼父", "💀"],
    1032: ["秋乃", "アキノ", "Akino", "哈哈剑","恰恰剑"],
    1033: ["真阳", "マヒル", "Mahiru", "奶牛", "🐄", "🐮", "真☀"],
    1034: ["优花梨", "ユカリ", "Yukari", "由加莉", "黄骑", "酒鬼", "奶骑", "圣骑", "🍺", "🍺👻"],

    1036: ["镜华", "キョウカ", "Kyouka", "小仓唯", "xcw", "小苍唯", "8岁", "八岁", "喷水萝", "八岁喷水萝", "8岁喷水萝"],
    1037: ["智", "トモ", "Tomo", "卜毛"],
    1038: ["栞", "シオリ", "Shiori", "tp弓", "小栞", "白虎弓", "白虎妹"],

    1040: ["碧", "アオイ", "Aoi", "香菜", "香菜弓", "绿毛弓", "毒弓", "绿帽弓", "绿帽"],

    1042: ["千歌", "チカ", "Chika", "绿毛奶"],
    1043: ["真琴", "マコト", "Makoto", "狼", "🐺", "月月", "朋", "狼姐"],
    1044: ["伊莉亚", "イリヤ", "Iriya", "伊利亚", "伊莉雅", "伊利雅", "yly", "吸血鬼", "那个女人"],
    1045: ["空花", "クウカ", "Kuuka", "抖m", "抖"],
    1046: ["珠希", "タマキ", "Tamaki", "猫剑", "🐱剑", "🐱🗡️"],
    1047: ["纯", "ジュン", "Jun", "黑骑", "saber"],
    1048: ["美冬", "ミフユ", "Mifuyu", "子龙", "赵子龙"],
    1049: ["静流", "シズル", "Shizuru", "姐姐"],
    1050: ["美咲", "ミサキ", "Misaki", "大眼", "👀", "👁️", "👁"],
    1051: ["深月", "ミツキ", "Mitsuki", "眼罩", "抖s"],
    1052: ["莉玛", "リマ", "Rima", "Lima", "草泥马", "羊驼", "🦙", "🐐"],
    1053: ["莫妮卡", "モニカ", "Monika", "毛二力"],
    1054: ["纺希", "ツムギ", "Tsumugi", "裁缝", "蜘蛛侠", "🕷️", "🕸️"],
    1055: ["步未", "アユミ", "Ayumi", "步美", "路人", "路人妹"],
    1056: ["流夏", "ルカ", "Ruka", "大姐", "大姐头", "儿力", "luka", "刘夏"],
    1057: ["吉塔", "ジータ", "Jiita", "姬塔", "团长", "吉他", "🎸", "骑空士", "qks"],
    1058: ["贪吃佩可", "ペコリーヌ", "Pecoriinu", "佩可莉姆", "吃货", "佩可", "公主", "饭团", "🍙"],
    1059: ["可可萝", "コッコロ", "Kokkoro", "可可罗", "妈", "普白"],
    1060: ["凯留", "キャル", "Kyaru", "凯露", "百地希留耶", "希留耶", "Kiruya", "黑猫", "臭鼬", "普黑", "接头霸王", "街头霸王", "猫猫头"],
    1061: ["矛依未", "ムイミ", "Muimi", "诺维姆", "Noemu", "夏娜", "511", "无意义", "天楼霸断剑"],

    1063: ["亚里莎", "アリサ", "Arisa", "鸭梨瞎", "瞎子", "亚里沙", "鸭梨傻", "亚丽莎", "亚莉莎", "瞎子弓", "🍐🦐", "yls"],
    1064: ["雪菲","シェフィ","Shefi"],
    1065: ["嘉夜", "カヤ", "Kaya", "憨憨龙", "龙拳", "🐲👊🏻", "🐉👊🏻", "接龙笨比"],
    1066: ["祈梨", "イノリ", "Inori", "梨老八", "李老八", "龙锤"],
    1067: ["穗希", "ホマレ", "Homare", "龙妈","帆希"],
    1068: ["拉比林斯达", "ラビリスタ", "Rabirisuta", "迷宫女王", "模索路晶", "模索路", "晶"],
    1069: ["真那", "マナ", "Mana", "霸瞳皇帝", "千里真那", "千里", "霸瞳", "霸铜"],
    1070: ["似似花", "ネネカ", "Neneka", "变貌大妃", "现士实似似花", "現士実似々花", "現士実", "现士实", "nnk", "448", "捏捏卡", "变貌", "大妃"],
    1071: ["克莉丝提娜", "クリスティーナ", "Kurisutiina", "誓约女君", "克莉丝提娜·摩根", "Christina", "Cristina", "克总", "女帝", "克", "摩根"],
    1072: ["可萝爹", "長老", "Chourou", "岳父", "爷爷"],
    1073: ["拉基拉基", "ラジニカーント", "Rajinigaanto", "跳跃王", "Rajiraji", "Lajilaji", "垃圾垃圾", "教授"],

    1075: ["贪吃佩可(夏日)", "ペコリーヌ(サマー)", "Pekoriinu(Summer)", "佩可莉姆(夏日)", "水吃", "水饭", "水吃货", "水佩可", "水公主", "水饭团", "水🍙", "泳吃", "泳饭", "泳吃货", "泳佩可", "泳公主", "泳饭团", "泳🍙", "泳装吃货", "泳装公主", "泳装饭团", "泳装🍙", "佩可(夏日)", "🥡", "👙🍙", "泼妇"],
    1076: ["可可萝(夏日)", "コッコロ(サマー)", "Kokkoro(Summer)", "水白", "水妈", "水可", "水可可", "水可可萝", "水可可罗", "泳装妈", "泳装可可萝", "泳装可可罗"],
    1077: ["铃莓(夏日)", "スズメ(サマー)", "Suzume(Summer)", "水女仆", "水妹抖"],
    1078: ["凯留(夏日)", "キャル(サマー)", "Kyaru(Summer)", "水黑", "水黑猫", "水臭鼬", "泳装黑猫", "泳装臭鼬", "潶", "溴", "💧黑"],
    1079: ["珠希(夏日)", "タマキ(サマー)", "Tamaki(Summer)", "水猫剑", "渵", "💧🐱🗡️", "水🐱🗡️"],
    1080: ["美冬(夏日)", "ミフユ(サマー)", "Mifuyu(Summer)", "水子龙", "水美冬"],
    1081: ["忍(万圣节)", "シノブ(ハロウィン)", "Shinobu(Halloween)", "万圣忍", "瓜忍", "🎃忍", "🎃💀"],
    1082: ["宫子(万圣节)", "ミヤコ(ハロウィン)", "Miyako(Halloween)", "万圣宫子", "万圣布丁", "狼丁", "狼布丁", "万圣🍮", "🐺🍮", "🎃🍮", "👻🍮"],
    1083: ["美咲(万圣节)", "ミサキ(ハロウィン)", "Misaki(Halloween)", "万圣美咲", "万圣大眼", "瓜眼", "🎃眼", "🎃👀", "🎃👁️", "🎃👁"],
    1084: ["千歌(圣诞节)", "チカ(クリスマス)", "Chika(Xmas)", "圣诞千歌", "圣千", "蛋鸽", "🎄💰🎶", "🎄千🎶", "🎄1000🎶"],
    1085: ["胡桃(圣诞节)", "クルミ(クリスマス)", "Kurumi(Xmas)", "圣诞胡桃", "圣诞铃铛"],
    1086: ["绫音(圣诞节)", "アヤネ(クリスマス)", "Ayane(Xmas)", "圣诞熊锤", "蛋锤", "圣锤", "🎄🐻🔨", "🎄🐻"],
    1087: ["日和(新年)", "ヒヨリ(ニューイヤー)", "Hiyori(NewYear)", "新年日和", "春猫", "👘🐱"],
    1088: ["优衣(新年)", "ユイ(ニューイヤー)", "Yui(NewYear)", "新年优衣", "春田", "新年由衣"],
    1089: ["怜(新年)", "レイ(ニューイヤー)", "Rei(NewYear)", "春剑", "春怜", "春伶", "新春剑圣", "新年怜", "新年剑圣"],
    1090: ["惠理子(情人节)", "エリコ(バレンタイン)", "Eriko(Valentine)", "情人节病娇", "恋病", "情病", "恋病娇", "情病娇"],
    1091: ["静流(情人节)", "シズル(バレンタイン)", "Shizuru(Valentine)", "情人节静流", "情姐", "情人节姐姐"],
    1092: ["安", "アン", "An", "胖安", "55kg"],
    1093: ["露", "ルゥ", "Ruu", "逃课女王"],
    1094: ["古蕾娅", "グレア", "Gurea", "龙姬", "古雷娅", "古蕾亚", "古雷亚", "🐲🐔", "🐉🐔"],
    1095: ["空花(大江户)", "クウカ(オーエド)", "Kuuka(Ooedo)", "江户空花", "江户抖m", "江m", "花m", "江花"],
    1096: ["妮诺(大江户)", "ニノン(オーエド)", "Ninon(Ooedo)", "江户扇子", "忍扇"],
    1097: ["雷姆", "レム", "Remu", "蕾姆"],
    1098: ["拉姆", "ラム", "Ramu"],
    1099: ["爱蜜莉雅", "エミリア", "Emiria", "艾米莉亚", "emt"],
    1100: ["铃奈(夏日)", "スズナ(サマー)", "Suzuna(Summer)", "瀑击弓", "水爆", "水爆弓", "水暴", "瀑", "水暴弓", "瀑弓", "泳装暴弓", "泳装爆弓"],
    1101: ["伊绪(夏日)", "イオ(サマー)", "Io(Summer)", "水魅魔", "水老师", "泳装魅魔", "泳装老师"],
    1102: ["美咲(夏日)", "ミサキ(サマー)", "Misaki(Summer)", "水大眼", "泳装大眼"],
    1103: ["咲恋(夏日)", "サレン(サマー)", "Saren(Summer)", "水电", "泳装充电宝", "泳装咲恋", "水着咲恋", "水电站", "水电宝", "水充", "👙🔋"],
    1104: ["真琴(夏日)", "マコト(サマー)", "Makoto(Summer)", "水狼", "浪", "水🐺", "泳狼", "泳月", "泳月月", "泳朋", "水月", "水月月", "水朋", "👙🐺"],
    1105: ["香织(夏日)", "カオリ(サマー)", "Kaori(Summer)", "水狗", "泃", "水🐶", "水🐕", "泳狗"],
    1106: ["真步(夏日)", "マホ(サマー)", "Maho(Summer)", "水狐狸", "水狐", "水壶", "水真步", "水maho", "氵🦊", "水🦊", "💧🦊"],
    1107: ["碧(插班生)", "アオイ(編入生)", "Aoi(Hennyuusei)", "生菜", "插班碧"],
    1108: ["克萝依", "クロエ", "Kuroe", "华哥", "黑江", "黑江花子", "花子"],
    1109: ["琪爱儿", "チエル", "Chieru", "切露", "茄露", "茄噜", "切噜"],
    1110: ["优妮", "ユニ", "Yuni", "真行寺由仁", "由仁", "u2", "优妮辈先", "辈先", "书记", "uni", "先辈", "仙贝", "油腻", "优妮先辈", "学姐", "18岁黑丝学姐"],
    1111: ["镜华(万圣节)", "キョウカ(ハロウィン)", "Kyouka(Halloween)", "万圣镜华", "万圣小仓唯", "万圣xcw", "猫仓唯", "黑猫仓唯", "mcw", "猫唯", "猫仓", "喵唯"],
    1112: ["禊(万圣节)", "ミソギ(ハロウィン)", "Misogi(Halloween)", "万圣禊", "万圣炸弹人", "瓜炸弹人", "万圣炸弹", "万圣炸", "瓜炸", "南瓜炸", "🎃💣"],
    1113: ["美美(万圣节)", "ミミ(ハロウィン)", "Mimi(Halloween)", "万圣兔", "万圣兔子", "万圣兔兔", "绷带兔", "绷带兔子", "万圣美美", "绷带美美", "万圣🐰", "绷带🐰", "🎃🐰", "万圣🐇", "绷带🐇", "🎃🐇"],
    1114: ["露娜", "ルナ", "Runa", "露仓唯", "露cw"],
    1115: ["克莉丝提娜(圣诞节)", "クリスティーナ(クリスマス)", "Kurisutiina(Xmas)", "Christina(Xmas)", "Cristina(Xmas)", "圣诞克", "圣诞克总", "圣诞女帝", "蛋克", "圣克", "必胜客"],
    1116: ["望(圣诞节)", "ノゾミ(クリスマス)", "Nozomi(Xmas)", "圣诞望", "圣诞偶像", "蛋偶像", "蛋望"],
    1117: ["伊莉亚(圣诞节)", "イリヤ(クリスマス)", "Iriya(Xmas)", "圣诞伊莉亚", "圣诞伊利亚", "圣诞伊莉雅", "圣诞伊利雅", "圣诞yly", "圣诞吸血鬼", "圣伊", "圣yly"],
    1118: ["贪吃佩可(新年)", "ペコリーヌ(ニューイヤー)", "Pekoriinu(NewYear)", "春佩可", "春吃", "春吃货","新春吃货","新春佩可"],
    1119: ["可可萝(新年)", "コッコロ(ニューイヤー)", "Kokkoro(NewYear)", "春可可", "春白", "新年妈", "春妈"],
    1120: ["凯留(新年)", "キャル(ニューイヤー)", "Kyaru(NewYear)", "春凯留", "春黑猫", "春黑", "春臭鼬", "新年凯留", "新年黑猫", "新年臭鼬", "唯一神"],
    1121: ["铃莓(新年)", "スズメ(ニューイヤー)", "Suzume(NewYear)", "春铃莓", "春女仆", "春妹抖", "新年铃莓", "新年女仆", "新年妹抖"],
    1122: ["霞(魔法少女)", "カスミ(マジカル)", "Kasumi(MagiGirl)", "魔法少女霞", "魔法侦探", "魔法杜宾犬", "魔法驴", "魔法驴子", "魔驴", "魔法霞", "魔法少驴"],
    1123: ["栞(魔法少女)", "シオリ(マジカル)", "Shiori(MagiGirl)", "魔法少女栞", "魔法tp弓", "魔法小栞", "魔法白虎弓", "魔法白虎妹", "魔法白虎", "魔栞"],
    1124: ["卯月(偶像大师)", "ウヅキ(デレマス)", "Udsuki(DEREM@S)", "卯月", "卵用", "Udsuki(DEREMAS)", "岛村卯月"],
    1125: ["凛(偶像大师)", "リン(デレマス)", "Rin(DEREM@S)", "凛", "Rin(DEREMAS)", "涩谷凛", "西部凛"],
    1126: ["未央(偶像大师)", "ミオ(デレマス)", "Mio(DEREM@S)", "未央", "Mio(DEREMAS)", "本田未央","Mio"],
    1127: ["铃(游侠)", "リン(レンジャー)", "Rin(Ranger)", "骑兵松鼠", "游侠松鼠", "游骑兵松鼠", "护林员松鼠", "护林松鼠", "游侠🐿️", "武松"],
    1128: ["真阳(游侠)", "マヒル(レンジャー)", "Mahiru(Ranger)", "骑兵奶牛", "游侠奶牛", "游骑兵奶牛", "护林员奶牛", "护林奶牛", "游侠🐄", "游侠🐮", "牛叉"],
    1129: ["璃乃(奇境)", "リノ(ワンダー)", "Rino(Wonder)", "璃乃(仙境)", "爽弓", "爱丽丝弓", "爱弓", "兔弓", "奇境妹弓", "仙境妹弓", "白丝妹弓"],
    1130: ["步未(奇境)", "アユミ(ワンダー)", "Ayumi(Wonder)", "步未(仙境)", "路人兔", "兔人妹", "爱丽丝路人", "奇境路人", "仙境路人"],
    1131: ["流夏(夏日)", "ルカ(サマー)", "Ruka(Summer)", "泳装流夏", "水流夏", "泳装刘夏", "水刘夏", "泳装大姐", "泳装大姐头", "水大姐", "水大姐头", "水儿力", "泳装儿力", "水流", "亚索"],
    1132: ["杏奈(夏日)", "アンナ(サマー)", "Anna(Summer)", "泳装中二", "泳装煤气罐", "水中二", "水煤气罐", "冲", "冲二"],
    1133: ["七七香(夏日)", "ナナカ(サマー)", "Nanaka(Summer)", "泳装娜娜卡", "泳装77k", "泳装77香", "水娜娜卡", "水77k", "水77香","水七七香","水七七","水77"],
    1134: ["初音(夏日)", "ハツネ(サマー)", "Hatsune(Summer)", "水星", "海星", "水hego", "水星法", "泳装星法", "水⭐法", "水睡法", "湦"],
    1135: ["美里(夏日)", "ミサト(サマー)", "Misato(Summer)", "水母", "泳装圣母", "水圣母"],
    1136: ["纯(夏日)", "ジュン(サマー)", "Jun(Summer)", "泳装黑骑", "水黑骑", "泳装纯", "水纯", "小次郎"],
    1137: ["茜里(天使)", "アカリ(エンジェル)", "Akari(Angel)", "天使妹法"],
    1138: ["依里(天使)", "ヨリ(エンジェル)", "Yori(Angel)", "天使姐法","天姐"],
    1139: ["纺希(万圣节)", "ツムギ(ハロウィン)", "Tsumugi(Halloween)", "万圣裁缝", "万圣蜘蛛侠", "🎃🕷️", "🎃🕸️", "万裁", "瓜裁", "鬼裁", "鬼才"],
    1140: ["怜(万圣节)", "レイ(ハロウィン)", "Rei(Halloween)", "幽怜", "鬼剑","万圣剑圣"],
    1141: ["茉莉(万圣节)", "マツリ(ハロウィン)", "Matsuri(Halloween)", "万圣跳跳虎", "万圣老虎", "瓜虎", "🎃🐅"],
    1142: ["莫妮卡(魔法少女)", "モニカ(マジカル)", "Monika(MagiGirl)", "魔法少女毛二力", "魔法提督", "魔二力"],
    1143: ["智(魔法少女)", "トモ(マジカル)", "Tomo(MagiGirl)", "魔法少女卜毛", "魔法少女智","阿库娅","弱智","马猴智","⑨"],
    1144: ["秋乃(圣诞节)", "アキノ(クリスマス)", "Akino(Xmas)","圣哈","圣诞秋乃","圣诞哈哈剑"],
    1145: ["咲恋(圣诞节)", "サレン(クリスマス)", "Saren(Xmas)","圣电","圣诞充电宝","圣诞咲恋"],
    1146: ["优花梨(圣诞节)", "ユカリ(クリスマス)", "Yukari(Xmas)","蛋黄","圣黄骑","圣诞黄骑"],
    1147: ["矛依未(新年)", "ムイミ(ニューイヤー)", "Muimi(NewYear)","春511","春矛","新春511"],
    1150: ["似似花(新年)", "ネネカ(ニューイヤー)", "Neneka(NewYear)","春花","新春nnk","新春似似花","春nnk"],
    1155: ["可可萝(礼服)", "コッコロ(儀装束)", "Kokkoro(dress)","仪妈","礼妈","礼服妈"],
    1156: ["优衣(礼服)", "ユイ(儀装束)", "Yui(dress)","仪田","礼田","礼服优衣","礼衣"],
    1157: ["霞(夏日)", "カスミ(サマー)", "Kasumi(Summer)","水驴","沪"],
    1158: ["莉玛(灰姑娘)", "リマ(シンデレラ)", "Rima(cinderella)","人驼","灰羊驼"],
    1159: ["真琴(灰姑娘)", "マコト(シンデレラ)", "Makoto(cinderella)","灰太狼","灰狼","人狼"],
    1160: ["真步(灰姑娘)", "マホ(シンデレラ)", "Maho(cinderella)","灰壶","茶壶","灰狐"],
    1162: ["克萝依(圣学祭)", "クロエ(聖学祭)", "Kuroe(聖学祭)","圣华哥","华祭"],
    1163: ["琪爱儿(圣学祭)", "チエル(聖学祭)", "Chieru(聖学祭)","圣切噜","圣噜"],
    1164: ["优妮(圣学祭)", "ユニ(聖学祭)", "Yuni(聖学祭)","圣优尼","圣油腻","圣u","圣优","圣uni","圣优妮"],
    1165: ["祈梨(时空旅行者)", "イノリ(タイムトラベル)", "Inori(TimeTravel)","86","军龙锤","爱上火车","火车"],
    1166: ["嘉夜(时空旅行者)", "カヤ(タイムトラベル)", "Kaya(TimeTravel)","军龙拳"],
    1167: ["碧(作业服)", "アオイ(作業服)", "Aoi(作業服)","韭菜","榨菜","工菜","贡菜"],
    1168: ["珠希(作业服)", "タマキ(作業服)", "Tamaki(作業服)","工猫"],
    1169: ["美冬(作业服)", "ミフユ(作業服)", "Mifuyu(作業服)","电子龙"],
    1170: ["惠理子(夏日)", "エリコ(サマー)", "Eriko(Summer)","水饺","水病娇","水病","水娇"],
    1171: ["静流(夏日)", "シズル(サマー)", "Shizuru(Summer)","水姐"],
    1172: ["望(夏日)", "ノゾミ(サマー)", "Nozomi(Summer)","水望","水偶像"],
    1173: ["千歌(夏日)", "チカ(サマー)", "Chika(Summer)","水千","水千歌"],
    1174: ["纺希(夏日)", "ツムギ(サマー)", "Tsumugi(Summer)","水裁缝","水裁"],
    1175: ["深月(大江户)", "ミツキ(オーエド)", "Mitsuki(Ooedo)","江s","花s","江户深月","江月","护士深月"],
    1176: ["雪(大江户)", "ユキ(オーエド)", "Yuki(Ooedo)","江雪","江镜","江户雪哥","江户镜子"],
    1177: ["香织(万圣节)", "カオリ(ハロウィン)", "Kaori(Halloween)","鬼狗","圣狗","万圣狗","瓜狗","尾刀狗"],
    1178: ["妮诺(万圣节)", "ニノン(ハロウィン)", "Ninon(Halloween)","鬼扇","万圣扇","万圣扇子","瓜扇"],
    1179: ["铃奈(万圣节)", "スズナ(ハロウィン)", "Suzuna(Halloween)","鬼暴","万圣暴","万圣暴击弓","瓜暴"],
    1180: ["克蕾琪塔", "クレジッタ", "Kurejitta", "大吉塔", "奸商", "大吉他", "富婆"],
    1181: ["兰法", "ランファ", "Rannfa", "兰法妈妈"],
    1182: ["美空", "ミソラ", "Misora", "坏女人"],
    1185: ["花凛", "カリン", "Karin", "绿毛恶魔", "绿色恶魔", "绿魔"],
    1186: ["涅比亚", "ネビア", "Nebia",  "飞机杯"],
    1190: ["伊绪(黑暗)", "イオ(ノワール)", "Io(Noir)", "暗黑老师", "暗老师", "黑魔"],
    1191: ["空花(黑暗)", "クウカ(ノワール)", "Kuuka(Noir)", "暗黑空花", "暗M", "黑花"],
    1192: ["真阳(圣诞节)", "マヒル(クリスマス)", "Mahiru(Xmas)", "圣诞奶牛", "🎄🐄", "🎄🐮"],
    1193: ["璃乃(圣诞节)", "リノ(クリスマス)", "Rino(Xmas)", "弹弓", "圣诞妹弓"],
    1199: ["宫子(圣诞节)", "ミヤコ(クリスマス)", "Miyako(Xmas)", "但丁", "雪布丁", "圣诞布丁", "雪布","🎄🍮"],
    1200: ["静流(黑暗)", "シズル(ノワール)", "Shizuru(Noir)", "暗姐姐", "黑姐", "黑姐姐"],
    1207: ["雪菲(新年)", "シェフィ(ニューイヤー)", "Shefi(NewYear)", "春雪菲","春菲","春节雪菲"],
    1208: ["流夏(新年)", "ルカ(ニューイヤー)", "Ruka(NewYear)", "春流夏", "新春流夏", "春亚索", "春大姐头"],
    1209: ["伊莉亚(新年)", "イリヤ(ニューイヤー)", "Iriya(NewYear)", "春伊利亚", "春伊"],
    1210: ["贪吃佩可(超载)", "ペコリーヌ(オーバーロード)", "Pekoriinu(OverLord)", "超市佩可","超吃"],
    1211: ["凯留(超载)", "凯留(オーバーロード)", "凯留(OverLord)", "超市凯露","超黑","超威蓝猫", "超猫", "蓝猫","超载凯露","超载黑猫"],
    1212: ["拉比林斯达(超载)", "ラビリスタ(オーバーロード)", "Rabirisuta(OverLord)", "超市晶","超晶"],
    1213: ["胡桃(舞台)", "クルミ(ステージ))", "Kurumi(Stage)", "舞台铃铛","舞台🔔","舞铃","50"],
    1214: ["美咲(舞台)", "ミサキ(ステージ))", "Misaki(Stage)", "舞台大眼","舞台👀","舞台👁️","舞眼","舞台👁","泥头车美咲","泥头车","车眼"],
    1215: ["步未(怪盗)", "アユミ(怪盗)", "Ayumi(Kaitou)", "怪盗路人妹"],
    1216: ["祈梨(怪盗)", "イノリ(怪盗)", "Inori(Kaitou)", "怪盗龙锤", "忍龙"],
    1219: ["杏奈(海盗)", "アンナ(パイレーツ)", "Anna(Pirate)", "海盗中二", "海二"],
    1220: ["忍(海盗)", "シノブ（パイレーツ）", "Shinobu(Pirate)", "海盗忍", "海忍"],
    1221: ["碧(露营)", "アオイ(キャンプ)", "Aoi(Camp)", "野菜"],
    1222: ["优花梨(露营)", "ユカリ（キャンプ）", "Yukari(Camp)", "蒂骑","路由","野骑","露营黄骑","野黄","野营黄骑"],
    1223: ["斑比", "ヴァンピィ", "Vania","班比"],
    1224: ["日和(夏日)", "ヒヨリ(サマー)", "Hiyori(Summer)","水猫","水猫拳","💧🐱", "水🐱"],
    1225: ["怜(夏日)", "レイ(サマー)", "Rei(Summer)","水剑","水怜"],
    1226: ["优衣(夏日)", "ユイ(サマー)", "Yui(Summer)","水ue","水田","泳装ue"],
    1227: ["镜华(夏日)", "キョウカ(サマー)", "Kyouka(Summer)","水cw","水仓唯","水xcw","泳装xcw","泳装镜华","scw","水镜华"],
    1228: ["禊(夏日)", "ミソギ(サマー)", "Misogi(Summer)","水炸","水炸弹人","泳装炸弹人"],
    1229: ["美美(夏日)", "ミミ(サマー)", "Mimi(Summer)","水兔","水兔子","水美美"],
    1230: ["爱梅斯", "アメス", "Amesu", "ams"],
    1231: ["真步(探险家)", "マホ(エクスプローラー)", "Maho(Explorer)", "矿壶", "矿狐", "探险家狐狸", "探险家真步"],
    1232: ["绫音(探险家)", "アヤネ(エクスプローラー)", "Ayane(Explorer)", "探险家熊锤", "探险熊锤"],
    1233: ["涅娅", "ネア", "Nea", "黄史莱姆","小黄"],
    1235: ["铃(万圣节)", "リン(ハロウィン)", "Rin(Halloween)", "万圣松鼠", "万圣铃"],
    1236: ["智(万圣节)", "トモ(ハロウィン)", "Tomo(Halloween)", "万圣智","瓜智"],
    1237: ["七七香(万圣节)", "ナナカ(ハロウィン)", "Nanaka(Halloween)", "万圣七七香"],
    1238: ["克莉丝提娜(狂野)", "クリスティーナ(ワイルド)", "Kurisutiina(Wild)", "兔克"],
    1239: ["茉莉(狂野)", "マツリ(ワイルド)", "Matsuri(Wild)", "狂野跳跳虎","地虎侠"],
    1240: ["茜里(圣诞节)", "アカリ(クリスマス)", "Akari(Xmas)", "圣诞妹法"],
    1241: ["依里(圣诞节)", "ヨリ(クリスマス)", "Yori(Xmas)", "圣诞姐法"],
    1242: ["纯(圣诞节)", "ジュン(クリスマス)", "Jun(Xmas)", "圣诞黑骑","白骑","圣诞纯"],
    1245: ["穗希(新年)", "ホマレ(ニューイヤー)", "Homare(NewYear)", "春龙","春龙妈"],
    1246: ["美里(新年)", "ミサト(ニューイヤー)", "Misato(NewYear)", "春母","新年圣母","春圣母"],
    1247: ["深月(新年)", "ミツキ(ニューイヤー)", "Mitsuki(NewYear)", "新年深月","春s","春月"],
    1248: ["望(解放者)", "ノゾミ(リベレイター)", "Nozomi(Liberator)", "解放望", "解望", "白望", "光望"],
    1249: ["嘉夜(解放者)", "カヤ(リベレイター)", "Kaya(Liberator)", "解放龙拳"],
    1250: ["矛依未(解放者)", "ムイミ(リベレイター)", "Muimi(Liberator)", "513", "解511", "解放511","51狗"],
    1251: ["珠希(咖啡)", "タマキ(カフェ)", "Tamaki(Cafe)", "猫咖", "咖啡猫"],
    1252: ["莫妮卡(咖啡)", "モニカ(カフェ)", "Monika(Cafe)", "猫二力"],
    1253: ["可可萝(游侠)", "コッコロ(レンジャー)", "Kokkoro(Ranger)", "游侠妈", "狗妈"],
    1254: ["栞(游侠)", "シオリ(レンジャー)", "Shiori(Ranger)", "游侠tp弓", "游侠栞"],
    1255: ["姬塔（术士）", "ジータ（ウォーロック)", "Jiita(Warlock)", "魔法吉他", "魔法姬塔","法姬"],
    1256: ["碧卡拉", "ビカラ", "Bikara",  "鼠鼠"],
    1256: ["花凛(炼金术师)", "カリン(アルケミスト)", "Karin(Alchemist)",  "炼金花凛"],
    1258: ["莉莉(堕天使)", "リリ（フォールン）", "Riri(Fallen)", "莉莉"],
    1260: ["可璃亚(堕天使)", "クリア（フォールン）", "Kuria(Fallen)", "盾妹", "可莉亚", "可利亚"],
    1261: ["普蕾西亚(堕天使)", "プレシア（フォールン）", "Pureshia(Fallen)", "猪妹","普蕾西亚"],
    1262: ["伊莉亚(礼服)", "イリヤ(儀装束)", "Iriya(dress)", "礼伊","仪莉亚"],
    1263: ["雪(礼服)", "ユキ(儀装束)", "Yuki(dress)", "礼雪","雪仪","仪雪"],
    1264: ["克洛琪", "クローチェ", "Kurocchie","机娘","克罗琦","克罗切"],
    1265: ["莱菈耶儿", "ライラエル", "Rairaeru","莱莱"],
    1266: ["似似花(夏日)", "ネネカ(サマー)", "Neneka(Summer)", "水花","㳸"],
    1267: ["秋乃(夏日)", "アキノ(サマー)", "Akino(Summer)", "水哈"],
    1268: ["优花梨(夏日)", "ユカリ(サマー)", "Yukari(Summer)", "水黄骑"],
    1269: ["兰法(夏日)", "ランファ(サマー)", "Rannfa(Summer)", "水兰法", "泳装兰法"],
    1270: ["空花(夏日)", "クウカ(サマー)", "Kuuka(Summer)", "水空花", "水M"],
    1271: ["忍(夏日)", "シノブ(サマー)", "Shinobu(Summer)", "水忍"],
    1272: ["凯留(插班生)", "キャル(編入生)", "Kyaru(Hennyuusei)", "生猫", "学院猫猫"],
    1273: ["铃奈(插班生)", "スズナ(編入生)", "Suzuna(Hennyuusei)", "生暴"],
    1275: ["咲恋(撒拉沙利亚)", "サレン(サラサリア)", "Saren(Sarasaria)", "沙电","火电"],
    1276: ["流夏(撒拉沙利亚)", "ルカ(サラサリア)", "Ruka(Sarasaria)", "沙流夏","冰流夏"],
    1277: ["琳德", "リンド", "Rinndo", "龙姐","绿龙"],
    1278: ["乌尔姆", "ブルム", "Burumu", "龙妹","红龙"],
    1279: ["贪吃佩可(圣诞节)", "ペコリーヌ(クリスマス)", "Pekoriinu(Xmas)", "圣诞佩可","圣吃","法可","圣诞吃货"],
    1280: ["克蕾琪塔(圣诞节)", "クレジッタ(クリスマス)", "Kurejitta(Xmas)", "圣诞富婆","圣富婆"],
    1283: ["祈梨(新年)", "イノリ(ニューイヤー)", "Inori(NewYear)", "春龙锤"],
    1284: ["初音(新年)", "ハツネ(ニューイヤー)", "Hatsune(NewYear)", "春星", "春星法"],
    1285: ["霞(新年)", "カスミ(ニューイヤー)", "Kasumi(NewYear)", "春驴"],
    1287: ["日和(星幽)", "ヒヨリ(アストラル)", "Hiyori(Astral)", "星猫", "星猫拳"],
    1288: ["怜(星幽)", "レイ(アストラル)", "Rei(Astral)", "星怜", "星剑", "星剑圣", "光剑"],
    1289: ["优衣(星幽)", "ユイ(アストラル)", "Yui(Astral)", "星ue", "星田", "光田"],
    1290: ["厄莉丝", "エリス", "Erisu", "黑ue", "els","黑优衣","厄里斯"],
    1293: ["优妮（冬日）", "ユニ(ウィンター)", "Yuni(Winter)", "水优妮", "水uni"],
    1294: ["克萝依（冬日）", "クロエ(ウィンター)", "Kuroe(Winter)", "水华", "水华哥"],
    1295: ["琪爱儿（冬日）", "チエル（ウィンター）", "Chieru(Winter)", "水切噜","水切"],
    1296: ["银莲", "アネモネ", "Anemone", "otto","草神","纳西妲"],
    1297: ["涅妃涅菈", "ネフィ＝ネラ", "NeFi=nera", "涅妃"],
    1298: ["真琴（教官）", "マコト(コマンダー)", "Makoto(Commander)", "教官狼","战狼"],
    1299: ["惠理子（教官）", "エリコ（コマンダー）", "Eriko(Commander)", "教官病娇","病教"],
    1300: ["倭", "ヤマト", "Yamato","大和"],
    1301: ["若菜", "ワカナ", "Wakana", "小厨娘","平底锅"],
    1302: ["布武机", "フブキ", "Hubuki", "雌小鬼","吹雪"],
    1307: ["镜华（春日）", "キョウカ（スブリング）", "Kyouka（Spring）", "花cw","hcw","华为","花仓唯","春仓唯","春cw"],
    1308: ["铃莓（春日）", "スズメ（スブリング）", "Suzume（Spring）", "春日女仆","花铃莓","花女仆"],
    1309: ["库露露", "クルル", "Kururu", "宝石兔"],
    1310: ["真步（梦想乐园）", "マホ（ドリームパーク）", "Maho（DreamPark）", "兔壶","烧壶"],
    1311: ["涅娅（夏日）", "ネア（サマー）", "Nea（Summer）", "水史莱姆","水小黄"],
    1312: ["美空（夏日）", "ミソラ（サマー）", "Misora（Summer）", "水美空"],
    1316: ["莉莉（夏日）", "リリ（サマー）", "Riri（Summer）", "水莉莉"],
    1317: ["爱梅斯（夏日）", "アメス（サマー）", "Amesu（Summer）", "水ams","水爱梅斯"],
    1318: ["穗希（夏日）", "ホマレ（サマー）", "Homare（Summer）", "水龙妈"],
    1319: ["爱蜜莉雅（夏日）", "エミリア（サマー）", "Emiria（Summer）", "水艾米莉亚", "水emt"],
    1320: ["艾姬多娜（夏日）", "エキドナ（サマー）", "Ekidona（Summer）", "水魔女"],
    1321: ["蕾姆（夏日）", "レム（サマー）", "Remu（Summer）", "水蕾姆"],
    1322: ["望（炼金术师）", "ノゾミ（アルケミスト）", "Nozomi（Alchemist）", "炼金望"],
    1328: ["莱菈耶儿（圣诞节）", "ライラエル（クリスマス）", "Rairaeru（Xmas）", "圣莱","圣莱莱"],
    1329: ["伊绪（圣诞节）", "イオ（クリスマス）", "Io（Xmas）", "圣老师"],
    1330: ["格蕾斯", "グレイス", "Gureisu", "格蕾丝"],
    1332: ["莫妮卡（新年）", "モニカ（ニューイヤー）", "Monika（NewYear）", "春二力"],
    1335: ["咲恋（新年）", "サレン（ニューイヤー）", "Saren（NewYear）", "春电"],
    1336: ["美杜莎", "メドゥーサ", "Medusa", "小美"],
    1337: ["菈比莉斯塔（始原）", "ラビリスタ（アルファ）", "Rabirisuta（Alpha）", "水晶"],
    1338: ["似似花（始原）", "ネネカ（アルファ）", "Neneka（Alpha）", "αNNK", "α花", "阿尔法花"],
    1339: ["克莉丝提娜（始原）", "クリスティーナ（アルファ）", "Kurisutiina（Alpha）", "α克", "阿尔法克"],
    1340: ["菲欧", "フィオ", "Fio"],
    1343: ["兰法（礼服）", "ランファ（儀装束）", "Rannfa（Dress）", "礼兰法"],
    1344: ["千歌（礼服）", "チカ（儀装束）", "Chika（Dress）", "礼千", "礼千歌"],


    # =================================== #
    1701: ["环奈", "かんな", "Kanna","桥本环奈", "红二力", "毛大力", "毛小力", "毛六力", "可大萝", "大可萝", "缝合怪"],
    1702: ["环奈(新年)", "かんな(ニューイヤー)", "Kanna(NewYear)","春环"],
    1801: ["日和(公主)", "ヒヨリ(プリンセス)", "Hiyori(Princess)", "公主猫拳", "创燃高达", "公猫", "公主猫", "火猫"],
    1802: ["优衣(公主)", "ユイ(プリンセス)", "Yui(Princess)", "公主优衣", "公主yui", "公主种田", "公主田", "公主ue", "掉毛优衣", "掉毛yui", "掉毛ue", "掉毛", "飞翼优衣", "飞翼ue", "飞翼", "飞翼高达", "毛衣", "羽衣", "吊毛","飞田"],
    1803: ["怜(公主)", "レイ(プリンセス)", "Rei(Princess)", "公主怜", "公主剑圣", "公剑", "公怜","风剑"],

    1804: ["贪吃佩可(公主)", "ペコリーヌ(プリンセス)", "Pekoriinu(Princess)", "公主吃", "公主饭", "公主吃货", "公主佩可", "公主饭团", "公主🍙", "命运高达", "高达", "命运公主", "高达公主", "命吃", "春哥高达", "🤖🍙", "🤖"],
    1805: ["可可萝(公主)", "コッコロ（プリンセス）", "Kokkoro(Princess)", "公主妈", "月光妈", "蝶妈", "蝴蝶妈", "月光蝶妈", "公主可", "公主可萝", "公主可可萝", "月光可", "月光可萝", "月光可可萝", "蝶可", "蝶可萝", "蝶可可萝"],
    1806: ["凯留(公主)", "キャル（プリンセス）", "Kyaru(Princess)", "公主黑猫", "公黑", "白猫"],
    1807: ["初音&栞", "ハツネ&シオリ", "Hatsune&Shiori", "星弓", "星栞","初音栞"],
    1808: ["禊&美美&镜华", "ミソギ&ミミ&キョウカ", "Misogi&Mimi&Kyouka", "27岁", "小小甜心", "狱三家"],
    1809: ["秋乃&咲恋", "アキノ&サレン", "Akino&Saren", "笑哈哈", "咲哈哈", "哈电", "哈哈大笑"],
    1810: ["安&古蕾娅", "アン&グレア", "An&Gurea", "姬佬","双姬"],
    1811: ["静流&璃乃", "シズル&リノ", "Shizuru&Rino", "姐妹","姐妹丼","流璃","琉璃"],
    1812: ["雪菲(公主)", "シェフィ（プリンセス）", "Shefi(Princess)", "公主雪菲", "白菲"],


    # =================================== #

    #1908: ["花凛", "カリン", "Karin", "绿毛恶魔"],#

 
    4031: ["骷髅", "髑髏", "Dokuro", "骷髅老爹", "老爹"],
 
    9000: ["祐树", "ユウキ", "Yuuki", "骑士", "骑士君"],
    #9401: ["爱梅斯", "アメス", "Amesu", "菲欧", "フィオ", "Fio"],
    
    # =================================== #
    #ウマ娘 プリティーダービー#
   11100: ["特别周","小特","Special-Week","スペシャルウィーク"],
   11101: ["无声铃鹿","铃鹿","Silence-Suzuka","サイレンススズカ"],
   11102: ["东海帝王","东海帝皇","Tokai-Teio","トウカイテイオー","帝宝"],
   11103: ["丸善斯基","丸善滑雪","Maru Zensky","マルゼンスキー" ],
   11104: ["富士奇石","富士奇迹","Fuji Kiseki","フジキセキ" ],
   11105: ["小栗帽","小栗栗","オグリ","Oguri-Cap","オグリキャップ" ],
   11106: ["黄金船","皮皮船","皮划艇","Gold-Ship","ゴールドシップ" ],
   11107: ["伏特加","Vodka","ウオッカ" ],
   11108: ["大和赤骥","大和緋紅","Daiwa-Scarlet","ダイワスカーレット" ],
   11109: ["大树快车","タイキ","Taiki-Shuttle","タイキシャトル" ],
   11110: ["草上飞","小草","草原奇迹","Grass Wonder","グラスワンダー" ],
   11111: ["菱亚马逊","亚马逊","Hishi-Amazon","ヒシアマゾン" ],
   11112: ["目白麦昆","麦昆","目白魔","Mejiro-McQueen","メジロマックイーン" ],
   11113: ["神鹰","怪鸟","エル","El-Condor-Pasa","エルコンドルパサー"],
   11114: ["好歌剧","TM-Opera-O","テイエムオペラオー" ],
   11115: ["成田白仁","Narita Brian","ナリタブライアン" ],
   11116: ["皇帝","鲁铎象征","鲁道夫象征","Symboli Rudolf","シンボリルドルフ" ],
   11117: ["气槽","Air-Groove","エアグルーヴ" ],
   11118: ["爱丽数码","Agnes-Digital" ],
   11119: ["玉藻十字","白色闪电","Tamamo-Cross","タマモクロス" ],
   11120: ["星云天空","Seiun-Sky","セイウンスカイ" ],
   11121: ["美妙姿势","Fine-Motion" ],
   11122: ["琵琶晨光","Biwa-Hayahide" ],
   11123: ["重炮","Mayano-Top-Gun" ],
   11124: ["曼城茶座","Manhattan-Cafe" ],
   11125: ["美浦波旁","Mihono-Bourbon" ],
   11126: ["目白赖恩","Mejiro-Ryan" ],
   11127: ["菱曙","Hishi-Akebono" ],
   11128: ["雪之美人","Yukino-Bijin" ],
   11129: ["米浴","关东的刺客","黑の刺客","Rice-Shower","ライスシャワー" ],
   11130: ["艾尼斯风神","Ines-Fujin" ],
   11131: ["爱丽速子","美龄快子","Agnes-Tachyon","アグネスタキオン" ],
   11132: ["爱慕织姬","Admire-Vega" ],
   11133: ["稻荷一","Inari-One" ],
   11134: ["胜利奖券","Winning-Ticket" ],
   11135: ["空中神宫","Air-Shakur" ],
   11136: ["荣进闪耀","Eishin-Flash" ],
   11137: ["真机伶","Curren-Chan" ],
   11138: ["川上公主","Kawakami-Princess" ],
   11139: ["黄金城市","Gold-City" ],
   11140: ["樱花进王","Sakura-Bakushin-O" ],
   11141: ["采珠","Seeking-the-Pearl" ],
   11142: ["新光风","Shinko-Windy" ],
   11143: ["东商变革","Sweep-Tosho" ],
   11144: ["超级小海湾","超級小渠","超级小湾","Super-Creek","スーパークリーク" ],
   11145: ["醒目飞鹰","Smart-Falcon" ],
   11146: ["荒漠英雄","Zenno-Rob-Roy" ],
   11147: ["东瀛佐敦","Tosen-Jordan" ],
   11148: ["中山庆典","Nakayama-Festa" ],
   11149: ["成田大进","Narita-Taishin" ],
   11150: ["西野花","Nishino-Flower" ],
   11151: ["春丽","乌拉拉","Haru-Urara","ハルウララ" ],
   11152: ["青竹回忆","Bamboo-Memory" ],
   11153: ["微光飞驹","Biko-Pegasus" ],
   11154: ["美丽周日","Marvelous Sunday" ],
   11155: ["待兼福来","Matikane-Fukukitaru" ],
   11156: ["Mr.C.B", ],
   11157: ["名将怒涛","名将户仁","Meisho-Doto","メイショウドトウ" ],
   11158: ["目白多伯","Mejiro-Dober" ],
   11159: ["优秀素质","Nice-Nature" ],
   11160: ["帝皇光辉","King-Halo" ],
   11161: ["Matikanetannhauser" ],
   11162: ["狄杜斯","Ikuno-Dictus" ],
   11163: ["目白善信","Mejiro-Palmer" ],
   11164: ["大拓太阳神","Daitaku-Helios" ],
   11165: ["双涡轮","Twin-Turbo" ],
   11166: ["MejiroArdan","メジロアルダン" ],
   11167: ["SakuraChiyonoO","サクラチヨノオー" ],
   11168: ["シリウスシンボリ" ],
   11169: ["ヤエノムエテキ" ],
   11170: ["ハッピーミーク" ],
   11171: ["駿川たづな" ],
   11172: ["理事长","秋川やよい" ],
   11173: ["乙名氏悦子"],
   11174: ["桐生院葵"],

}
