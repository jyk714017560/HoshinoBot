from hoshino import util
from .sqlitegacha import SqliteGacha

class GachaMaster(object):

    def __init__(self, uid):
        super().__init__()
        self.uid = uid
        self.sqlitegacha = SqliteGacha()
    
    def add_colle(self, colle, jewel, hiishi):
        return self.sqlitegacha.add({'uid': self.uid, 'colle': colle, 'jewel': jewel, 'hiishi': hiishi})
    def mod_colle(self, colle, jewel, hiishi):
        return self.sqlitegacha.modify({'uid': self.uid, 'colle': colle, 'jewel': jewel, 'hiishi': hiishi})
    def has_colle(self):
        return True if self.sqlitegacha.find_one(self.uid) else False
    def get_colle(self):
        return self.sqlitegacha.find_one(self.uid)