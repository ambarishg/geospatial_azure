# Change these four parameters as needed for your own environment
AKS_PERS_STORAGE_ACCOUNT_NAME=stggeo
AKS_PERS_RESOURCE_GROUP=geogroup
AKS_PERS_LOCATION=eastus
AKS_PERS_SHARE_NAME=aksshare

# Create a Resource Group          
az group create --location $AKS_PERS_LOCATION --resource-group $AKS_PERS_RESOURCE_GROUP 


# Create a storage account
az storage account create -n $AKS_PERS_STORAGE_ACCOUNT_NAME -g $AKS_PERS_RESOURCE_GROUP -l $AKS_PERS_LOCATION --sku Standard_LRS

# Export the connection string as an environment variable, this is used when creating the Azure file share
export AZURE_STORAGE_CONNECTION_STRING=$(az storage account show-connection-string -n $AKS_PERS_STORAGE_ACCOUNT_NAME -g $AKS_PERS_RESOURCE_GROUP -o tsv)

# Create the file share
az storage share create -n $AKS_PERS_SHARE_NAME --connection-string $AZURE_STORAGE_CONNECTION_STRING

# Get storage account key
STORAGE_KEY=$(az storage account keys list --resource-group $AKS_PERS_RESOURCE_GROUP --account-name $AKS_PERS_STORAGE_ACCOUNT_NAME --query "[0].value" -o tsv)

# Echo storage account name and key
echo Storage account name: $AKS_PERS_STORAGE_ACCOUNT_NAME
echo Storage account key: $STORAGE_KEY

##############################################################

# Put files in AZURE FILE SHARE 

##################################################################

# Build the docker image        
docker build -t geo .   

# Run Docker     
docker run -p 8501:8501 geo

# Login into the Azure Container Registry    
docker tag geo:latest geoambarishacr.azurecr.io/geo:v2 

# Create a Azure Container Registry    
az acr create --resource-group $AKS_PERS_RESOURCE_GROUP  --name geoambarishacr --sku Basic 

# Login into the Azure Container Registry     
az acr login -n geoambarishacr   


# Push image into Azure Container Registry  
docker push geoambarishacr.azurecr.io/geo:v2

# Update the  Azure Container Registry 
az acr update -n geoambarishacr --admin-enabled true       

# Create AKS cluster
az aks create \
    --resource-group $AKS_PERS_RESOURCE_GROUP \
    --name geoCluster \
    --node-count 1 \
    --generate-ssh-keys \
    --attach-acr geoambarishacr

# Get AKS cluster credentials
az aks get-credentials --resource-group $AKS_PERS_RESOURCE_GROUP --name geoCluster

kubectl create secret generic azure-secret --from-literal=azurestorageaccountname=$AKS_PERS_STORAGE_ACCOUNT_NAME  --from-literal=azurestorageaccountkey=$STORAGE_KEY

# Creating the Persistent Volume and Persistent Volume Claim   
kubectl apply -f pv.yaml

# Create pods and service 
kubectl apply -f geo-pv.yaml


# Cleanup ( Run in Console)   
az group delete --resource-group $AKS_PERS_RESOURCE_GROUP 



