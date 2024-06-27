import requests
import pandas as pd
import os
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt

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

def plot_data(workspaces_per_month, resources_per_month, current_resources_per_workspace):
    # Workspaces per Month
    plt.figure(figsize=(10, 6))
    plt.plot(workspaces_per_month['Month'], workspaces_per_month['Cumulative Workspaces'], marker='o', label='Total Workspaces per Month')
    plt.title('Total Workspaces per Month')
    plt.xlabel('Month')
    plt.ylabel('Total Workspaces')
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # Resources per Month
    plt.figure(figsize=(10, 6))
    plt.plot(resources_per_month['Month'], resources_per_month['Number of Resources'], marker='o', color='r', label='Resources Existing per Month')
    plt.title('Resources Existing per Month')
    plt.xlabel('Month')
    plt.ylabel('Number of Resources')
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # Current Resources per Workspace
    plt.figure(figsize=(12, 8))
    current_resources_per_workspace.sort_values('Current Number of Resources', ascending=False, inplace=True)
    plt.bar(current_resources_per_workspace['Workspace Name'], current_resources_per_workspace['Current Number of Resources'], color='green')
    plt.title('Current Resources per Workspace')
    plt.xlabel('Workspace Name')
    plt.ylabel('Number of Resources')
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.show()

def main():
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', None)
    
    workspaces = fetch_workspaces()
    all_resources = []
    all_workspaces = []

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

    df_resources = pd.DataFrame(all_resources)
    df_workspaces = pd.DataFrame(all_workspaces)

    df_workspaces['Created Month'] = pd.to_datetime(df_workspaces['Created Month']).dt.to_period('M')
    workspaces_per_month = df_workspaces.groupby('Created Month').size().reset_index()
    workspaces_per_month.columns = ['Month', 'Workspaces Created']
    workspaces_per_month['Month'] = workspaces_per_month['Month'].astype(str)
    full_date_range = pd.date_range(start=df_workspaces['Created Month'].min().to_timestamp(), end=datetime.today(), freq='MS').strftime('%Y-%m')
    all_months_df = pd.DataFrame(full_date_range, columns=['Month'])
    workspaces_per_month = pd.merge(all_months_df, workspaces_per_month, on='Month', how='left').fillna(0)
    workspaces_per_month['Cumulative Workspaces'] = workspaces_per_month['Workspaces Created'].cumsum().astype(int)

    resources_per_month = df_resources.groupby('Month').agg({'Resource ID': pd.Series.nunique}).reset_index()
    resources_per_month.rename(columns={'Resource ID': 'Number of Resources'}, inplace=True)
    resources_per_month = pd.merge(all_months_df, resources_per_month, on='Month', how='left').fillna(0)

    latest_month = df_resources['Month'].max()
    resources_current_month = df_resources[df_resources['Month'] == latest_month].groupby('Workspace Name').agg({'Resource ID': pd.Series.nunique}).reset_index()
    resources_current_month.rename(columns={'Resource ID': 'Current Number of Resources'}, inplace=True)
    all_workspace_names = df_workspaces[['Workspace Name']].drop_duplicates()
    current_resources_per_workspace = pd.merge(all_workspace_names, resources_current_month, on='Workspace Name', how='left')
    current_resources_per_workspace['Current Number of Resources'].fillna(0, inplace=True)

    # Print tables to the terminal
    print("Workspaces per Month (Created and Cumulative):")
    print(workspaces_per_month)
    print("\nResources per Month (Count and Cumulative):")
    print(resources_per_month)
    print("\nCurrent Resources per Workspace:")
    print(current_resources_per_workspace)

    # Plot data
    plot_data(workspaces_per_month, resources_per_month, current_resources_per_workspace)

if __name__ == "__main__":
    main()
