# maps

import geopandas as gpd
import folium
from shapely.geometry import MultiPolygon, Polygon


def create_marker_map(dataframe, latitude_col, longitude_col, destination_col, icon_list, color_list):
    dataframe = dataframe.set_crs('EPSG:4326')

    df_with_markers = dataframe.copy()
    df_with_markers['icon'] = icon_list
    df_with_markers['color'] = color_list

    mapit = folium.Map(location=[dataframe[latitude_col].mean(), dataframe[longitude_col].mean()], zoom_start=12, tiles="Stamen Toner")
    folium.TileLayer('Stamen Terrain').add_to(mapit)
    folium.TileLayer('Stamen Toner').add_to(mapit)
    folium.TileLayer('Stamen Water Color').add_to(mapit)
    folium.TileLayer('cartodbpositron').add_to(mapit)
    folium.TileLayer('cartodbdark_matter').add_to(mapit)
    folium.LayerControl().add_to(mapit)
    
    for row in df_with_markers.itertuples():
        folium.Marker(location=[getattr(row, latitude_col), getattr(row, longitude_col)],
                      popup=getattr(row, destination_col),
                      icon=folium.Icon(icon=f"glyphicon-{getattr(row, 'icon')}", color=getattr(row, 'color'))).add_to(mapit)

    return mapit


def create_custom_map(dataframe, location, zoom_start=12, polygon_style=None, tile_layers=None, markers=None):
    # Create a Folium map centered on the specified location
    mapit = folium.Map(location=location, zoom_start=zoom_start)

    # Add polygon layers if provided
    if polygon_style:
        for geom in dataframe.geometry:
            if isinstance(geom, MultiPolygon) or isinstance(geom, Polygon):
                folium.GeoJson(geom, style_function=lambda x: polygon_style).add_to(mapit)

    # Add tile layers if provided
    if tile_layers:
        for tile_layer in tile_layers:
            folium.TileLayer(tile_layer).add_to(mapit)

    # Add markers if provided
    if markers:
        for marker in markers:
            folium.Marker(location=marker[0], icon=folium.Icon(**marker[1])).add_to(mapit)

    return mapit