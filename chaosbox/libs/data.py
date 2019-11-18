import json


def load_json(json_path):
    try:
        with open(json_path) as open_file:
            boxes = json.load(open_file)
    except FileNotFoundError:
        boxes = {}

    return boxes


def save_json(json_path, data):
    with open(json_path, "w+", encoding="utf-8") as open_file:
        json.dump(data, open_file, indent=4)


def create_dummy_data():
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
