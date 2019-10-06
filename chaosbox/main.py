from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
import time

app = Flask("chaosbox")

# initialize boxes
boxes = {}

@app.route('/')
def home():
    return render_template('index.html', boxes=boxes)


@app.route('/detail/box')
def boxDetails():
    return render_template('boxDetail.html', box_id="123456789")


@app.route('/detail/item')
def itemDetails():
    return render_template('itemDetail.html', box_id="123456789")


@app.route('/box', methods=['GET', 'POST'])
@app.route('/box/<box_id>', methods=['GET', 'POST'])
def createBox(box_id=None):
    if request.method == 'POST':

        #add box to boxes
    	#set time in ms as box_id
        box_id = str(int(round(time.time() * 1000)))
        box_name = request.form['box_name']
        box_description = request.form['box_description']
        boxes[box_id] = {'box_name': box_name, 'box_description': box_description}

        return redirect(url_for('home'))

    # show details
    if(box_id):
        box = boxes[box_id]
        box_name = boxes[box_id]['box_name']
        box_description = boxes[box_id]['box_description']
        return render_template('createBox.html', box_id=box_id, box=box)

    return render_template('createBox.html')


@app.route('/create/item')
def createItem():
    return render_template('createItem.html')


'''@app.route("/test")
def test():
    return render_template('test.html', name="Fabio")'''

if __name__ == "__main__":
    app.run(debug=True, port=5000)
