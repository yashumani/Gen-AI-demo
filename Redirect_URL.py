# -*- coding: utf-8 -*-
import os
import pandas as pd
import hashlib
import urllib.parse as urlp
from datetime import datetime
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# ---------------- Configuration from KNIME Flow Variables ----------------
credential_file = r'fpasar_token.json'
token_file = os.path.join(os.path.dirname(credential_file), 'fpasar_token.json')

FOLDER_ID   = flow_variables['gdrive_folder_link']
WEBAPP_BASE = flow_variables.get('webapp_base', '').strip()
CAMPAIGN    = flow_variables.get('campaign', 'IE_default')
SALT        = flow_variables.get('salt', '')
PROMPT_BASE = flow_variables.get('prompt_base', '')  # optional; if blank we use the same Drive link

# ---------------- OAuth helper ----------------
def perform_oauth():
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

# ---------------- Small utilities ----------------
def sha256_short(s: str, salt: str, n: int = 16) -> str:
    x = (salt + (s or '').strip().lower()).encode('utf-8')
    return hashlib.sha256(x).hexdigest()[:n]

def url_encode(u: str) -> str:
    return urlp.quote(u, safe='')

def build_redirect(base: str, cid: str, email_h: str, btn: str, dest: str) -> str:
    return f"{base}?cid={cid}&email={email_h}&btn={btn}&dest={url_encode(dest)}"

# ---------------- Main ----------------
try:
    drive_service = perform_oauth()

    # Pull up to 1000 files from the folder with details
    results = drive_service.files().list(
        q=f"'{FOLDER_ID}' in parents and trashed=false",
        pageSize=1000,
        orderBy='modifiedTime desc',  # most recent first
        fields="files(id, name, webViewLink, modifiedTime, size, mimeType)"
    ).execute()
    items = results.get('files', [])

    if not items:
        output_table_1 = pd.DataFrame({'status': ['No files found in this folder.']})
    else:
        # Build a full table for visibility
        all_files_details = []
        for it in items:
            all_files_details.append({
                'ID': it.get('id'),
                'FileName': it.get('name'),
                'Link': it.get('webViewLink'),
                'ModifiedTime': it.get('modifiedTime'),
                'Size_Bytes': int(it.get('size', 0) or 0),
                'Type': it.get('mimeType')
            })
        files_df = pd.DataFrame(all_files_details)

        # Pick the latest file (row 0 due to orderBy=modifiedTime desc)
        latest = files_df.iloc[0].copy()
        open_link = latest['Link']
        # If PROMPT_BASE provided, use that; else reuse the same link
        prompt_link = PROMPT_BASE if PROMPT_BASE else open_link

        # --------- Mode A (no recipient input): emit latest links only ---------
        # If the node received no input_table (KNIME passes a 0-row df sometimes),
        # or the input doesn't have an 'email' column, we output a single-row with links.
        try:
            has_recipients = 'input_table' in globals() and isinstance(input_table, pd.DataFrame) and ('email' in input_table.columns)
        except Exception:
            has_recipients = False

        if not has_recipients:
            output_table_1 = pd.DataFrame([{
                'Campaign': CAMPAIGN,
                'FileName': latest['FileName'],
                'ModifiedTime': latest['ModifiedTime'],
                'open_link': open_link,
                'prompt_link': prompt_link
            }])
        else:
            # --------- Mode B (with recipients): build redirect URLs per recipient ---------
            df = input_table.copy()

            # Safety: ensure 'email' column is string
            df['email'] = df['email'].astype(str)

            # Hash emails (privacy-safe)
            df['email_h'] = df['email'].apply(lambda x: sha256_short(x, SALT, n=16))

            # Build redirect links (requires WEBAPP_BASE)
            if not WEBAPP_BASE:
                raise ValueError("Flow variable 'webapp_base' is empty. Set it to your Apps Script Web App URL.")

            df['open_redirect']   = df['email_h'].apply(lambda h: build_redirect(WEBAPP_BASE, CAMPAIGN, h, 'open',   open_link))
            df['prompt_redirect'] = df['email_h'].apply(lambda h: build_redirect(WEBAPP_BASE, CAMPAIGN, h, 'prompt', prompt_link))

            # Optional: include context columns for convenience
            df['Campaign'] = CAMPAIGN
            df['FileName'] = latest['FileName']
            df['ModifiedTime'] = latest['ModifiedTime']

            # Emit only the useful columns for the Email node
            cols = ['email', 'email_h', 'Campaign', 'FileName', 'ModifiedTime', 'open_redirect', 'prompt_redirect']
            output_table_1 = df[cols]

except Exception as e:
    output_table_1 = pd.DataFrame({'error': [str(e)]})
