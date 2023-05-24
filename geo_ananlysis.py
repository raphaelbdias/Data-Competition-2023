import geopandas as gpd
from shapely.geometry import Point, Polygon


# function to check if a point is inside a polygon and return the corresponding WARD value
def is_point_inside_polygon(point, polygons):
    for polygon in polygons:
        if point.within(polygon):
            return row['WARD']
    return False
