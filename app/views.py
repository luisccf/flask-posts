from flask import render_template, url_for
from app import app

@app.route('/')
@app.route('/index')
def index():
	return render_template('index.html')

@app.route('/add', methods=['GET', 'POST'])
def add():
	if request.method == 'POST':
		news.insert(request.form.to_dict())
		return render_template('success.html')
	return render_template('add.html')