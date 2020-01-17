"""
the items lib is the helper lib whih handles any interactions/manipulations with items
"""

def add_item(boxes, box_id, item_name, item_description, item_quantity):
    """
    Adds an item to a box

    Args:
        boxes (dict): all warehouse data
        box_id (str): ID of relevant box in which the item will be added
        item_name (str): property name of item
        item_description (str): property description of item
        item_quantity (str): property quantity of item

    Returns:
        boxes (dict): A dictionary containing all the warehouse data including the new created item
    """
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
    """
    Update an existing item

    Args:
        boxes (dict): all warehouse data
        box_id (str): ID of relevant box in which the item is
        item_id (str): ID of relevant item which should be updated
        item_name (str): property name of item
        item_description (str): property description of item
        item_quantity (str): property quantity of item

    Returns:
        boxes (dict): A dictionary containing all the warehouse data including the updated item
    """
    boxes[box_id]['box_items'][item_id] = {
        'item_name': item_name,
        'item_description': item_description,
        'item_quantity': item_quantity
    }

    return boxes


def delete_item(boxes, box_id, item_id):
    """
    Delete an item of a box

    Args:
        boxes (dict): all warehouse data
        box_id (str): ID of relevant box in which the item is
        item_id (str): ID of relevant item which should be deleted

    Returns:
        boxes (dict): A dictionary containing all the warehouse data
    """
    boxes[box_id]['box_items'].pop(item_id)
    return boxes
