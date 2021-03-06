"""
stats.py is the lib in which everything regarding statistic calculation is handled
next step would be to save the stats into a separate json file and create a history which could be visualized
"""

def calc_stats(boxes):
    """
    Calculates the relevant statistics for the dashboard

    Args:
        boxes (dict): all warehouse data to calc the stats

    Returns:
        stats (dict): All the stats in a dict which is ready to be shown
    """
    count_boxes = len(boxes)
    count_items = 0
    max_items = 0
    max_items_box = ""

    if count_boxes > 0:
        for box in boxes:
            if len(boxes[box]['box_items']) > max_items:
                max_items = len(boxes[box]['box_items'])
                max_items_box = "<a href='./box/" + box + "'>" + boxes[box]['box_name'] + "</a> mit " + str(max_items) + " items"
            elif len(boxes[box]['box_items']) == max_items:
                max_items_box += ", <a href='./box/" + box + "'>" + boxes[box]['box_name'] + "</a> mit " + str(max_items) + " items"

            for item in boxes[box]['box_items']:
                count_items = count_items + 1

        stats = {
            'Anzahl Boxen': count_boxes,
            'Anzahl Items': count_items,
            'Durchschnittliche Items pro Box': round(count_items / count_boxes, 2),
            'Box(en) mit den meisten Items': max_items_box
        }

    else:
        stats = {
            'Anzahl Boxen': "-",
            'Anzahl Items': "-",
            'Durchschnittliche Items pro Box': "-",
            'Box(en) mit den meisten Items': "-"
        }

    return stats
