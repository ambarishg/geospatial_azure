import streamlit as st
import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np  

from config import vars_shapefile,vars_shapefile_assembly, \
vars_book,vars_indicators,vars_state,vars_analysis_level

from config import GEOSPATIAL_FILE_PATH


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
   

def get_socio_economic_data ():

    analysis_level, pc, ac, district, page_category='', '', '', '', ''

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

        plot_locations = plot_locations.to_crs(epsg='4326')
        pc_assembly = pc_assembly.to_crs(epsg='4326')
        mx = plot_locations.overlay(pc_assembly,how="intersection")
    elif(analysis_level == 'Assembly'):
        assembly_data = get_assembly_data(state)

        ac_all = assembly_data["ac_name"].unique()
        ac_all = np.sort(ac_all)

        ac = st.sidebar.selectbox("Choose the Assembly Constituency",
                    ac_all)    
        ac_assembly = assembly_data[assembly_data.ac_name == ac]

        plot_locations = plot_locations.to_crs(epsg='4326')
        ac_assembly = ac_assembly.to_crs(epsg='4326')
        mx = plot_locations.overlay(ac_assembly,how="intersection")

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

    df = mx[["NAME",choice]].sort_values(by=[choice],ascending = False)

    st.dataframe(df.head(10),use_container_width = True)

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

    set_summary_stats_label(analysis_level, pc, ac, district, page_category)


    st.write("Median  :" + str(df[choice].median()))
    st.write("Maximum  :" + str(df[choice].max()))
    st.write("Minimum  :" + str(df[choice].min()))
    st.write("Standard Deviation  :" + str(df[choice].std()))

    set_maps_label(analysis_level, pc, ac, district, page_category)

    ax.set_axis_off()
    plt.savefig('Choice.png')

    st.image('Choice.png',width=800)

    m=mx.explore()

    st.components.v1.html(m._repr_html_(),height=800,width=800)








