#!/usr/bin/env python3
import os.path
import argparse
import sys
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/admin.directory.user']

def get_credentials():
    """Obtain valid OAuth2 credentials from token.json or via an interactive flow."""
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('client_secrets.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

def main():
    parser = argparse.ArgumentParser(
        description='Offboard (delete) a user via Google Admin Directory API using OAuth2 credentials'
    )
    parser.add_argument('--email', help='User email address', required=True)
    args = parser.parse_args()

    email = args.email.strip()

    creds = get_credentials()
    service = build('admin', 'directory_v1', credentials=creds)

    try:
        service.users().delete(userKey=email).execute()
        print(f"User {email} has been successfully offboarded (deleted).")
    except Exception as e:
        print("An error occurred while offboarding the user:", e)
        sys.exit(1)

if __name__ == '__main__':
    main()
