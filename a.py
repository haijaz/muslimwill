from __future__ import division
from flask import Flask, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask.ext.mako import MakoTemplates, render_template
from flask.ext.wtf import Form, TextField, BooleanField, PasswordField, SelectMultipleField, SelectField, validators, Required
import calculator


app = Flask(__name__)
mako = MakoTemplates(app)
app.secret_key = 'aas8df98wf298r2#@#$ASDF'

#def calcSpouse(new, eds):
#    if eds==0:
#        if new.gender=="Female":
#            spShare = 1/2
#        else:
#            spShare=1/4
#    else:
#        if new.gender=="Female":
#            spShare = 1/4
#        else:
#            spShare = 1/8
#    return spShare

def dShare(new, bShare):
    if len(new.boys)==0:
        if len(new.girls)==0:
            dShare = 0
        if len(new.girls)==1:
            dShare = 1/2
        if len(new.girls)>=2:
            dShare = 2/3
    if len(new.boys)!=0:
        dShare = bShare * (1/2)
    if trackme == 15:
            print sucks
    return dShare

def calcFather(new, eds, residue, maleEds):
    if eds>=1:
        fShare = 1/6
    if not maleEds:
        fShare = 1/6 + residue
    if not eds:
        fShare = residue
    return fShare

def calcMother(new, eds, residue):
     if eds>=1 or (len(new.brothers)+len(new.sisters)>0):
         mShare = 1/6
     if not eds:
         if (len(new.brothers)+len(new.sisters)) == 0: #complete
             pass

def findMaleEds(new):
    maleEds = 0
    if len(new.boys) >=1:
        maleEds = 1                                            #male entitled descendants
    # if len(new.grandchildren) > 0:
    for child in new.grandchildren:
        if child["gender"] == "Male":
            maleEds=1
    return maleEds

def calculate(information):
    spouseAlive = 4 #needs to change this
    new = testator(gender="Female")
    for i in range(int(information["numBoys"].data)):
        new.addRelation({'name': 'Bob', 'gender': 'Male', 'alive': 'yes'}, "boys")
    for i in range(int(information["numGirls"].data)):
        new.addRelation({'name': 'Babs', 'gender': 'Female', 'alive': 'yes'}, "girls")
    new.addRelation({'name': 'bro',  'gender': 'Female', 'alive': 'yes'},  "brothers")
    print new["brothers"][0]["name"]
    test = []
    for value in information:
        if value.type == "TextField":
            test.append(int(value.data)+5)
    eds = 0
    eds = len(new.boys)+len(new.girls)+len(new.grandchildren) #entitled descendants
    # maleEds = findMaleEds(new)

    # if spouseAlive:
        # spShare = calcSpouse(new, eds)
    # else:
        # spShare = 0
    # # residue = 1 - spShare #add in other shares
    # # fShare = calcFather(new, eds, residue, maleEds)
    # # bShare = #must be before dShare, since dShare may be contingent
    # # dShare = calcDaughter(new)
    # # fShare = calcFather(new, eds, maleEds, residue) # residue must first be calculated
    # print spShare
    # print maleEds
    # print eds
    # return test

#[find]forms
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

class formtest(Form):
    numBoys = TextField('numBoys')
    numGirls  = TextField('numGirls')
    numSisters = TextField('numSisters')
    numBrothers = TextField('numBrothers')

class infoForm(Form):
    fName= TextField('fName')
    lName= TextField('lName')
    numBoys = TextField('numBoys')
    numGirls= TextField('numGirls')

@app.route('/testform/', methods=['GET', 'POST'])
def testform():
    form = formtest()
    if request.method == 'POST':
        results = calculate(form)
        return render_template('results.html', results = results)
    return render_template('testform.html', form = form)

#[find]routes
#
#
#
# @app.route('/')
# def index():
    # return render_template('mindex.html')

@app.route('/')
@app.route('/info/', methods=['GET', 'POST'])
def info():
    form = infoForm(request.form)
    if request.method == 'POST':
        return render_template('newwill.html', form = form)
    return render_template('mindex.html', form = form)

@app.route('/newwill/', methods=['GET', 'POST'])
def newwill(form):
    if request.method == 'POST':
        results = calculate(request)
        return render_template('results.html', results = results)
    return render_template('newwill.html', form = form)


if __name__ == '__main__':
    app.run(debug = True, host='0.0.0.0', port=81)
