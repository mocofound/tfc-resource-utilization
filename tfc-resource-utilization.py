import requests
import pandas as pd
import os
from datetime import datetime
import numpy as np

# Constants
API_URL = "https://app.terraform.io/api/v2"
ORGANIZATION = "aharness-org"
TOKEN = os.environ['TFC_TOKEN']  # Terraform Cloud token from environment variables

# Headers for authentication
headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/vnd.api+json"
}

def fetch_workspaces():
    """Fetch all workspaces and return a list of their IDs, creation dates, and names."""
    workspaces = []
    next_url = f"{API_URL}/organizations/{ORGANIZATION}/workspaces"
    while next_url:
        response = requests.get(next_url, headers=headers)
        if response.status_code != 200:
            print("Failed to fetch workspaces:", response.status_code)
            print("Response:", response.text)
            return workspaces
        workspaces_data = response.json()
        workspaces.extend([
            (ws['id'], ws['attributes']['created-at'], ws['attributes']['name']) for ws in workspaces_data['data']
        ])
        next_url = workspaces_data.get('links', {}).get('next', None)
    return workspaces

def fetch_resources(workspace_id):
    """Fetch resources for a given workspace ID."""
    resources = []
    next_url = f"{API_URL}/workspaces/{workspace_id}/resources"
    while next_url:
        response = requests.get(next_url, headers=headers)
        if response.status_code != 200:
            print("Failed to fetch resources:", response.status_code)
            return resources
        resources_data = response.json()
        resources.extend([(resource['id'], resource['attributes']['created-at']) for resource in resources_data['data']])
        next_url = resources_data.get('links', {}).get('next', None)
    return resources

def main():
    pd.set_option('display.max_rows', None)  # or specify a number of rows: pd.set_option('display.max_rows', 500)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', None)
    
    # Fetch workspaces
    workspaces = fetch_workspaces()
    
    # Data storage for resources and workspaces
    all_resources = []
    all_workspaces = []

    # Process each workspace
    for workspace_id, created_at, workspace_name in workspaces:
        all_workspaces.append({
            'Workspace ID': workspace_id,
            'Workspace Name': workspace_name,
            'Created Month': pd.to_datetime(created_at).strftime('%Y-%m')
        })
        resources = fetch_resources(workspace_id)
        for resource_id, resource_created_at in resources:
            all_resources.append({
                'Workspace ID': workspace_id,
                'Workspace Name': workspace_name,
                'Resource ID': resource_id,
                'Month': pd.to_datetime(resource_created_at).strftime('%Y-%m')
            })

    # Convert list of dictionaries to DataFrame
    df_resources = pd.DataFrame(all_resources)
    df_workspaces = pd.DataFrame(all_workspaces)

    # Calculate total number of workspaces per month
    df_workspaces['Created Month'] = pd.to_datetime(df_workspaces['Created Month']).dt.to_period('M')
    workspaces_per_month = df_workspaces.groupby('Created Month').size().reset_index()
    workspaces_per_month.columns = ['Month', 'Workspaces Created']
    workspaces_per_month['Month'] = workspaces_per_month['Month'].astype(str)
    full_date_range = pd.date_range(start=df_workspaces['Created Month'].min().to_timestamp(), end=datetime.today(), freq='MS').strftime('%Y-%m')
    all_months_df = pd.DataFrame(full_date_range, columns=['Month'])
    workspaces_per_month = pd.merge(all_months_df, workspaces_per_month, on='Month', how='left').fillna(0)
    workspaces_per_month['Cumulative Workspaces'] = workspaces_per_month['Workspaces Created'].cumsum().astype(int)

    # Group by month to see resources per month
    resources_per_month = df_resources.groupby('Month').agg({'Resource ID': pd.Series.nunique}).reset_index()
    resources_per_month = resources_per_month.rename(columns={'Resource ID': 'Number of Resources'})
    resources_per_month = pd.merge(all_months_df, resources_per_month, on='Month', how='left').fillna(0)
    resources_per_month['Cumulative Resources'] = resources_per_month['Number of Resources'].cumsum()

    # Display Tables
    print("Workspaces per Month (Created and Cumulative):")
    print(workspaces_per_month)
    print("\nResources per Month (Count and Cumulative):")
    print(resources_per_month)

if __name__ == "__main__":
    main()
