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

# utils/bbox_utils.py

def measure_distance(p1, p2):
    # Debugging print statements to inspect the inputs
    # print(f"start_position: {p1}, end_position: {p2}")
    # print(f"Type of start_position: {type(p1)}, Type of end_position: {type(p2)}")
    
    # Ensure both positions are lists with two points
    if isinstance(p1, list) and isinstance(p2, list):
        # Calculate distance for each corresponding pair of points
        total_distance = 0
        for i in range(len(p1)):
            x1, y1 = p1[i]
            x2, y2 = p2[i]
            total_distance += ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
        return total_distance
    else:
        # Return 0 or raise an error if data is not in the expected format
        print(f"Invalid data format: start_position {p1}, end_position {p2}")
        return 0


def get_foot_position(bbox):
    x1,y1,x2,y2 = bbox
    return int((x1+x2)/2),int(y2)
