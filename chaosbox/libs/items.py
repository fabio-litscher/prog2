def add_item(boxes, box_id, item_name, item_description, item_quantity):
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

    return boxes


def update_item(boxes, box_id, item_id, item_name, item_description, item_quantity):
    boxes[box_id]['box_items'][item_id] = {
        'item_name': item_name,
        'item_description': item_description,
        'item_quantity': item_quantity
    }

    return boxes


def delete_item(boxes, box_id, item_id):
    boxes[box_id]['box_items'].pop(item_id)
    return boxes
