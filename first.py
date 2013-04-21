import sys
from bs4 import BeautifulSoup
from flask import Flask, flash, url_for, render_template, request, redirect, session, escape
from flask_sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager, login_required, login_user, current_user, logout_user, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
from flask.ext.wtf import Form, TextField, BooleanField, PasswordField, SelectMultipleField, SelectField, validators, Required

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///%s\\test2.db' %sys.path[0]
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.setup_app(app)
app.secret_key = 'aas8df98wf298r2#@#$ASDF'

# forms

# class LoginForm(Form):
    # username = TextField('username', [Required()])
    # password = PasswordField('password', default = False)
	
class infoForm(Form):
	fName= TextField('fName')
	lName= TextField('lName')
	numBoys = TextField('numBoys')
	numGirls= TextField('numGirls')

# class User(db.Model):
	# id = db.Column(db.Integer, primary_key=True)
	# username = db.Column(db.String(80), unique=True)
	# email = db.Column(db.String(80), unique=False, nullable=True) # make this unique in the future
	# fname = db.Column(db.String(80))
	# lname = db.Column(db.String(80))
	# pword = db.Column(db.String(160))
	# search = db.relationship('Search', backref='user', lazy='dynamic')
	

	# def __init__(self, username, email, fname, lname, pword):
		# self.username = username
		# self.email = email
		# self.fname = fname
		# self.lname = lname
		# self.pword = pword
		
	# def check_password(self, password):
		# return check_password_hash(self.pword, password)

	# def is_active(self):
		# return True
		
	# def get_id(self):
		# userid = self.id
		# return userid
		
	# def get(self):
		# return User.query.filter_by(id = self.id).first()
	
	# def is_anonymous(self):
		# if self.id:
			# return False
		# return True
		
	# def is_authenticated(self):
		# return True
	
	# def get_keywords(self):
		# return Search.query.filter_by(user_id=self.id)

	# def get_results(self):
		# q = Results.query.join(Search).filter_by(user_id=self.id)
		# return q
		
# class Results(db.Model):
	# id = db.Column(db.Integer, primary_key=True)
	# search_id = db.Column(db.Integer, db.ForeignKey('search.id'))
	# fundingNumber = db.Column(db.String(80))
	# opportunityTitle = db.Column(db.String(80))
	# Agency = db.Column(db.String(80))
	# openDate = db.Column(db.String(80))
	# attachment = db.Column(db.String(80))
	# link = db.Column(db.String(120))
	# created = db.Column(db.DateTime, default=datetime.datetime.now())
	
	# def __init__(self, search_id, fundingNumber, opportunityTitle, Agency, openDate, CloseDate, attachment, link):
		# self.search_id = search_id
		# self.fundingNumber = fundingNumber
		# self.opportunityTitle = opportunityTitle
		# self.Agency = Agency
		# self.openDate = openDate
		# self.CloseDate = CloseDate
		# self.attachment = attachment
		# self.link = link

# class Search(db.Model):
	# id = db.Column(db.Integer, primary_key=True)
	# keyword = db.Column(db.String(80), unique=False)
	# user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	# results = db.relationship('Results', backref='keyword', lazy='dynamic')
	
	# def __init__(self, keyword, user_id):
		# self.keyword = keyword
		# self.user_id = user_id

		
# def getByUsername(username):
	# return User.query.filter_by(username=username).first()
		
# def getBySearchid(id):
	# return Search.query.filter_by(id=id).first()
		
# def getByUserid(userid):
	# return User.query.filter_by(id=userid).first()
		
# @login_manager.user_loader
# def load_user(userid):
	# return User.query.filter_by(id = userid).first()
		
@app.route('/')
def index():
	return render_template('index.html')

#replace signin
# @app.route('/newsign/', methods = ['GET', 'POST'])
# def newsign():
    # form = LoginForm()
    # return render_template('newsign.html', 
        # title = 'Sign In',
        # form = form)


	
# @login_manager.unauthorized_handler
# def unauthorized():
    # # do stuff
    # return redirect(url_for('index'))


	
def results(request):
	x=1
	return x


