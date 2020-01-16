import os
from pathlib import Path
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
# from collections import OrderedDict
import time
from libs import data as data_lib
from libs import stats as stats_lib
from libs import boxes as box_lib
from libs import items as item_lib


app = Flask("chaosbox")
app_main_path = Path(os.path.abspath(
    "/".join(os.path.realpath(__file__).split("/")[:-1])))
data_path = Path(os.path.abspath(app_main_path / "data"))
data_storage_file = data_path / "chaosbox_boxes.json"
# stats_lib_storage_file = data_lib_path / "chaosbox_stats_lib.json"


# initialize boxes
boxes = {}

# get dummy data_lib
# boxes = data_lib.load_json(data_storage_file)
# boxes = data_lib.create_dummy_data_lib()


@app.route('/')
def home():
    boxes = data_lib.load_json(data_storage_file)
    statistics = stats_lib.calc_stats(boxes)
    return render_template('index.html', boxes=boxes, statistics=statistics)


@app.route('/box', methods=['GET', 'POST'])
@app.route('/box/<box_id>', methods=['GET', 'POST'])
@app.route('/box/<box_id>/<edit_box>', methods=['GET', 'POST'])
def box(box_id=None, edit_box=None):
    boxes = data_lib.load_json(data_storage_file)

    if request.method == 'POST':
        box_name = request.form['box_name']
        box_description = request.form['box_description']

        # when editbox set box_id otherwise create new from timestamp in ms
        if 'box_id' in request.form:
            box_id = request.form['box_id']
            boxes = box_lib.update_box(
                boxes, box_id, box_name, box_description)
        else:
            box_id = str(int(round(time.time() * 1000)))
            boxes = box_lib.add_new_box(
                boxes, box_id, box_name, box_description)

        data_lib.save_json(data_storage_file, boxes)

        box = boxes[box_id]
        return render_template('box.html', box_id=box_id, box=box)

    # edit box
    if edit_box == "edit":
        try:
            box = boxes[box_id]
            return render_template('box.html', edit_box_id=box_id, box=box)
        except():
            return redirect(url_for('home'))

    # show details
    if box_id:
        try:
            box = boxes[box_id]
            return render_template('box.html', box_id=box_id, box=box)
        except():
            return redirect(url_for('home'))

    return render_template('box.html')


@app.route('/box/delete/<box_id>', methods=['GET', 'POST'])
def delete_box(box_id=None):
    boxes = data_lib.load_json(data_storage_file)

    if request.method == 'POST':
        boxes = box_lib.delete_box(boxes, box_id)

        data_lib.save_json(data_storage_file, boxes)

        return redirect(url_for('home'))

    # show details
    if box_id:
        box = boxes[box_id]
        return render_template('delete_box.html', box_id=box_id, box=box)

    return render_template('index.html')


@app.route('/box/<box_id>/item', methods=['GET', 'POST'])
@app.route('/box/<box_id>/item/<item_id>', methods=['GET', 'POST'])
@app.route('/box/<box_id>/item/<item_id>/<edit_item>', methods=['GET', 'POST'])
def item(box_id=None, item_id=None, edit_item=None):
    boxes = data_lib.load_json(data_storage_file)

    # post request from adding new item
    if request.method == 'POST':
        item_name = request.form['item_name']
        item_description = request.form['item_description']
        item_quantity = request.form['item_quantity']

        # when editbox set box_id ootherwise create new from timestamp in ms
        if 'item_id' in request.form:
            item_id = request.form['item_id']
            boxes[box_id]['box_items'][item_id] = {
                'item_name': item_name,
                'item_description': item_description,
                'item_quantity': item_quantity
            }
        else:
            key_list = list(boxes[box_id]['box_items'].keys())
            if len(key_list) != 0:
                next_key = str(int(key_list[-1]) + 1)
            else:
                next_key = '0'

            boxes[box_id]['box_items'][next_key] = {
                'item_name': item_name,
                'item_description': item_description,
                'item_quantity': item_quantity
            }

        """item_name = request.form['item_name']
        item_description = request.form['item_description']
        item_quantity = request.form['item_quantity']"""

        data_lib.save_json(data_storage_file, boxes)

        return redirect(url_for('box', box_id=box_id))

    if edit_item == "edit":
        try:
            item = boxes[box_id]['box_items'][item_id]
            return render_template('item.html', box_id=box_id, edit_item_id=item_id, item=item)
        except():
            return redirect(url_for('home'))

    # show existing item
    if item_id:
        item = boxes[box_id]['box_items'][item_id]

        return render_template('item.html', box_id=box_id, item_id=item_id, item=item)

    # when going to create a new item (empty item page)
    return render_template('item.html', box_id=box_id)


@app.route('/box/delete/<box_id>/<item_id>', methods=['GET', 'POST'])
def delete_item(box_id=None, item_id=None):
    boxes = data_lib.load_json(data_storage_file)
    
    if request.method == 'POST':
        boxes[box_id]['box_items'].pop(item_id)

        data_lib.save_json(data_storage_file, boxes)

        return redirect(url_for('box', box_id=box_id))

    # show details
    if box_id and item_id:
        item = boxes[box_id]['box_items'][item_id]
        return render_template('delete_item.html', box_id=box_id, item_id=item_id, item=item)

    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True, port=5000)
