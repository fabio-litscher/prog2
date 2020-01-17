"""
data.py is a lib which helps to handle all interactions with the json file (read/write)
furthermore it has a function to create dummy data which was used at the beginning of the project
"""
import json


def load_json(json_path):
    """
    Loads all the warehouse data from the json file

    Args:
        json_path (str): path to the json file
    Returns:
        dict: A dictionary containing the warehouse data. Returns an empty structure if file not found
    """
    try:
        with open(json_path) as open_file:
            boxes = json.load(open_file)
    except FileNotFoundError:
        boxes = {}

    return boxes


def save_json(json_path, data):
    """
    Writes all the warehouse data from into the json file

    Args:
        json_path (str): path to the json file
        data (dict): dict with all the warehouse data to write into the file
    """
    with open(json_path, "w+", encoding="utf-8") as open_file:
        json.dump(data, open_file, indent=4)


def create_dummy_data():
    """
    Creates dict with dummy warehouse data including boxes and items

    Returns:
        dict: A dictionary with dummy warehouse data in the same structure as prod data would be
    """
    boxes = {
        '0': {
            'box_name': 'Testbox 1',
            'box_description': 'Dies ist die erste Testbox.',
            'box_items': {
                '0': {
                    'item_name': 'erstes Item',
                    'item_description': 'beschreibung des ersten items',
                    'item_quantity': 200
                },
                '1': {
                    'item_name': 'zweites Item',
                    'item_description': 'beschreibung des zweiten items',
                    'item_quantity': 10
                }
            }
        },
        '1': {
            'box_name': 'Testbox 1',
            'box_description': 'Dies ist die erste Testbox.',
            'box_items': {
                '0': {
                    'item_name': 'drittes Item',
                    'item_description': 'beschreibung des dritten items',
                    'item_quantity': 200
                },
                '1': {
                    'item_name': 'viertes Item',
                    'item_description': 'beschreibung des vierten items',
                    'item_quantity': 10
                }
            }
        }
    }
    return boxes
