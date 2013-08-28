from __future__ import division

class person():
    def __init__(self, name, children,  gender,  alive):
        self.name = name
        self.children = children
        self.gender = gender
        self.alive = alive
        # a dict with relationship?, gender, and alive and ...?

class testator():
    def __init__(self, boys=[], girls=[], father=person, mother=person, brothers=[], sisters=[], 
                    grandchildren=[], gender = "",  spouse = person,  eds = 0,  maleEds=0, 
                    splitChildren = "",  residue = 1):
        self.boys = boys
        self.girls = girls
        self.father = father
        self.mother = mother
        self.brothers = brothers
        self.sisters = sisters
        self.grandchildren = grandchildren
        self.gender = gender
        self.spouse = spouse
        self.eds = eds
        self.maleEds = maleEds
        self.splitChildren = splitChildren
        self.residue = residue


    def addRelation(self, person, relationship):
        l = getattr(self, relationship)
        l.append(person)
        l is getattr(self, relationship)
        return self
