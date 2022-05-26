import random

from hoshino import util
from .. import chara

class Gacha(object):

    def __init__(self, pool_name: str = "CN"):
        super().__init__()
        self.load_pool(pool_name)


    def load_pool(self, pool_name: str):
        config = util.load_config(__file__)
        pool = config[pool_name]
        self.up_prob = pool["up_prob"]
        self.s3_prob = pool["s3_prob"]
        self.s2_prob = pool["s2_prob"]
        self.s1_prob = 1000 - self.s3_prob - self.s2_prob
        self.up = pool["up"]
        self.star3 = pool["star3"]
        self.star2 = pool["star2"]
        self.star1 = pool["star1"]

        self.up_star = pool["up_star"]
        self.up3_prob = 0
        self.up2_prob = 0
        self.up1_prob = 0
        for i in range(len(self.up)):
            if self.up_star[i] == 3:
                self.up3_prob += self.up_prob[i]
            elif self.up_star[i] == 2:
                self.up2_prob += self.up_prob[i]
            else:
                self.up1_prob += self.up_prob[i]


    def gacha_one(self, up3_prob: int, up2_prob: int, up1_prob: int, s3_prob: int, s2_prob: int, s1_prob: int = None):
        if s1_prob is None:
            s1_prob = 1000 - s3_prob - s2_prob
        total_ = s3_prob + s2_prob + s1_prob
        pick = random.randint(1, total_)
        up = self.up
        up_star = self.up_star
        up_prob = self.up_prob
        if pick <= up3_prob + up2_prob + up1_prob:
            if not s1_prob:
                for i, star in enumerate(self.up_star):
                    if star == 1:
                        up_prob[i] = 0
            name = random.choices(up, up_prob, k=1)[0]
            i = up.index(name)
            star = up_star[i]
            return chara.fromname(name, star)
        elif pick <= s3_prob + up2_prob + up1_prob:
            return chara.fromname(random.choice(self.star3), 3)
        elif pick <= s3_prob + s2_prob + up1_prob:
            return chara.fromname(random.choice(self.star2), 2)
        else:
            return chara.fromname(random.choice(self.star1), 1)
    

    def gacha_ten(self):
        result = []
        up3 = self.up3_prob
        up2 = self.up2_prob
        up1 = self.up1_prob
        s3 = self.s3_prob
        s2 = self.s2_prob
        s1 = 1000 - s3 - s2
        for i in range(9):
            c = self.gacha_one(up3, up2, up1, s3, s2, s1)
            result.append(c)
        c = self.gacha_one(up3, up2, 0, s3, s2 + s1, 0)
        result.append(c)

        return result


    def gacha_tenjou(self):
        result = {'up': [], 's3': [], 's2': [], 's1': []}
        first_up_pos = 99999
        up3 = self.up3_prob
        up2 = self.up2_prob
        up1 = self.up1_prob
        s3 = self.s3_prob
        s2 = self.s2_prob
        s1 = 1000 - s3 - s2
        for i in range(9 * 30):
            c = self.gacha_one(up3, up2, up1, s3, s2, s1)
            if c.star == 1:
                result['s1'].append(c)
            elif c.star == 2:
                result['s2'].append(c)
            elif c.name in self.up:
                result['up'].append(c)
                first_up_pos = min(first_up_pos, 10 * ((i + 1) // 9) + ((i + 1) % 9))
            elif c.star == 3:
                result['s3'].append(c)
            else:
                pass
            
        for i in range(30):
            c = self.gacha_one(up3, up2, 0, s3, s2 + s1, 0)
            if c.star == 2:
                result['s2'].append(c)
            elif c.name in self.up:
                result['up'].append(c)
                first_up_pos = min(first_up_pos, 10 * (i + 1))
            elif c.star == 3:
                result['s3'].append(c)
            else:
                pass
        result['first_up_pos'] = first_up_pos
        return result      

    def gacha_tenjou_jp(self):
        result = {'up': [], 's3': [], 's2': [], 's1': []}
        first_up_pos = 99999
        up3 = self.up3_prob
        up2 = self.up2_prob
        up1 = self.up1_prob
        s3 = self.s3_prob
        s2 = self.s2_prob
        s1 = 1000 - s3 - s2
        for i in range(9 * 20):
            c = self.gacha_one(up3, up2, up1, s3, s2, s1)
            if c.star == 1:
                result['s1'].append(c)
            elif c.star == 2:
                result['s2'].append(c)
            elif c.name in self.up:
                result['up'].append(c)
                first_up_pos = min(first_up_pos, 10 * ((i + 1) // 9) + ((i + 1) % 9))
            elif c.star == 3:
                result['s3'].append(c)
            else:
                pass
            
        for i in range(20):
            c = self.gacha_one(up3, up2, 0, s3, s2 + s1, 0)
            if c.star == 2:
                result['s2'].append(c)
            elif c.name in self.up:
                result['up'].append(c)
                first_up_pos = min(first_up_pos, 10 * (i + 1))
            elif c.star == 3:
                result['s3'].append(c)
            else:
                pass
        result['first_up_pos'] = first_up_pos
        return result     