import geopandas as gpd
import streamlit as st
import matplotlib.pyplot as plt


SHAPE_FILE_ROADS = 'gis_osm_roads_free_1.shp'

def get_roads_data():

    @st.cache(allow_output_mutation=True)
    def read_data():
        plot_locations = gpd.read_file(SHAPE_FILE_ROADS)
        return plot_locations

    plot_locations = read_data()    
    m = plot_locations[plot_locations.name == "Vidyasagar Setu"].explore()
    st.components.v1.html(m._repr_html_(),height=800,width=800)
