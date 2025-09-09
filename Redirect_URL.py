# -*- coding: utf-8 -*-
import os
import pandas as pd
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# --- Configuration ---
credential_file = r'fpasar_token.json'
token_file = os.path.join(os.path.dirname(credential_file), 'fpasar_token.json')

# ❗️ 1. FOLDER_ID has been updated to your new folder.
FOLDER_ID = flow_variables['gdrive_folder_link']#'1AzdlQWEZEzehEmqiFCou4Ax0UoXIlEAt'
# ---

def perform_oauth():
    """Handles Google OAuth2 flow and returns an authenticated API service object."""
    SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
    creds = None
    if os.path.exists(token_file):
        creds = Credentials.from_authorized_user_file(token_file, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(credential_file):
                raise FileNotFoundError(f"Credential file not found at: {credential_file}")
            flow = InstalledAppFlow.from_client_secrets_file(credential_file, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(token_file, 'w') as token:
            token.write(creds.to_json())
    service = build('drive', 'v3', credentials=creds)
    return service

# --- Main script execution for KNIME ---
try:
    drive_service = perform_oauth()
    
    # ❗️ LOGIC CHANGE: This API call now gets up to 1000 files and more details.
    results = drive_service.files().list(
        q=f"'{FOLDER_ID}' in parents and trashed=false",
        pageSize=1000,  # Get up to 1000 files from the folder
        orderBy='name', # Sort the results alphabetically by name
        fields="files(id, name, webViewLink, modifiedTime, size, mimeType)" # Request more info
    ).execute()
    
    items = results.get('files', [])

    if not items:
        output_df = pd.DataFrame({'status': ['No files found in this folder.']})
    else:
        # Create a list to hold the details of each file
        all_files_details = []
        for item in items:
            # For each file, create a dictionary of its details
            file_data = {
                'ID': item.get('id'),
                'FileName': item.get('name'),
                'Link': item.get('webViewLink'),
                'ModifiedTime': item.get('modifiedTime'),
                # Google Docs/Sheets don't have a size, so default to 0
                'Size_Bytes': int(item.get('size', 0)),
                'Type': item.get('mimeType')
            }
            all_files_details.append(file_data)
        
        # Convert the list of file details into a Pandas DataFrame
        output_df = pd.DataFrame(all_files_details)

except Exception as e:
    output_df = pd.DataFrame({'error': [str(e)]})

# Assign the resulting DataFrame to the KNIME node's output
output_table_1 =  output_df
