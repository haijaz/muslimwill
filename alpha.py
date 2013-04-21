import os
import sys
print sys.path[0]
from werkzeug.security import generate_password_hash
from first import db, User
if os.access('test2.db', os.F_OK):
	os.remove('test2.db')
	print 'deleted'
	pass

db.create_all()
test = generate_password_hash('test')
new_user = User(fname = 'a', 
				lname = 'b',
				email = 'c',
				username = 'a',
				pword = test)
db.session.add(new_user)
db.session.commit()
test = generate_password_hash('test')
new_user = User(fname = 'b', 
				lname = 'b',
				email = 'ca',
				username = 'b',
				pword = test)
db.session.add(new_user)
db.session.commit()
exit()