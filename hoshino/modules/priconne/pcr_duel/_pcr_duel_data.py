'''公主连接Re:dive的游戏数据'''


'''角色名称

遵照格式： id: [台服官译简体, 日文原名, 英文名(罗马音), B服官译, 常见别称, 带错别字的别称等] （<-依此顺序）
若暂无台服官译则用日文原名占位，台日用全角括号，英文用半角括号
'''
CHARA_NAME = {
    1000: ["未知角色", "未知キャラ", "Unknown"],
    1001: ["日和", "ヒヨリ", "Hiyori", "日和莉", "猫拳", "🐱👊"],
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
    1060: ["凯留", "キャル", "Kyaru", "凯露", "百地希留耶", "希留耶", "Kiruya", "黑猫", "臭鼬", "普黑", "接头霸王", "街头霸王"],
    1061: ["矛依未", "ムイミ", "Muimi", "诺维姆", "Noemu", "夏娜", "511", "无意义", "天楼霸断剑"],

    1063: ["亚里莎", "アリサ", "Arisa", "鸭梨瞎", "瞎子", "亚里沙", "鸭梨傻", "亚丽莎", "亚莉莎", "瞎子弓", "🍐🦐", "yls"],
    1064: ["雪菲","シェフィ","Shefi"],
    1065: ["嘉夜", "カヤ", "Kaya", "憨憨龙", "龙拳", "🐲👊🏻", "🐉👊🏻", "接龙笨比"],
    1066: ["祈梨", "イノリ", "Inori", "梨老八", "李老八", "龙锤"],
    1067: ["穗希", "ホマレ", "Homare"],
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
    1079: ["珠希(夏日)", "タマキ(サマー)", "Tamaki(Summer)", "水猫剑", "水猫", "渵", "💧🐱🗡️", "水🐱🗡️"],
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
    1126: ["未央(偶像大师)", "ミオ(デレマス)", "Mio(DEREM@S)", "未央", "Mio(DEREMAS)", "本田未央"],
    1127: ["铃(游侠)", "リン(レンジャー)", "Rin(Ranger)", "骑兵松鼠", "游侠松鼠", "游骑兵松鼠", "护林员松鼠", "护林松鼠", "游侠🐿️", "武松"],
    1128: ["真阳(游侠)", "マヒル(レンジャー)", "Mahiru(Ranger)", "骑兵奶牛", "游侠奶牛", "游骑兵奶牛", "护林员奶牛", "护林奶牛", "游侠🐄", "游侠🐮", "牛叉"],
    1129: ["璃乃(奇境)", "リノ(ワンダー)", "Rino(Wonder)", "璃乃(仙境)", "爽弓", "爱丽丝弓", "爱弓", "兔弓", "奇境妹弓", "仙境妹弓", "白丝妹弓"],
    1130: ["步未(奇境)", "アユミ(ワンダー)", "Ayumi(Wonder)", "步未(仙境)", "路人兔", "兔人妹", "爱丽丝路人", "奇境路人", "仙境路人"],
    1131: ["流夏(夏日)", "ルカ(サマー)", "Ruka(Summer)", "泳装流夏", "水流夏", "泳装刘夏", "水刘夏", "泳装大姐", "泳装大姐头", "水大姐", "水大姐头", "水儿力", "泳装儿力", "水流"],
    1132: ["杏奈(夏日)", "アンナ(サマー)", "Anna(Summer)", "泳装中二", "泳装煤气罐", "水中二", "水煤气罐", "冲", "冲二"],
    1133: ["七七香(夏日)", "ナナカ(サマー)", "Nanaka(Summer)", "泳装娜娜卡", "泳装77k", "泳装77香", "水娜娜卡", "水77k", "水77香"],
    1134: ["初音(夏日)", "ハツネ(サマー)", "Hatsune(Summer)", "水星", "海星", "水hego", "水星法", "泳装星法", "水⭐法", "水睡法", "湦"],
    1135: ["美里(夏日)", "ミサト(サマー)", "Misato(Summer)", "水母", "泳装圣母", "水圣母"],
    1136: ["纯(夏日)", "ジュン(サマー)", "Jun(Summer)", "泳装黑骑", "水黑骑", "泳装纯", "水纯", "小次郎"],
    1137: ["茜里(天使)", "アカリ(エンジェル)", "Akari(Angel)", "天使妹法"],
    1138: ["依里(天使)", "ヨリ(エンジェル)", "Yori(Angel)", "天使姐法"],
    1139: ["纺希(万圣节)", "ツムギ(ハロウィン)", "Tsumugi(Halloween)", "万圣裁缝", "万圣蜘蛛侠", "🎃🕷️", "🎃🕸️", "万裁", "瓜裁", "鬼裁", "鬼才"],
    1140: ["怜(万圣节)", "レイ(ハロウィン)", "Rei(Halloween)", "幽怜", "鬼剑","万圣剑圣"],
    1141: ["茉莉(万圣节)", "マツリ(ハロウィン)", "Matsuri(Halloween)", "万圣跳跳虎", "万圣老虎", "瓜虎", "🎃🐅"],
    1142: ["莫妮卡(魔法少女)", "モニカ(マジカル)", "Monika(MagiGirl)", "魔法少女毛二力", "魔法提督"],
    1143: ["智(魔法少女)", "トモ(マジカル)", "Tomo(MagiGirl)", "魔法少女卜毛", "魔法少女智","阿库娅","弱智","马猴智","⑨"],
    1144: ["秋乃(圣诞节)", "アキノ(クリスマス)", "Akino(Xmas)","圣哈","圣诞秋乃","圣诞哈哈剑"],
    1145: ["咲恋(圣诞节)", "サレン(クリスマス)", "Saren(Xmas)","圣电","圣诞充电宝","圣诞咲恋"],
    1146: ["优花梨(圣诞节)", "ユカリ(クリスマス)", "Yukari(Xmas)","蛋黄","圣黄骑","圣诞黄骑"],
    1147: ["矛依未(新年)", "ムイミ(ニューイヤー)", "Muimi(NewYear)","春511","春矛","新春511"],
    1150: ["似似花(新年)", "ネネカ(ニューイヤー)", "Neneka(NewYear)","春花","新春nnk","新春似似花","春nnk"],
    1155: ["可可萝(儀装束)", "コッコロ(儀装束)", "Kokkoro(dress)","仪妈","礼妈","礼服妈"],
    1156: ["优衣(儀装束)", "ユイ(儀装束)", "Yui(dress)","仪田","礼田","礼服优衣","礼衣"],
    1157: ["霞(夏日)", "カスミ(サマー)", "Kasumi(Summer)","水驴","沪"],
    1158: ["莉玛(灰姑娘)", "リマ(シンデレラ)", "Rima(cinderella)","人驼","沪"],
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
    1185: ["花凛", "カリン", "Karin", "绿毛恶魔", "绿色恶魔", "绿魔"],
    1190: ["伊绪(黑暗)", "イオ(ノワール)", "Io(Noir)", "暗黑老师", "暗老师", "黑魔"],
    1191: ["空花(黑暗)", "クウカ(ノワール)", "Kuuka(Noir)", "暗黑空花", "暗M", "黑花"],
    1192: ["真阳(圣诞节)", "マヒル(クリスマス)", "Mahiru(Xmas)", "圣诞奶牛", "🎄🐄", "🎄🐮"],
    1193: ["璃乃(圣诞节)", "リノ(クリスマス)", "Rino(Xmas)", "弹弓", "圣诞妹弓"],
    1199: ["宫子(圣诞节)", "ミヤコ(クリスマス)", "Miyako(Xmas)", "但丁", "雪布丁", "圣诞布丁", "雪布","🎄🍮"],
    1207: ["雪菲(新年)", "シェフィ(ニューイヤー)", "Shefi(NewYear)", "春雪菲","春菲","春节雪菲"],
    1208: ["流夏(新年)", "ルカ(ニューイヤー)", "Ruka(NewYear)", "春流夏", "新春流夏", "春亚索", "春大姐头"],
    1209: ["伊莉亚(新年)", "イリヤ(ニューイヤー)", "Iriya(NewYear)", "春伊利亚", "春伊"],
    1210: ["贪吃佩可(超载)", "ペコリーヌ(オーバーロード)", "Pekoriinu(OverLord)", "超市佩可","超吃"],
    1211: ["凯留(超载)", "凯留(オーバーロード)", "凯留(OverLord)", "超市凯露","超黑","超威蓝猫"],
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
    1230: ["爱梅斯", "アメス", "Amesu", "菲欧", "フィオ", "Fio", "ams"],
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
    1248: ["望(解放者)", "ノゾミ(リベレイター)", "Nozomi(Liberator)", "解放望"],
    1249: ["嘉夜(解放者)", "カヤ(リベレイター)", "Kaya(NewYear)", "解放龙拳"],
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
    1295: ["琪爱儿（冬日）", "チエル（ウィンター）", "Chieru(Winter)", "水切噜"],
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
    1337: ["菈比莉斯塔（阿尔法）", "ラビリスタ（アルファ）", "Rabirisuta（Alpha）", "水晶"],



    # =================================== #
    1701: ["环奈", "かんな", "Kanna","桥本环奈", "红二力", "毛大力", "毛小力", "毛六力", "可大萝", "大可萝", "缝合怪"],
    1702: ["环奈(新年)", "かんな(ニューイヤー)", "Kanna(NewYear)","春环"],
    1801: ["日和(公主)", "ヒヨリ(プリンセス)", "Hiyori(Princess)", "公主猫拳", "创燃高达", "公猫", "公主猫", "火猫"],
    1802: ["优衣(公主)", "ユイ(プリンセス)", "Yui(Princess)", "公主优衣", "公主yui", "公主种田", "公主田", "公主ue", "掉毛优衣", "掉毛yui", "掉毛ue", "掉毛", "飞翼优衣", "飞翼ue", "飞翼", "飞翼高达"],

    1804: ["贪吃佩可(公主)", "ペコリーヌ(プリンセス)", "Pekoriinu(Princess)", "公主吃", "公主饭", "公主吃货", "公主佩可", "公主饭团", "公主🍙", "命运高达", "高达", "命运公主", "高达公主", "命吃", "春哥高达", "🤖🍙", "🤖"],
    1805: ["可可萝(公主)", "コッコロ（プリンセス）", "Kokkoro(Princess)", "公主妈", "月光妈", "蝶妈", "蝴蝶妈", "月光蝶妈", "公主可", "公主可萝", "公主可可萝", "月光可", "月光可萝", "月光可可萝", "蝶可", "蝶可萝", "蝶可可萝"],
    1806: ["凯留(公主)", "キャル（プリンセス）", "yaru(Princess)", "公主黑猫", "公黑", "白猫"],
    1807: ["初音&栞", "ハツネ&シオリ", "Hatsune&Shiori", "星弓", "星栞","初音栞"],
    1808: ["禊&美美&镜华", "ミソギ&ミミ&キョウカ", "Misogi&Mimi&Kyouka", "27岁", "小小甜心", "狱三家"],
    1809: ["秋乃&咲恋", "アキノ&サレン", "Akino&Saren", "笑哈哈", "咲哈哈", "哈电", "哈哈大笑"],
    1810: ["安&古蕾娅", "アン&グレア", "An&Gurea", "姬佬","双姬"],
    1811: ["静流&璃乃", "シズル&リノ", "Shizuru&Rino", "姐妹","姐妹丼","流璃","琉璃"],
    1812: ["雪菲(公主)", "シェフィ（プリンセス）", "Shefi(Princess)", "公主雪菲", "白菲"],


    # =================================== #

    1908: ["花凛", "カリン", "Karin", "绿毛恶魔"],

 
    4031: ["骷髅", "髑髏", "Dokuro", "骷髅老爹", "老爹"],
 
    9000: ["祐树", "ユウキ", "Yuuki", "骑士", "骑士君"],
    9401: ["爱梅斯", "アメス", "Amesu", "菲欧", "フィオ", "Fio"],


    # =================================== # #FGO#
    8001: ['玛修·基列莱特','玛修','色茄子','学妹','马修'],
    8002: ['阿尔托莉雅·潘德拉贡','阿尔托利亚','呆毛','saber','棉被','吾王'],
    8003: ['阿尔托莉雅·潘德拉贡(Alter)','黑呆','黑无毛','黑SABER'],
    8004: ['阿尔托莉雅·潘德拉贡〔Lily〕','莉莉','白SABER','saberlily'],
    8005: ['尼禄·克劳狄乌斯','唔呣','罗马之花','红SABER','尼禄'],
    8008: ['阿蒂拉','大王','B提拉','彩笔','阿提拉'],
    8010: ['骑士迪昂','百合剑','迪昂'],
    8014: ['阿塔兰忒','猫茶','阿塔','塔喵'],
    8015: ['尤瑞艾莉','二姐'],
    8018: ['伊丽莎白·巴托里','龙娘'],
    8023: ['美杜莎','R姐'],
    8026: ['布狄卡','布妈'],
    8027: ['牛若丸','牛肉丸'],
    8029: ['玛丽·安托瓦内特','蛋糕','WO酱','玛丽'],
    8030: ['玛尔达','马达'],
    8031: ['美狄亚','c妈'],
    8041: ['斯忒诺','大姐'],
    8042: ['荆轲','毛腿王'],
    8045: ['玛塔·哈丽','舞娘','玛塔哈丽'],
    8046: ['卡米拉','大龙娘'],
    8056: ['清姬','斯托卡'],
    8058: ['玉藻猫','B狐'],
    8059: ['贞德','村姑'],
    8060: ['俄里翁','月神','奶茶'],
    8061: ['伊丽莎白·巴托里〔万圣节〕','C龙娘','术龙娘'],
    8062: ['玉藻前','c狐','小玉'],
    8065: ['弗朗西斯·德雷克','海盗船长','船长','德雷克'],
    8066: ['安妮·伯妮＆玛莉·瑞德','骑双子','安与玛丽'],
    8067: ['美狄亚〔Lily〕','C子','美狄亚lily'],
    8068: ['冲田总司','樱SABER','总司','冲田'],
    8070: ['斯卡哈','BBA','紫发老太婆'],
    8073: ['阿尔托莉雅·潘德拉贡〔圣诞Alter〕','骑黑呆','圣诞黑呆'],
    8074: ['童谣','魔导书','爱丽丝'],
    8075: ['开膛手杰克','女儿','小红鞋'],
    8076: ['莫德雷德','小莫','坑爹剑'],
    8082: ['弗兰肯斯坦','肯娘','弗兰'],
    8086: ['谜之女主角X','x毛','星战呆毛'],
    8088: ['布伦希尔德','布姐'],
    8090: ['尼禄·克劳狄乌斯〔花嫁〕','嫁王','花嫁尼禄'],
    8091: ['两仪式(根源)','根源式','215'],
    8092: ['两仪式','式姐','织哥','214'],
    8094: ['阿斯托尔福','黑虎阿福','阿福'],
    8097: ['南丁格尔','护士','南丁','男丁'],
    8099: ['女王梅芙','妹夫','梅芙'],
    8100: ['海伦娜·布拉瓦茨基','海妈','海伦娜'],
    8106: ['贞德〔Alter〕','黑贞'],
    8111: ['爱丽丝菲尔〔天之衣〕','太太','天之衣'],
    8112: ['酒吞童子','凹酱','酒吞'],
    8113: ['玄奘三藏','唐僧','唐三藏','唐玄奘','三藏'],
    8114: ['源赖光','奶光','赖光','奶子光'],
    8116: ['茨木童子','脚神','茨木'],
    8119: ['阿尔托莉雅·潘德拉贡(lancer)','狮子王','乳上','白枪呆','枪呆','北半球'],
    8120: ['尼托克丽丝','女法老','尼托'],
    8127: ['莱昂纳多·达·芬奇','大碧池','奸商','达芬奇'],
    8128: ['玉藻前(水着)','枪狐','泳装玉藻前'],
    8129: ['阿尔托莉雅·潘德拉贡(水着)','弓呆','泳装呆毛'],
    8130: ['玛丽·安托瓦内特(水着)','C玛丽','泳装蛋糕'],
    8131: ['安妮·伯妮＆玛莉·瑞德(水着)','弓双子','泳装双子'],
    8132: ['莫德雷德(水着)','R莫','泳装小莫','水莫'],
    8133: ['斯卡哈(水着)','杀师酱','泳装斯卡哈','泳装师匠'],
    8134: ['清姬(水着)','枪清姬','泳装清姬'],
    8135: ['玛尔达(水着)','铁拳圣女','泳装马达'],
    8136: ['伊莉雅丝菲尔·冯·爱因兹贝伦','小学生','伊利亚','伊莉雅','伊利亚斯菲尔'],
    8137: ['克洛伊·冯·爱因兹贝伦','小黑','克洛伊'],
    8138: ['伊丽莎白·巴托里〔勇者〕','剑龙娘','勇者龙娘'],
    8139: ['克娄巴特拉','艳后','埃及艳后','超高校级艳后'],
    8141: ['贞德·Alter·Santa·Lily','幼贞','圣诞幼贞'],
    8142: ['伊什塔尔','弓凛','伊修塔尔'],
    8143: ['恩奇都','小恩','小恶魔'],
    8144: ['魁札尔·科亚特尔','羽蛇神','大姐姐'],
    8146: ['美杜莎(lily)','安娜','美杜莎lily','r子'],
    8147: ['戈耳工','魔神R姐','戈尔贡'],
    8149: ['提亚马特','提妈'],
    8153: ['宫本武藏','火箭队','武藏'],
    8155: ['谜之女主角X〔Alter〕','bx毛','黑X毛'],
    8162: ['茶茶','淀殿'],
    8163: ['melt lilith','莉莉丝','刀锋战士','lls'],
    8164: ['Passionlip','lip'],
    8165: ['铃鹿御前','JK狐'],
    8166: ['BB','2B'],
    8167: ['杀生院祈荒','尼姑','杀生院','ssy'],
    8168: ['BeastⅢ／R','魔性菩萨'],
    8169: ['山鲁佐德','1001'],
    8170: ['武则天','媚娘','武媚娘'],
    8171: ['彭忒西勒亚','CEO','彭忒'],
    8174: ['保罗·班扬','伐木巨人','保罗','班杨'],
    8175: ['尼禄·克劳狄乌斯(Caster)','水尼禄','水泥'],
    8176: ['弗兰肯斯坦(Saber)','剑肯娘','泳装肯娘'],
    8177: ['尼托克丽丝(Assassin)','水尼托','泳装尼托'],
    8179: ['阿尔托莉雅·潘德拉贡〔Alter〕(Rider)','水骑呆','泳装黑呆'],
    8180: ['海伦娜·布拉瓦茨基(Archer)','奥特曼','泳装海伦娜','弓海伦娜'],
    8181: ['源赖光(Lancer)','枪奶光','泳装源赖光'],
    8182: ['伊什塔尔(Rider)','骑凛','泳装凛'],
    8183: ['帕尔瓦蒂','雪山樱'],
    8184: ['巴御前','鲅鱼圈','817'],
    8185: ['望月千代女','蛇巫女'],
    8188: ['加藤段藏','飞加藤','段藏'],
    8189: ['刑部姬','老邢','宅女'],
    8190: ['机械伊丽酱','机械龙娘'],
    8191: ['机械伊丽酱II号机','机械龙娘2号'],
    8192: ['喀耳刻','C姑妈','喀尔刻','猪妈'],
    8193: ['哪吒','三太子'],
    8194: ['示巴女王','所罗门老婆','示巴'],
    8195: ['阿比盖尔·威廉姆斯','阿比','阿比盖尔','Abigail'],
    8196: ['埃蕾什基伽勒','艾蕾','枪凛'],
    8197: ['阿蒂拉·圣诞','弓大王','弓提拉','圣诞阿提拉'],
    8198: ['葛饰北斋','阿荣','北宅'],
    8199: ['塞弥拉弥斯','女帝'],
    8200: ['浅上藤乃','拆桥','藤乃'],
    8201: ['阿纳斯塔西娅','皇女'],
    8202: ['阿塔兰忒〔Alter〕','黑塔','黑阿塔','狂塔','狂阿塔','猪皮塔'],
    8209: ['冲田总司〔Alter〕','魔总','魔神总司'],
    8214: ['瓦尔基里','女武神'],
    8215: ['斯卡哈=斯卡蒂','CBA','斯卡蒂'],
    8216: ['贞德(水着)','弓贞','姐姐','泳装贞德'],
    8217: ['茨木童子(水着)','枪茨木','泳装茨木'],
    8218: ['牛若丸(水着)','狗肉丸','泳装牛肉丸'],
    8219: ['贞德〔Alter〕(水着)','狂贞','泳装黑贞','水黑贞'],
    8220: ['BB(水着)','泳装bb'],
    8221: ['女王梅芙(水着)','泳装梅芙','水梅芙','剑梅芙'],
    8222: ['谜之女主角XX','XX毛'],
    8224: ['志度内','熊莉亚'],
    8225: ['酒吞童子(护法少女)','C酒吞'],
    8228: ['秦良玉','包子头'],
    8230: ['虞美人','摸虞','虞姬'],
    8232: ['布拉达曼特','尻枪','屁股枪'],
    8233: ['魁札尔·科亚特尔〔桑巴／圣诞〕','圣诞羽蛇神'],
    8234: ['红阎魔','小麻雀'],
    8236: ['美游·艾德费尔特','卫宫美游','美游'],
    8237: ['紫式部','奶紫'],
    8238: ['Kingprotea','巨萝莉', '巨樱', '绷带樱','帝王花'],
    8239: ['迦摩','夹馍','伽摩'],
    8240: ['BeastⅢ／L','黑樱'],
    8241: ['司马懿','莱妹','义妹','莱妮丝'],
    8242: ['阿斯特蕾亚','金钻头'],
    8243: ['格蕾','小灰','格雷'],
    8245: ['拉克什米·芭伊','印度贞德'],
    8250: ['魔王信长','魔信'],
    8252: ['长尾景虎','上杉谦信'],
    8253: ['莱昂纳多·达·芬奇(lily)','小碧池','达芬骑','达芬奇lily'],
    8255: ['帕里斯','白莲花'],
    8259: ['夏绿蒂·科黛','暗杀天使','夏绿蒂'],
    8260: ['莎乐美','病娇'],
    8261: ['宫本武藏(水着)','水武藏'],
    8262: ['刑部姬(水着)','弓刑','泳装刑部姬'],
    8263: ['卡米拉(水着)','骑米拉','泳装大龙娘'],
    8264: ['葛饰北斋(水着)','剑北斋','泳装北宅'],
    8265: ['阿尔托莉雅·潘德拉贡(兔女郎)','兔子王'],
    8266: ['朗姆达莉莉丝','企鹅莉莉丝','lilith(水着)'],
    8267: ['冲田总司(水着)','杀总司','泳装总司'],
    8268: ['宇宙伊修塔尔','宇宙凛','仇凛'],
    8269: ['灾星简','野姑娘杰恩','简'],
    8270: ['阿斯托尔福(saber)','剑阿福','乌鸦坐飞机'],
    8271: ['南丁格尔(圣诞)','弓南丁','圣诞南丁'],
    8274: ['欧罗巴','祖奶奶'],
    8275: ['杨贵妃','杨玉环'],
    8276: ['清少纳言','Switch','VTB'],
    8278: ['狄俄斯库里','双子座','内田骨科'],
    8279: ['凯妮斯'],
    8283: ['宇津见绘里世','14岁','绘里世','爱丽瑟'],
    8284: ['阿尔托利雅(caster)','Caber','c呆'],
    8285: ['杀生院祈荒(水着)','水杀生院','人鱼','泳装杀生院'],
    8286: ['伊莉雅丝菲尔·冯·爱因兹贝伦(水着)','泳装伊莉雅','泳装伊利亚'],
    8287: ['布伦希尔德(水着)','泳装布姐'],
    8288: ['虞美人(水着)','水鱼','泳装虞姬','水虞姬'],
    8289: ['阿比盖尔·威廉姆斯〔夏〕','泳装阿比','水阿比'],
    8290: ['巴御前(水着)','泳装巴御前','水鲅鱼圈'],
    8291: ['紫式部(水着)','水紫奶','泳装紫式部'],
    8295: ['梵高','向日葵'],
    8296: ['尼莫','尼摩船长'],
    8299: ['伊吹童子'],
    8300: ['弗栗多'],


}
