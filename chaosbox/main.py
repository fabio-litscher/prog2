from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
import time
from libs import data

app = Flask("chaosbox")

# initialize boxes
boxes = {}

# get dummy data
boxes = data.create_dummy_data()


@app.route('/')
def home():
    return render_template('index.html', boxes=boxes)


@app.route('/box', methods=['GET', 'POST'])
@app.route('/box/<box_id>', methods=['GET', 'POST'])
def box(box_id=None):
    if request.method == 'POST':

        # add box to boxes
        # set time in ms as box_id
        box_id = str(int(round(time.time() * 1000)))
        box_name = request.form['box_name']
        box_description = request.form['box_description']
        boxes[box_id] = {
            'box_name': box_name,
            'box_description': box_description
        }

        return redirect(url_for('home'))

    # show details
    if(box_id):
        box = boxes[box_id]
        box_name = boxes[box_id]['box_name']
        box_description = boxes[box_id]['box_description']
        return render_template('box.html', box_id=box_id, box=box)

    return render_template('box.html')


@app.route('/item')
@app.route('/item/<origin>')
def item(origin=None):
    return render_template('item.html', origin=origin)


'''@app.route("/test")
def test():
    return render_template('test.html', name="Fabio")'''

if __name__ == "__main__":
    app.run(debug=True, port=5000)
