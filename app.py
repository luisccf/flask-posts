from flask import Flask

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
	return "Welcome!"

if __name__ == '__main__':
	app.run(debug=True, use_reloader=True)