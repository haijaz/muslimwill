from __future__ import division

class person():
    def __init__(self, name, children,  gender,  alive):
        self.name = name
        self.children = children
        self.gender = gender
        self.alive = alive
        # a dict with relationship?, gender, and alive and ...?

class testator():
    def __init__(self, boys = None, girls = None, father = None, mother = None, brothers = None, sisters = None, 
                    grandchildren = None, gender = None,  spouse = None,  eds  = None,  maleEds = None, 
                    splitChildren = None,  residue = None,  fatherAlive = None,  motherAlive = None,  spouseAlive = None):
        if boys is None:
            self.boys = []
        else:
            self.boys = boys
        if girls is None:
            self.girls = []
        else:
            self.girls = girls
        if father is None:
            self.father = []
        else:
            self.father = father
        if mother is None:
            self.mother = []
        else:
            self.mother = mother
        if brothers is None:
            self.brothers = []
        else:
            self.brothers = brothers
        if sisters is None:
            self.sisters = []
        else:
            self.sisters = sisters
        if grandchildren is None:
            self.grandchildren = []
        else:
            self.grandchildren = grandchildren
        if gender is None:
            self.gender = []
        else:
            self.gender = gender
        if spouse is None:
            self.spouse = []
        else:
            self.spouse = spouse
        if eds is None:
            self.eds = []
        else:
            self.eds = eds
        if maleEds is None:
            self.maleEds = []
        else:
            self.maleEds = maleEds
        if splitChildren is None:
            self.splitChildren = []
        else:
            self.splitChildren = splitChildren
        if residue is None:
            self.residue = []
        else:
            self.residue = residue
        if fatherAlive is None:
            self.fatherAlive = []
        else:
            self.fatherAlive = fatherAlive
        if motherAlive is None:
            self.motherAlive = []
        else:
            self.motherAlive = motherAlive
        if spouseAlive is None:
            self.spouseAlive = []
        else:
            self.spouseAlive = spouseAlive



    def addRelation(self, person, relationship):
        l = getattr(self, relationship)
        l.append(person)
        l is getattr(self, relationship)
        return self
        
    def initialize(self):
    # add relatives and spouse
        self.gender = "Female"
        self.residue = 1
        spouse = person(name = "spouse", gender = "Female",  alive="Yes",  children="")
        self.spouseAlive = True
        self.spouse = spouse
        self.fatherAlive = True
        for i in range(2):
            self.addRelation({'name': 'Bob', 'gender': 'Male', 'alive': 'yes'}, "boys")
        for i in range(1):
            self.addRelation({'name': 'Babs', 'gender': 'Female', 'alive': 'yes'}, "girls")
        bro = person(name='bro',  gender = 'Male', alive ='yes', children = [])
        kid1 = person(name="test",  gender="Male",  alive="yes",  children = [])
        self.addRelation(bro,  "brothers")
        self.addRelation({'name': 'Bob', 'gender': 'Male', 'alive': 'yes'},  "brothers")
        self.brothers[0].children.append(kid1)
        return self
        
    def quickAdd(self, gender,  relationship,  numPeople,  numKids):
        relation = person(name='bro',  gender = gender, alive ='yes', children = [])
        self.addRelation(relation,  relationship)
        for i in range(numPeople-1):
            if numKids != 0:
                for i in range(numKids - 1):
                    kid1 = person(name="test",  gender="Male",  alive="yes",  children = [])
                    relation.children.append(kid1)
            self.addRelation(relation,  relationship)
        return self

def calcSpouse(new):
    if new.spouseAlive == False:
        spShare = 0
    else:
        if new.eds==0:
            if new.gender=="Female":
                spShare = 1/2
            else:
                spShare=1/4
        else:
            if new.gender=="Female":
                spShare = 1/4
            else:
                spShare = 1/8
    return spShare

def calcDaughters(new):
    dShare = 0
    if len(new.boys) and len(new.girls):
        new.splitChildren = True
        dShare = 0 #oops
    elif len(new.boys) and not len(new.girls):
        new.splitChildren = False
        dShare = 0
    elif len(new.girls) and not len(new.boys):       
        if len(new.girls)==1:
            dShare = 1/2
        if len(new.girls)>=2:
            dShare = 2/3
    return dShare

def calcSons(new):
    dShare = 0
    sShare = 0
    if len(new.boys) and len(new.girls):
        numKids = (len(new.boys)*2) + len(new.girls)
        sShare = new.residue*(2 / numKids)
        dShare = new.residue*(1 / numKids)
    elif len(new.boys) and not len(new.girls):
        sShare = residue
        dShare = 0
    
    return sShare, dShare

def calcEds(new):
    new.eds = len(new.boys)+len(new.girls)+len(new.grandchildren)
    findMaleEds(new)
    return new.eds

def calcFather(new):
    if new.eds>=1:
        fShare = 1/6
    if not new.maleEds:
        fShare = 1/6 + new.residue
    if not new.eds:
        fShare = new.residue
    if new.fatherAlive == False:
        fShare = 0
    return fShare

def calcMother(new):
    if new.eds>=1 or (len(new.brothers)+len(new.sisters)>0):
        mShare = 1/6
    if not new.eds:
        if (len(new.brothers)+len(new.sisters)) == 0 and new.spouseAlive=="False" and new.father.alive == "False":
            mShare = 1/3 #complete
        else:
            mShare = new.residue/3
    if new.motherAlive == False:
        mShare = 0
    return mShare

def findMaleEds(new):
    new.maleEds = 0
    if len(new.boys) >=1:
        new.maleEds = 1                                            #male entitled descendants
    # if len(new.grandchildren) > 0:
    for child in new.grandchildren:
        if child["gender"] == "Male":
            new.maleEds=1
    return new.maleEds

def calculate(new):
    values = {}
    calcEds(new)

    values["spShare"]= round(calcSpouse(new), 4)
    values["mShare"] = round(calcMother(new), 4)
    values["fShare"] = round(calcFather(new), 4)
    values["dShare"] = round(calcDaughters(new), 4)
    new.residue = 1
    for i, j in values.iteritems():
        new.residue = new.residue - j
    values["sShare"], values["dShare"] = calcSons(new)
    values["sShare"] = round(values["sShare"],  4)
    values["dShare"] = round(values["dShare"],  4)
    return values
