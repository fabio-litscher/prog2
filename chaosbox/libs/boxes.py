def add_new_box(boxes, box_id, box_name, box_description):
    boxes[box_id] = {
        'box_name': box_name,
        'box_description': box_description,
        'box_items': {}
    }
    return boxes


def update_box(boxes, box_id, box_name, box_description):
    boxes[box_id]['box_name'] = box_name
    boxes[box_id]['box_description'] = box_description
    return boxes
