from flask import Flask
from flask import render_template

app = Flask("chaosbox")

@app.route('/')
def home():
	return render_template('index.html', name="Fabio")

@app.route('/detail')
def details():
	return render_template('detail.html', box_id="123456789")

'''@app.route("/test")
def test():
	return render_template('test.html', name="Fabio")'''

if __name__ == "__main__":
	app.run(debug=True, port=5000)