
from __future__ import division
import copy
import os
from sqlalchemy import Column, Integer, String, create_engine, ForeignKey, Date
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
Base = declarative_base()
engine = create_engine('sqlite:///test4.db', echo=False) #set echo to True for debug statements
Session = sessionmaker(bind=engine)
session = Session()

if open('test4.db'):
    os.remove('test4.db')
    
class Testator(Base):
    __tablename__ = 'testator'
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    gender = Column(String)
    relatives = relationship("Relations", backref="testator", lazy="dynamic")
    
    def __init__(self, name, gender):
        self.name = name
        self.gender = gender

class Relations(Base):
    __tablename__ = "relations"
    
    id = Column(Integer, primary_key = True)
    name = Column(String)
    alive = Column(String)
    relationType = Column(Integer, ForeignKey('lookupRelations.id'))
    fromPerson = Column(Integer, ForeignKey('testator.id'))
    parent_id = Column(Integer, ForeignKey('relations.id'))
    children = relationship("Relations")

    def __init__(self, name, alive, relationType):
        self.name = name
        self.alive = alive
        self.relationType = relationType
        
class lookupRelations(Base):
    __tablename__ = "lookupRelations"
    
    id = Column(Integer, primary_key = True)
    name = Column(String)
    
    def __init__(self, name):
        self.name = name
        
def getRIDbyName(relType):
    return session.query(lookupRelations).filter(lookupRelations.name==relType).first().id
    
def initLookup(session):
    relationList  = ["spouse", "mother", "father", "brother", "sister", "daughter", "son", "nephew", "neice", "aunt", "uncle", "grandchildren"]
    for a in relationList:
        a = lookupRelations(a)
        session.add(a)

def calcEds(new):
    list = []
    list.append(getRIDbyName("son"))
    list.append(getRIDbyName("daughter"))
    list.append(getRIDbyName("grandchildren"))
    eds = new.relatives.filter(Relations.relationType.in_(list)).count()
    return eds
    
def calcSpouse(new, values):
    spouse = new.relatives.filter(Relations.relationType==getRIDbyName("spouse")).first()
    if spouse and spouse.alive == "True":
        if calcEds(new) == 0:
            if new.gender=="female":
                values["spShare"] = 1/2
            else:
                values["spShare"] = 1/4
        else:
            if new.gender=="female":
                values["spShare"] = 1/4
            elif new.gender=="male":
                values["spShare"] = 1/8    
        values["residue"] -= values["spShare"]
    return values
    
def calcChildren(new, values):
    numBoys = new.relatives.filter(Relations.relationType==getRIDbyName("son")).count()
    numGirls = new.relatives.filter(Relations.relationType==getRIDbyName("daughter")).count()    
    if numBoys and numGirls:
        numKids = (numBoys*2) + numGirls
        values["sShare"] = values["residue"]*(2 / numKids)
        values["dShare"] = values["residue"]*(1 / numKids)
        values["residue"] = values["residue"] - values["sShare"] - values["dShare"]
    elif numBoys and not numGirls:
        values["sShare"] = values["residue"]
        values["residue"] = 0
    elif numGirls and not numBoys:       
        if numGirls==1:
            values["residue"] -= 1/2
            values["dShare"] = 1/2
            print values["residue"]
        if numGirls>=2:
            values["residue"] -= 2/3
            values["dShare"] = 2/3 + values["residue"]
    return values

def calcParents(new, values):
    father = new.relatives.filter(Relations.relationType==getRIDbyName("father")).first()
    mother = new.relatives.filter(Relations.relationType==getRIDbyName("mother")).first()
    if father and father.alive and mother and mother.alive:
        if calcEds(new)>=1:
            values["fShare"], values["mShare"] = 1/6, 1/6
            values["residue"] -= 1/3
            values = calcChildren(new, values)
            if values["residue"] >= 0:
                values["fShare"] += values["residue"]
                values["residue"] = 0
        else:
            values["mShare"] = 1/6
            values["residue"] -=  1/6
            values["fShare"] = values["residue"]
            values["residue"] = 0
    elif father and father.alive:
        values["fShare"] = 1/6
        values["residue"] -= 1/6
        values = calcChildren(new, values)        
    elif mother and mother.alive:
        values["mShare"] = 1/6
        values["residue"] -= 1/6
        values = calcChildren(new, values) 
    else:
        values = calcChildren(new, values)
    return values

def findMaleEds(new):
    maleEds = False
    if new.relatives.filter(Relations.relationType==getRIDbyName("son")).count() >=1:
        maleEds = True
    # if len(new.grandchildren) > 0:
    for child in new.relatives.filter(Relations.relationType==getRIDbyName("grandchildren")).all():
        if child.gender== "Male":  #need to make a way to distinguish between kids and grandkids while retaining information about which child (of testator) the grandchild descends from
            maleEds=False
    return maleEds

def init():
    person = Testator("first", "Female")
    mother = Relations("father", "True", getRIDbyName("mother"))
    person.relatives.append(mother)
    session.add(person)
    session.commit()
    return session.query(Testator).filter(Testator.name=="first").first()
    
