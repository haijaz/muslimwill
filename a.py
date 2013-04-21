from flask import Flask, request
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
from flask.ext.mako import MakoTemplates, render_template
from flask.ext.wtf import Form, TextField, BooleanField, PasswordField, SelectMultipleField, SelectField, validators, Required

app = Flask(__name__)
mako = MakoTemplates(app)
app.secret_key = 'aas8df98wf298r2#@#$ASDF'

#[find]forms
#
#
#
class infoForm(Form):
	fName= TextField('fName')
	lName= TextField('lName')
	numBoys = TextField('numBoys')
	numGirls= TextField('numGirls')	

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