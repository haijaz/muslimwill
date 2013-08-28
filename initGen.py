list = "boys, girls, father, mother, brothers, sisters, grandchildren, gender,  spouse,  eds ,  maleEds, splitChildren,  residue,  fatherAlive,  motherAlive,  spouseAlive"
a = list.replace(" ", "").split(',')
print a
f = open("output.txt", 'w')
s = ""
for x in a:
    s += "if %s is None:\n" %x
    s += "    self.%s = []\n" %x  # default values
    s += "else:\n"
    s += "    self.%s = %s\n" %(x, x)
f.write(s)
f.close()