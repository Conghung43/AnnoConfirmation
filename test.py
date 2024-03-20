from shapely.geometry import Polygon

def merge_overlapping_polygons(pl1, pl2):
    # Create Shapely Polygon objects from the lists of points
    polygon1 = Polygon(pl1)
    polygon2 = Polygon(pl2)
    
    # Check if the two polygons intersect
    if polygon1.intersects(polygon2):
        # If they intersect, perform a union operation to merge them
        merged_polygon = polygon1.union(polygon2)
        # Extract the coordinates of the merged polygon
        merged_coords = list(merged_polygon.exterior.coords)
        # Remove the last coordinate, which is a duplicate of the first one
        merged_coords.pop()
        return merged_coords
    else:
        # If they don't intersect, return None
        return None

# Test the function with the provided polygons
pl1 = [(0, 0), (0, 0.4), (0.4, 0.4), (0.4, 0)]
pl2 = [(0.3, 0), (0, 0.4), (0.8, 4), (0.8, 0)]

merged_polygon = merge_overlapping_polygons(pl1, pl2)
if merged_polygon:
    print("Merged polygon:", merged_polygon)
else:
    print("The polygons do not overlap.")
