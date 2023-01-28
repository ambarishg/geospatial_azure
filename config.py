GEOSPATIAL_FILE_PATH ="/mnt/azure/"

vars_analysis_level = ["","Parliament",'Assembly','District']

vars_state = ["","Assam",'West Bengal',
'Union Territories','Uttar Pradesh']

vars_indicators =["","Scheduled Tribes",'Scheduled Caste',
    'Literacy','Government Canal',
    'Private Canal','Tank Irrigation',
    'River Irrigation','Lake Irrigation',
    'Total Irrigation','Number of Primary School',
    'Number of Middle School','Number of Secondary School',
    'Number of Senior Secondary School',
    'Number of College','Number of Industrial School',
    'Number of Training School',
    'Number of Adult literacy Class/Centre']

vars_book = {'Scheduled Tribes': 'P_ST', 
    'Scheduled Caste': 'P_SC', 'Literacy': 'P_LIT',
    'Government Canal':'CANAL_GOVT','Private Canal':'CANAL_PVT',
    'Tank Irrigation':'TANK_IRR','River Irrigation':'RIVER_IRR',
    'Lake Irrigation':'LAKE_IRR','Total Irrigation':'TOT_IRR',
    'Number of Primary School':'P_SCH','Number of Middle School':'M_SCH',
    'Number of Secondary School':'S_SCH','Number of Senior Secondary School':'S_S_SCH',
    'Number of College':'COLLEGE','Number of Industrial School':'IND_SCH',
    'Number of Training School':'TR_SCH','Number of Adult literacy Class/Centre':'ADLT_LT_CT',}
    

vars_shapefile = {'Assam': 'india-village-census-2001-AS.shp',
    'West Bengal': 'india-village-census-2001-WB.shp',
    'Uttar Pradesh': 'india-village-census-2001-UP.shp',
    'Union Territories':'india-village-census-2001-UTerr.shp'}

vars_shapefile_assembly = {'West Bengal': 'westbengal.assembly.shp',
    'Assam': 'assam.assembly.shp',
    'Uttar Pradesh': 'uttarpradesh.assembly.shp',}

vars_map_pop_up = ["NAME"]