import streamlit as st
import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np  

from config import vars_shapefile,vars_shapefile_assembly, \
vars_book,vars_indicators,vars_state,vars_analysis_level, \
vars_map_pop_up

from config import GEOSPATIAL_FILE_PATH

def found_item(choice):
    found = False
    for name in vars_map_pop_up:
        if(name == choice):
            found = True
            break
    return found

def intialize_vars():
    analysis_level, pc, ac, district, page_category='', '', '', '', ''
    return(analysis_level, pc, ac, district, page_category)

def set_analysis_labels(analysis_level, pc, ac, district, page_category, state):
    if(analysis_level == 'Parliament'):
        st.subheader( 
        page_category + " in the parliament constituency " + pc + 
        " in " + state)
    elif(analysis_level == 'Assembly'):
        st.subheader( 
        page_category + " in the assembly constituency " + ac + 
        " in " + state)
    else:
        st.subheader( 
    page_category + " in the district " + str(district) + 
    " in " + state)

def set_summary_stats_label(analysis_level, pc, ac, district, page_category):
    if(analysis_level == 'Parliament'):
        st.subheader("Summary " + page_category + " Statistics of the parliament constituency " + pc)   
    elif(analysis_level == 'Assembly'):
        st.subheader("Summary " + page_category + " Statistics of the assembly constituency " + ac)
    else:
        st.subheader("Summary " + page_category + " Statistics of the district " + str(district))

def set_maps_label(analysis_level, pc, ac, district, page_category):
    if(analysis_level == 'Parliament'):
        st.subheader(page_category + \
            " map of the parliament constituency " + pc)
    elif(analysis_level == 'Assembly'):
        st.subheader(page_category + \
            " map of the assembly constituency " + ac)
    else:
        st.subheader(page_category + \
            " map of the district " + str(district))

@st.cache(allow_output_mutation=True)
def get_state_data(state):
       
        plot_locations = gpd.read_file(GEOSPATIAL_FILE_PATH + vars_shapefile[state])
        return plot_locations

@st.cache(allow_output_mutation=True)
def get_assembly_data(state):
        plot_locations = gpd.read_file(GEOSPATIAL_FILE_PATH + vars_shapefile_assembly[state])
        return plot_locations
   
def find_intersection_shape(x, y):
    x = x.to_crs(epsg='4326')
    y = y.to_crs(epsg='4326')
    mx = x.overlay(y,how="intersection")
    return mx 

def set_summary_stats(choice, df):
    st.write("Median  :" + str(df[choice].median()))
    st.write("Maximum  :" + str(df[choice].max()))
    st.write("Minimum  :" + str(df[choice].min()))
    st.write("Standard Deviation  :" + str(df[choice].std()))

def get_socio_economic_data ():

    analysis_level, pc, ac, district, page_category= intialize_vars()

    state = st.sidebar.selectbox("Choose the State",
                (vars_state))    

    if(state == ''):
        return

    plot_locations = get_state_data(state)

    analysis_level = st.sidebar.selectbox("Choose the Analysis Level",
                (vars_analysis_level))

    if(analysis_level == 'Parliament'):
        assembly_data = get_assembly_data(state)

        pc_all = assembly_data["pc_name"].unique()
        pc_all = np.sort(pc_all)

        pc = st.sidebar.selectbox("Choose the Parliament Constituency",
                    pc_all)    
        pc_assembly = assembly_data[assembly_data.pc_name == pc]

        mx = find_intersection_shape(plot_locations, pc_assembly)
    elif(analysis_level == 'Assembly'):
        assembly_data = get_assembly_data(state)

        ac_all = assembly_data["ac_name"].unique()
        ac_all = np.sort(ac_all)

        ac = st.sidebar.selectbox("Choose the Assembly Constituency",
                    ac_all)    
        ac_assembly = assembly_data[assembly_data.ac_name == ac]

        mx = find_intersection_shape(plot_locations, ac_assembly)

    else:
        district_all = plot_locations["DISTRICT"].unique()
        district_all = np.sort(district_all)
        district = st.sidebar.selectbox("Choose the District",
                (district_all))
        if (district == ''):
            return
        mx = plot_locations[(plot_locations.DISTRICT == district)]

    page_category = st.sidebar.selectbox("Choose the Indicator",
                (vars_indicators))

    if(page_category == ''):
        return

    st.title("Village Level Data for " + state )

    choice = vars_book[page_category]

    set_analysis_labels(analysis_level, pc, ac, district, page_category, state)
    df = mx[["NAME",choice]].sort_values(by=[choice],ascending = False)
    st.dataframe(df.head(10),use_container_width = True)

    
    set_summary_stats_label(analysis_level, pc, ac, district, page_category)
    set_summary_stats(choice, df)

    set_maps_label(analysis_level, pc, ac, district, page_category)
    ax = mx.plot(
    column=choice,  # Data to plot
    figsize=(15, 10),
    scheme="Quantiles",  # Classification scheme
    cmap="Reds",  # Color palette
    edgecolor="k",  # Borderline color
    linewidth=0.1,  # Borderline width
    legend=True,  # Add legend
    legend_kwds={
    "fmt": "{:.0f}"
    },  # Remove decimals in legend (for legibility)
    missing_kwds={
    "color": "lightgrey",
    "edgecolor": "red",
    "hatch": "///",
    "label": "Missing values",}
    )
    ax.set_axis_off()
    plt.savefig(GEOSPATIAL_FILE_PATH + 'Choice.png')
    st.image(GEOSPATIAL_FILE_PATH + 'Choice.png',width=800)
    
    found = found_item(choice)
    if(found == False ):
        vars_map_pop_up.append(choice)
    m=mx.explore(popup=vars_map_pop_up,tooltip=vars_map_pop_up)
    st.components.v1.html(m._repr_html_(),height=800,width=800)

















