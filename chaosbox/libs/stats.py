def calc_stats(boxes):
    count_boxes = len(boxes)
    count_items = 0

    for box in boxes:
        for item in boxes[box]['box_items']:
            count_items = count_items + 1

    stats = {
        'Anzahl Boxen': count_boxes,
        'Anzahl Items': count_items,
        'Durchsch. Items pro Box': round(count_items/count_boxes, 2)
    }

    return stats