@app.route('/info/', methods=['GET', 'POST'])
# @login_required
def info():
	form = infoForm(request.form)
	if request.method == 'POST':
		# new_keyword = Search(request.form['keyword'], session["user_id"])
		# db.session.add(new_keyword)
		# db.session.commit()
		# flash('Thanks for registering')
		return render_template('newwill.html', form = form)
	return render_template('info.html', form = form)
	
	
	
	
@app.route('/newwill/', methods=['GET', 'POST'])
def newwill(form):
	if request.method == 'POST':
		results = calculate(request)
		return render_template('results.html', results = results)
	return render_template('newwill.html', form)
	
	
# @app.route('/newadd/', methods=['GET', 'POST'])
# @login_required
# def newadd():
	# form = SearchForm(request.form)
	# if request.method == 'POST' and form.validate():
		# new_keyword = Search(request.form['keyword'], session["user_id"])
		# db.session.add(new_keyword)
		# db.session.commit()
		# flash('Thanks for registering')
		# return redirect(url_for('index'))
	# return render_template('newadd.html', form = form)

#replace with newadd
# @app.route('/add/', methods=['GET', 'POST'])
# @login_required
# def add():
	# if request.method == 'POST':
		# new_keyword = Search(request.form['keyword'], session["user_id"])
		# db.session.add(new_keyword)
		# db.session.commit()
		
		# return redirect(url_for('index'))
	# return render_template('add.html')

	
	
# @app.route('/delete/<keyword>')
# @login_required
# def delete(keyword):
	# me = getBySearchid(keyword)
	# db.session.delete(me)
	# db.session.commit()
	# return redirect(url_for('index'))
	

# @app.route('/test/')
# # @login_required
# def test():
	# return render_template('test.html')

	
	
# @app.route("/view/")
# @login_required
# def view():
	# me = getByUserid(session["user_id"])
	# testing = 'alphanumeric'
	# keywords = me.get_keywords()
	# return render_template('view.html', checkme = keywords)

	
#add new input from forms
# @app.route('/runit/<keyword>')
# @login_required
# def runit(keyword):
	# me = getBySearchid(keyword)
	# results = Scraper.scrape(me.keyword, ['*'])
	# # print results
	# for rows in results:
		# try:		
			# new_result = Results(search_id = keyword,
						# fundingNumber = rows["fundingNumber"].strip(), 
						# opportunityTitle = rows["opportunityTitle"].strip(),
						# Agency = rows["Agency"].strip(),
						# openDate = rows["openDate"].strip(),
						# CloseDate = rows["closeDate"].strip(),
						# attachment = rows["attachment"].strip(),
						# link = "http://www.grants.gov/"+rows["link"].strip()
						# )
			# db.session.add(new_result)
			# db.session.commit()
		# except Exception:
			# print 'goddamnit'
			# raise
	# return redirect(url_for('view'))
	
	
#switch out with newsign
# @app.route('/signin/', methods=['GET', 'POST'])
# def signin():
	# if request.method == 'POST':
		# while True:
			# try:
				# me = getByUsername(request.form['username'])
				# if	me.check_password(request.form['password']):
					# login_user(me)
					# flash('You were successfully logged in')
					# return redirect(url_for('index'))
				# return 'wa wa'
			# except AttributeError:
				# return redirect(url_for('index'))
	# return render_template('signin.html')

# @app.route("/logout")
# @login_required
# def logout():
    # logout_user()
    # return redirect(url_for('index'))	

# @app.route("/results")
# @login_required
# def results():	
	# me = getByUserid(session["user_id"])
	# results = me.get_results()
	# return render_template('results.html', results = results)
	
# @app.route('/register/', methods=['GET', 'POST'])
# def register():
	# if request.method == 'POST':
		# userpass = generate_password_hash(request.form['password'])
		# new_user = User(fname = request.form['name'], 
						# lname = request.form['surname'],
						# email = request.form['email'],
						# username = request.form['username'],
						# pword = userpass)
		# db.session.add(new_user)
		# db.session.commit()
		# return redirect(url_for('index'))
	# return render_template('register.html')

if __name__ == '__main__':
	app.run(debug = True, host='0.0.0.0', port=81)
	# app.run(debug = True)