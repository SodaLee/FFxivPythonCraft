from inspect import isclass
from . import Models
from .Utils import CallOrVar


class _SkillManager(dict):
    def load(self):
        from core.Simulator import Skills
        self.clear()
        self.list = set()
        for attr in dir(Skills):
            cls = getattr(Skills, attr)
            if isclass(cls) and cls != Models.SkillBase and issubclass(cls, Models.SkillBase):
                temp = cls()
                setattr(self, attr, temp)
                self[temp.name] = getattr(self, attr)
                if not cls.HIDE:
                    self.list.add(temp.name)

    def getCp(self, key, status):
        return CallOrVar(self[key].calc_cp, status)

    def getProgress(self, key, status):
        return CallOrVar(self[key].calc_progress, status)

    def getQuality(self, key, status):
        return CallOrVar(self[key].calc_quality, status)

    def getDurability(self, key, status):
        return CallOrVar(self[key].calc_durability, status)


class _BuffManager(dict):
    def load(self):
        from core.Simulator import Buffs
        self.clear()
        for attr in dir(Buffs):
            cls = getattr(Buffs, attr)
            if isclass(cls) and cls != Models.BuffBase and issubclass(cls, Models.BuffBase):
                setattr(self, attr, cls())
                self[attr] = getattr(self, attr)


class _BallManager(dict):
    def load(self):
        from core.Simulator import Balls
        self.clear()
        for attr in dir(Balls):
            cls = getattr(Balls, attr)
            if isclass(cls) and cls != Models.BuffBase and issubclass(cls, Models.BallBase):
                setattr(self, attr, cls())
                self[attr] = getattr(self, attr)
                self[self[attr].name] = getattr(self, attr)
        self.defaultBall = self[Balls.DefaultBall.name] if hasattr(Balls, "DefaultBall") else Models.BallBase()


SkillManager = _SkillManager()
BuffManager = _BuffManager()
BallManager = _BallManager()


def managers_load():
    for manager in [SkillManager, BuffManager, BallManager]: manager.load()
