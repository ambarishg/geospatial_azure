# Overview                 

## Problem    

**Socio Economic** Data  can be used by policy makers of the country to guide the administration for proper functioning of the country. Unfortunately the data is distributed in various formats such as shapefiles , tabular format. Insights and proper decision making is difficult since the data is not consolidated. The data is also not available to the decision makers in the format they can utilize   

## Solution / Idea 
The solution would be to develop the **SocioEconomic Hub** for India.  
The socio economic data would be consolidated with geospatial data as well as tabular data. The data would be cleaned and accurate. 
The data would be presented to the decision makers in the format they can utilize           

# Current Implementation    

This project shows the **socio economic** data of Indian States. The data presently shown are 
* Scheduled Tribes,              
* Scheduled Caste,          
* Literacy,           
* Government Canal,          
* Private Canal,          
* Tank Irrigation,         
* River Irrigation,          
* Lake Irrigation,          
* Total Irrigation,          
* Number of Primary School,        
* Number of Middle School,           
* Number of Secondary School,        
* Number of Senior Secondary School,      
* Number of College, Number of Industrial School,       
* Number of Training School,           
* Number of Adult literacy Class/Centre        
       

The socio economic indicators are presently shown for  
*  Assam     
*  West Bengal   
*  Uttar Pradesh    
*  Union Territories              

This can be **easily extended** for other `socio economic indicators and other Indian States`
    
The indicators are shown in the Village level for the following levels     
*   District    
*   Parliamentary Constituency   
*   Assembly Constituency         

# Technology      

Primary technologies used for development is   
* Python 
* Streamlit  

Main libraries used are GeoPandas for geospatial analysis and Folium     

## Deployment        
Deployment is done using **Microsoft Azure** using the following technologies     

* Azure File Share for storing the shapefiles    
* Docker for building the container image   
* Azure Kubernetes Service for the actual deployment        

# Key Implementation Steps for the Full Solution   

The `present solution` considers the following states    
*  Assam     
*  West Bengal   
*  Uttar Pradesh    
*  Union Territories     

The `present solution` considers 16 Socio Economic Indicators.    

The **future solution** would be extended to    
*  All States and Union Territories of India   
*  Other Socio Economic Indicators [ There are 200 of them ]      

The `present solution`  is scalable , reliable . It uses `Azure File Share` as the repository for data.   


The **future solution** would use the concept of **GeoLakeHouse** and use **Azure DataBricks**  and **Apache Sedona(Geospark)** for better performance   


