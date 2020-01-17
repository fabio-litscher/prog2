"""
main.py from the chaosbox webapp
all routes are handled in here

Attributes:
    app (flask.app.Flask): my app
    app_main_path (str): main path of project, coming from os
    data_path (str): path to the data folder which contains the JSON file
    data_storage_file (str): complete path to the json file - data_path + filename
"""

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


# initialize boxes
boxes = {}

# get dummy data for testing
# boxes = data_lib.create_dummy_data_lib()


@app.route('/')
def home():
    """
    Route for the home page where the box overview and statistics are shown

    Returns:
        render_template: renders the index.html template with the boxes and statistics
    """
    boxes = data_lib.load_json(data_storage_file)
    statistics = stats_lib.calc_stats(boxes)
    return render_template('index.html', boxes=boxes, statistics=statistics)


@app.route('/box', methods=['GET', 'POST'])
@app.route('/box/<box_id>', methods=['GET', 'POST'])
@app.route('/box/<box_id>/<edit_box>', methods=['GET', 'POST'])
def box(box_id=None, edit_box=None):
    """
    Route for the box page which handles anything about boxes, following situations
        (1): handling post request from adding or edit a box
        (2): handling the edit box reuest
        (3): showing box details
        (4): showing form to add new box

    Args:
        box_id (str): box_id for edit or show details
        edit_box (str): to know if edit button pressed

    Returns:
        (1) render_template: renders box.html template with box data to show details
        (2) render_template/redirect: renders box.html template with details or redirects to home if a wrong param (box_id is given) 
        (3) render_template/redirect: renders box.html template with details or redirects to home if a wrong param (box_id is given) 
        (4) render_template: renders box.html template without any data - empty form is shown
    """
    boxes = data_lib.load_json(data_storage_file)

    # (1): handling post request from adding a new box or edit
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

    # (2): handling the edit box reuest
    if edit_box == "edit":
        try:
            box = boxes[box_id]
            return render_template('box.html', edit_box_id=box_id, box=box)
        except():
            return redirect(url_for('home'))

    # (3): showing box details
    if box_id:
        try:
            box = boxes[box_id]
            return render_template('box.html', box_id=box_id, box=box)
        except():
            return redirect(url_for('home'))

    # (4): showing form to add new box
    return render_template('box.html')


@app.route('/box/delete/<box_id>', methods=['GET', 'POST'])
def delete_box(box_id=None):
    """
    Route to delete an existing box
        (1): handle post request to delete box when clicked on yes on the 'are you sure you want to delete this box' page
        (2): show the 'are you sure you want to delete this box' page

    Args:
        box_id (str): ID of the box to delete

    Returns:
        (1) redirect: redirect to home page with the overview of boxes after box is deleted
        (2) render_template: render delete_box.html template to ask if they are sure to delete the box with all the items (with all the box informations to display)
    """
    boxes = data_lib.load_json(data_storage_file)

    # (1): handle post request to delete box when clicked on yes on the 'are you sure you want to delete this box' page
    if request.method == 'POST':
        boxes = box_lib.delete_box(boxes, box_id)

        data_lib.save_json(data_storage_file, boxes)

        return redirect(url_for('home'))

    # (2): show the 'are you sure you want to delete this box' page
    if box_id:
        box = boxes[box_id]
        return render_template('delete_box.html', box_id=box_id, box=box)

    return render_template('index.html')


@app.route('/box/<box_id>/item', methods=['GET', 'POST'])
@app.route('/box/<box_id>/item/<item_id>', methods=['GET', 'POST'])
@app.route('/box/<box_id>/item/<item_id>/<edit_item>', methods=['GET', 'POST'])
def item(box_id=None, item_id=None, edit_item=None):
    """
    Route for the box page which handles anything about items, following situations
        (1): handling post request from adding or edit a item
        (2): handling the edit item reuest
        (3): showing item details
        (4): showing form to add new item

    Args:
        box_id (str): box_id in which the item is
        item_id (str): id of the item
        edit_item (str): to know if edit button pressed

    Returns:
        (1) redirect: redirects to specific box overview in which the new or updated item is
        (2) render_template/redirect: renders item.html template with details or redirects to home if a wrong param (box_id or item_id) 
        (3) render_template: renders item.html template with details of item
        (4) render_template: renders item.html template without any data - empty form is shown
    """
    boxes = data_lib.load_json(data_storage_file)

    # (1): handling post request from adding or edit a item
    if request.method == 'POST':
        item_name = request.form['item_name']
        item_description = request.form['item_description']
        item_quantity = request.form['item_quantity']

        # when edit
        if 'item_id' in request.form:
            item_id = request.form['item_id']
            boxes = item_lib.update_item(boxes, box_id, item_id, item_name, item_description, item_quantity)

        # else new item
        else:
            boxes = item_lib.add_item(
                boxes, box_id, item_name, item_description, item_quantity)

        data_lib.save_json(data_storage_file, boxes)

        return redirect(url_for('box', box_id=box_id))

    # (2): handling the edit item reuest
    if edit_item == "edit":
        try:
            item = boxes[box_id]['box_items'][item_id]
            return render_template('item.html', box_id=box_id, edit_item_id=item_id, item=item)
        except():
            return redirect(url_for('home'))

    # (3): showing item details
    if item_id:
        item = boxes[box_id]['box_items'][item_id]

        return render_template('item.html', box_id=box_id, item_id=item_id, item=item)

    # (4): showing form to add new item
    return render_template('item.html', box_id=box_id)


@app.route('/box/delete/<box_id>/<item_id>', methods=['GET', 'POST'])
def delete_item(box_id=None, item_id=None):
    """
    Route to delete an existing item
        (1): handle post request to delete item when clicked on yes on the 'are you sure you want to delete this item' page
        (2): show the 'are you sure you want to delete this item' page

    Args:
        box_id (str): ID of the box in which the item to delete is
        item_id (str): ID of the item to delete

    Returns:
        (1) redirect: redirect to box detail page with the overview of all items of the box
        (2) render_template: render delete_item.html template to ask if they are sure to delete the item (with all the item informations to display)
    """
    boxes = data_lib.load_json(data_storage_file)

    # (1): handle post request to delete item when clicked on yes on the 'are you sure you want to delete this item' page
    if request.method == 'POST':
        boxes = item_lib.delete_item(boxes, box_id, item_id)

        data_lib.save_json(data_storage_file, boxes)

        return redirect(url_for('box', box_id=box_id))

    # (2): show the 'are you sure you want to delete this item' page
    if box_id and item_id:
        item = boxes[box_id]['box_items'][item_id]
        return render_template('delete_item.html', box_id=box_id, item_id=item_id, item=item)

    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True, port=5000)
