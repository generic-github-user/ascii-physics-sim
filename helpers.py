class Name:
    def __init__(self, name, abbr):
        self.name = name
        self.abbr = abbr

class Unit:
    def __init__(self, name, abbr, utype):
        self.name = name
        self.abbr = abbr
        self.utype = utype

class Angle:
    def __init__(self, deg=0):
        self.deg = deg % 360
    def set(self, deg=0):
        self.deg = deg % 360
