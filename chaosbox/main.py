from flask import Flask
from flask import render_template

app = Flask("chaosbox")

@app.route('/')
def home():
	return render_template('index.html', name="Fabio")

@app.route('/detail/box')
def boxDetails():
	return render_template('boxDetail.html', box_id="123456789")

@app.route('/detail/item')
def itemDetails():
	return render_template('itemDetail.html', box_id="123456789")

@app.route('/create/box')
def createBox():
	return render_template('createBox.html')

@app.route('/create/item')
def createItem():
	return render_template('createItem.html')



'''@app.route("/test")
def test():
	return render_template('test.html', name="Fabio")'''

if __name__ == "__main__":
	app.run(debug=True, port=5000)