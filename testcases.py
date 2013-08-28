
import calculator
from calculator import person, testator



def adder(new, peopleDict, spouseAlive, motherAlive, fatherAlive, gender):
    new.spouseAlive = spouseAlive
    new.motherAlive = motherAlive
    new.fatherAlive = fatherAlive
    new.gender = gender
    for i, j in peopleDict.iteritems():
        new.quickAdd("Female", i, j, numKids = 0)
    return new
    

    

def main():
    new = testator()
#    new.initialize()
    #pass dict e.g., ({"boys": 3, "girls": 2, "sisters": 1}), and parameters (gender, spouseAlive, motherAlive, fatherAlive), loop through dict, set parameters, and then calculate
    adder(new, {"boys": 2, "girls": 1}, spouseAlive = True, motherAlive = False, fatherAlive = True, gender = "Female")
#    quickAdd("Female",  "sisters",  numPeople = 5,  numKids = 0) #this can be used to add new people with kids for a test suite
    values = calculator.calculate(new)    
    del(new)
    test1 = testator()
    print 'hi'
#    assert func(3) is 22 "testcase func failed"
    
if( __name__ == "__main__" ):
    main()
