def calc_stats(boxes):
    count_boxes = len(boxes)
    count_items = 0
    max_items = 0

    for box in boxes:
        if len(boxes[box]['box_items']) > max_items: max_items = len(boxes[box]['box_items'])
        for item in boxes[box]['box_items']:
            count_items = count_items + 1

    stats = {
        'Anzahl Boxen': count_boxes,
        'Anzahl Items': count_items,
        'Durchschnittliche Items pro Box': round(count_items/count_boxes, 2),
        'Meiste Items in Box': max_items
    }

    return stats