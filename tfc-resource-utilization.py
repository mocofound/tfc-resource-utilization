import requests
import pandas as pd
from datetime import datetime

# Constants
API_URL = "https://app.terraform.io/api/v2"
#TFC_TOKEN from environment modify
# export TFC_TOKEN=mcQWOpWlHH
#TFC_TOKEN = ""

# Headers for authentication
headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/vnd.api+json"
}

def fetch_workspaces():
    """Fetch all workspaces and return a list of their IDs and creation dates."""
    workspaces_url = f"{API_URL}/organizations/{ORGANIZATION}/workspaces"
    response = requests.get(workspaces_url, headers=headers)
    
    if response.status_code != 200:
        print("Failed to fetch workspaces:", response.status_code)
        print("Response:", response.text)
        return []

    workspaces_data = response.json()

    # Check and print the whole JSON response to understand its structure
    print("JSON Response:", workspaces_data)

    # Assuming the response structure is correct as per the API documentation
    workspaces = [
        (ws['id'], ws['attributes']['created-at']) for ws in workspaces_data['data']
    ]
    return workspaces

def fetch_resources(workspace_id):
    """Fetch resources for a given workspace ID."""
    resources_url = f"{API_URL}/workspaces/{workspace_id}/resources"
    response = requests.get(resources_url, headers=headers)
    resources_data = response.json()
    resources = resources_data['data']
    return resources

def main():
    # Fetch workspaces
    workspaces = fetch_workspaces()
    
    # Data storage
    workspaces_data = []
    resources_data = []
    
    # Process each workspace
    for workspace_id, created_at in workspaces:
        resources = fetch_resources(workspace_id)
        workspaces_data.append({'Workspace ID': workspace_id, 'Month': pd.to_datetime(created_at).strftime('%Y-%m')})
        for resource in resources:
            resources_data.append({
                'Workspace ID': workspace_id,
                'Month': pd.to_datetime(created_at).strftime('%Y-%m'),
                'Resource ID': resource['id']
            })
    
    # Create DataFrames
    df_workspaces = pd.DataFrame(workspaces_data)
    df_resources = pd.DataFrame(resources_data)
    
    # Calculate cumulative number of workspaces per month
    workspaces_per_month = df_workspaces.groupby('Month').size().cumsum().reset_index(name='Cumulative Number of Workspaces')
    workspaces_per_month = workspaces_per_month.sort_values('Month')
    print("Cumulative Workspaces per Month:")
    print(workspaces_per_month)
    
    # Calculate cumulative number of resources per month
    resources_per_month = df_resources.groupby('Month').size().cumsum().reset_index(name='Cumulative Number of Resources')
    resources_per_month = resources_per_month.sort_values('Month')
    print("\nCumulative Resources per Month:")
    print(resources_per_month)
    
    # Calculate cumulative number of resources per workspace per month
    resources_per_workspace_per_month = df_resources.groupby(['Workspace ID', 'Month']).size().groupby(level=0).cumsum().reset_index(name='Cumulative Number of Resources')
    resources_per_workspace_per_month = resources_per_workspace_per_month.sort_values(['Workspace ID', 'Month'])
    print("\nCumulative Resources per Workspace per Month:")
    print(resources_per_workspace_per_month)

if __name__ == "__main__":
    main()
