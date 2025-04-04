def get_center_of_bbox(bbox):
    """
    Calculate the center of a bounding box.

    Args:
        bbox (list or tuple): Bounding box coordinates in the format [x1, y1, x2, y2].

    Returns:
        tuple: Center coordinates (cx, cy).
    """
    x1, y1, x2, y2 = bbox
    cx = (x1 + x2) / 2
    cy = (y1 + y2) / 2
    return cx, cy

def get_bbox_area(bbox):
    return bbox[2]-bbox[0]