def calculate(new):
    values = dict()
    values["residue"] = 1
    values = calcSpouse(new, values)
    values = calcParents(new, values)
    total = 0
    for i, j in values.iteritems():
        if i !="residue":
            total +=j
    if total != 0 :
        for i, j in values.iteritems():
            values[i] = j/total
    values["residue"]=0
    for i, j in values.iteritems():
        values[i] = round(j, 4)
    return values

    
def makePerson(gender, lstRelatives, testName):
    values = dict()
    values["residue"] = 1
    person = Testator(gender+",".join(testName), gender)
    for i in lstRelatives:
        a = Relations(i, "True", getRIDbyName(i))
        person.relatives.append(a)
    session.add(person)
    session.commit()
    # return session.query(Testator).filter(Testator.name==gender+",".join(testName)).first()
    return session.query(Testator).filter(Testator.id==person.id).first()
    
def test_cases():
    # lister = [{"testName": "test1", "valIn": 2, "valOut": 1},
               # {"testName": "test2", "valIn": 4, "valOut": 1},
               # {"testName": "test3", "valIn": 1, "valOut": 1}]
    tValues = defineTestCases()
    for i in tValues:
        guy = makePerson(i["gender"], i["testName"], i["testName"])
        i["outputValue"] = calculate(guy)
        yield check_equal, (i["gender"]+",".join(i["testName"])), i["expectedValue"], i["outputValue"]

def check_equal(testName, expectedValue, outputValue):
    assert expectedValue == outputValue, "%s failed with values \n exp %s \n act %s" % (testName, expectedValue, outputValue)

def runtests():
    import nose
    from nose.tools import eq_ as eq
    nose.run(defaultTest=__name__, argv=[__file__, "-v"])

def defineTestCases():
    testValues =    [
    
                    {"testName": ["mother"],
                    "gender": "female",
                    "expectedValue":    {   "mShare": round(1/1, 4),
                                            "residue": 0}},    
    
                    {"testName": ["mother", "father"],
                    "gender": "female",
                    "expectedValue":    {   "fShare": round(5/6, 4),
                                            "mShare": round(1/6, 4),
                                            "residue": 0}},

                    {"testName": ["mother", "son"],
                    "gender": "female",
                    "expectedValue":    {   "sShare": round(5/6, 4),
                                            "mShare": round(1/6, 4),
                                            "residue": 0}},

                    {"testName": ["mother", "daughter"],
                    "gender": "female",
                    "expectedValue":    {   "dShare": round(3/4, 4),
                                            "mShare": round(1/4, 4),
                                            "residue": 0}},

                    {"testName": ["mother", "son", "daughter"],
                    "gender": "female",
                    "expectedValue":    {   "sShare": round(5/9, 4),
                                            "mShare": round(1/6, 4),
                                            "dShare": round(5/18,4),
                                            "residue": 0}},
                                            
                    {"testName": ["mother", "father", "daughter"],
                    "gender": "female",
                    "expectedValue":    {   "residue": 0,
                                            "fShare": round(1/3, 4),
                                            "mShare": round(1/6, 4),
                                            "dShare": round(1/2, 4)}},
                                            
                    {"testName": ["mother", "father", "son"],
                    "gender": "female",
                    "expectedValue":    {   "residue": 0,
                                            "fShare": round(1/6, 4),
                                            "mShare": round(1/6, 4),
                                            "sShare": round(2/3, 4)}},
                                            
                    {"testName": ["mother", "father", "daughter", "son"],
                    "gender": "female",
                    "expectedValue":    {   "residue": 0,
                                            "fShare": round(1/6, 4),
                                            "mShare": round(1/6, 4),
                                            "dShare": round(2/9, 4),
                                            "sShare": round(4/9, 4)}},
                                            
                    {"testName": ["mother", "father", "daughter", "daughter"],
                    "gender": "female",
                    "expectedValue":    {   "residue": 0,
                                            "fShare": round(1/6, 4),
                                            "mShare": round(1/6, 4),
                                            "dShare": round(2/3, 4)}},
                                            
                    {"testName": ["spouse", "son"],
                    "gender": "male",
                    "expectedValue":    {   "residue": 0,
                                            "spShare": round(1/8, 4),
                                            "sShare": round(7/8, 4)}},
                                            
                    {"testName": ["spouse", "mother", "father", "daughter"],
                    "gender": "male",
                    "expectedValue":    {   "residue": 0,
                                            "spShare": round(1/8, 4),
                                            "fShare": round(5/24, 4),
                                            "mShare": round(2/12, 4),
                                            "dShare": round(2/4, 4)}},
                                            
                    {"testName": ["spouse", "mother", "father", "daughter"],
                    "gender": "female",
                    "expectedValue":    {   "residue": 0,
                                            "spShare": round(3/13, 4),
                                            "fShare": round(2/13, 4),
                                            "mShare": round(2/13, 4),
                                            "dShare": round(6/13, 4)}},
                    
                    ]
    return testValues

def main():
    Base.metadata.create_all(engine)
    initLookup(session)
    runtests()
    
if __name__=="__main__":
   main()



