import os
from pathlib import Path
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
# from collections import OrderedDict
import time
from libs import data

app = Flask("chaosbox")
app_main_path = Path(os.path.abspath(
    "/".join(os.path.realpath(__file__).split("/")[:-1])))
#data_path = Path(os.path.abspath(app_main_path / ".." / "data"))
data_path = Path(os.path.abspath(app_main_path / "data"))
# app.secret_key = 'the random string'
data_storage_file = data_path / "chaosbox.json"


# initialize boxes
boxes = {}

# get dummy data
boxes = data.load_json(data_storage_file)
#boxes = data.create_dummy_data()


@app.route('/')
def home():
    return render_template('index.html', boxes=boxes)


@app.route('/box', methods=['GET', 'POST'])
@app.route('/box/<box_id>', methods=['GET', 'POST'])
@app.route('/box/<box_id>/<edit_box>', methods=['GET', 'POST'])
def box(box_id=None, edit_box=None):
    if request.method == 'POST':
        box_name = request.form['box_name']
        box_description = request.form['box_description']

        # when editbox set box_id ootherwise create new from timestamp in ms
        if request.form['box_id']:
            box_id = request.form['box_id']
            boxes[box_id]['box_name'] = box_name
            boxes[box_id]['box_description'] = box_description
        else:
            box_id = str(int(round(time.time() * 1000)))
            boxes[box_id] = {
                'box_name': box_name,
                'box_description': box_description,
                'box_items': {}
            }

        data.save_json(data_storage_file, boxes)

        box = boxes[box_id]
        return render_template('box.html', box_id=box_id, box=box)

    if edit_box == "edit":
        try:
            box = boxes[box_id]
            return render_template('box.html', edit_box_id=box_id, box=box)
        except:
            return redirect(url_for('home'))

    # show details
    if box_id:
        try:
            box = boxes[box_id]
            return render_template('box.html', box_id=box_id, box=box)
        except:
            return redirect(url_for('home'))

    return render_template('box.html')


@app.route('/box/delete/<box_id>', methods=['GET', 'POST'])
def delete_box(box_id=None):
    if request.method == 'POST':
        boxes.pop(box_id, None)

        data.save_json(data_storage_file, boxes)

        return redirect(url_for('home'))

    # show details
    if box_id:
        box = boxes[box_id]
        return render_template('delete_box.html', box_id=box_id, box=box)

    return render_template('index.html')


@app.route('/box/<box_id>/item', methods=['GET', 'POST'])
@app.route('/box/<box_id>/item/<item_id>', methods=['GET', 'POST'])
def item(box_id=None, item_id=None):
    # post request from adding new item
    if request.method == 'POST':
        # add box to boxes
        key_list = list(boxes[box_id]['box_items'].keys())
        if len(key_list) != 0:
            next_key = str(int(key_list[-1]) + 1)
        else:
            next_key = '0'

        item_name = request.form['item_name']
        item_description = request.form['item_description']
        item_quantity = request.form['item_quantity']
        boxes[box_id]['box_items'][next_key] = {
            'item_name': item_name,
            'item_description': item_description,
            'item_quantity': item_quantity
        }

        data.save_json(data_storage_file, boxes)

        return redirect(url_for('box', box_id=box_id))

    # show existing item
    if item_id:
        item = boxes[box_id]['box_items'][item_id]

        return render_template('item.html', box_id=box_id, item_id=item_id, item=item)

    # when going to create a new item (empty item page)
    return render_template('item.html', box_id=box_id)


@app.route('/box/delete/<box_id>/<item_id>', methods=['GET', 'POST'])
def delete_item(box_id=None, item_id=None):
    if request.method == 'POST':
        boxes[box_id]['box_items'].pop(item_id, None)

        data.save_json(data_storage_file, boxes)

        return redirect(url_for('box', box_id=box_id))

    # show details
    if box_id and item_id:
        item = boxes[box_id]['box_items'][item_id]
        return render_template('delete_item.html', box_id=box_id, item_id=item_id, item=item)

    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True, port=5000)
