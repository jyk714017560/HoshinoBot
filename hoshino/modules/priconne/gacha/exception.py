class ClanBattleError(Exception):
    def __init__(self, msg, *msgs):
        self._msgs = [msg, *msgs]

    def __str__(self):
        return '\n'.join(self._msgs)

    @property
    def message(self):
        return str(self)


class DatabaseError(ClanBattleError):
    pass