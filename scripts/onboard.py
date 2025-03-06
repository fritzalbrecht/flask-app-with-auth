#!/usr/bin/env python3
import os.path
import argparse
import json
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
        description='Onboard a new user via Google Admin Directory API using OAuth2 credentials'
    )
    parser.add_argument('--first', help='First name', required=True)
    parser.add_argument('--last', help='Last name', required=True)
    args = parser.parse_args()

    first_name = args.first.strip()
    last_name = args.last.strip()
    email = f"{first_name.lower()}.{last_name.lower()}@fritzalbrecht.com"

    creds = get_credentials()
    service = build('admin', 'directory_v1', credentials=creds)

    user_body = {
        "primaryEmail": email,
        "name": {
            "givenName": first_name,
            "familyName": last_name
        },
        "password": "ChangeMe123!",
        "changePasswordAtNextLogin": True,
        "orgUnitPath": "/"
    }

    try:
        user = service.users().insert(body=user_body).execute()
        print(f"User {email} created successfully!")
        print(json.dumps(user, indent=2))
    except Exception as e:
        print("An error occurred while creating the user:", e)
        sys.exit(1)

if __name__ == '__main__':
    main()
