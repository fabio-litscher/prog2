"""
the boxes lib is the helper lib whih handles any interactions/manipulations with boxes
"""

def add_new_box(boxes, box_id, box_name, box_description):
    """
    Adds an item to a box

    Args:
        boxes (dict): all warehouse data
        box_id (str): ID of box to create (timestamp in ms)
        box_name (str): property name of box
        box_description (str): property description of box

    Returns:
        boxes (dict): A dictionary containing all the warehouse data including the new created box
    """
    boxes[box_id] = {
        'box_name': box_name,
        'box_description': box_description,
        'box_items': {}
    }
    return boxes


def update_box(boxes, box_id, box_name, box_description):
    """
    Update an existing box

    Args:
        boxes (dict): all warehouse data
        box_id (str): ID of box to update
        box_name (str): property name of box
        box_description (str): property description of box

    Returns:
        boxes (dict): A dictionary containing all the warehouse data including the updated box
    """
    boxes[box_id]['box_name'] = box_name
    boxes[box_id]['box_description'] = box_description
    return boxes


def delete_box(boxes, box_id):
    """
    Delete an existing box

    Args:
        boxes (dict): all warehouse data
        box_id (str): ID of relevant box which should be deleted

    Returns:
        boxes (dict): A dictionary containing all the warehouse data
    """
    boxes.pop(box_id)
    return boxes
