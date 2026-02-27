"""
Google Gmail API OAuth2 Authentication Handler

This module handles the OAuth2 authentication flow for Gmail API access.
Supports loading credentials from both .env variables and credentials.json file.
"""

import os
import json
from pathlib import Path
from typing import Optional

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Gmail API scopes
SCOPES = [
  'https://www.googleapis.com/auth/gmail.send',      # Send emails
  'https://www.googleapis.com/auth/gmail.modify',    # Modify emails (mark as read, etc.)
  'https://www.googleapis.com/auth/gmail.readonly',  # Read emails (check for replies)
]

# File paths
TOKEN_FILE = 'token.json'
CREDENTIALS_FILE = 'credentials.json'


def get_client_config() -> dict:
  """
  Get OAuth client configuration from environment variables or credentials.json.

  Returns:
      dict: Client configuration for OAuth flow

  Raises:
      ValueError: If neither .env credentials nor credentials.json are found
  """
  # Try loading from environment variables first
  client_id = os.getenv('GOOGLE_CLIENT_ID')
  client_secret = os.getenv('GOOGLE_CLIENT_SECRET')

  if client_id and client_secret:
      print("✓ Loading Google credentials from .env file")
      return {
          "installed": {
              "client_id": client_id,
              "client_secret": client_secret,
              "auth_uri": "https://accounts.google.com/o/oauth2/auth",
              "token_uri": "https://oauth2.googleapis.com/token",
              "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
              "redirect_uris": ["http://localhost"]
          }
      }

  # Fall back to credentials.json
  if Path(CREDENTIALS_FILE).exists():
      print(f"✓ Loading Google credentials from {CREDENTIALS_FILE}")
      with open(CREDENTIALS_FILE, 'r') as f:
          return json.load(f)

  raise ValueError(
      "No Google credentials found. Please either:\n"
      "  1. Set GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET in .env, or\n"
      f"  2. Place {CREDENTIALS_FILE} in the project root"
  )


def get_credentials() -> Credentials:
  """
  Get valid Google API credentials, handling OAuth flow if necessary.

  Returns:
      Credentials: Valid Google API credentials

  Notes:
      - Checks for existing token.json with valid credentials
      - Attempts to refresh expired credentials
      - Initiates OAuth flow if no valid credentials exist
      - Saves new credentials to token.json for future use
  """
  creds = None

  # Load existing token if available
  if Path(TOKEN_FILE).exists():
      print(f"✓ Found existing {TOKEN_FILE}")
      creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

  # If no valid credentials, get new ones
  if not creds or not creds.valid:
      if creds and creds.expired and creds.refresh_token:
          print("⟳ Refreshing expired credentials...")
          try:
              creds.refresh(Request())
              print("✓ Credentials refreshed successfully")
          except Exception as e:
              print(f"✗ Failed to refresh credentials: {e}")
              print("⟳ Starting new OAuth flow...")
              creds = None

      # Start OAuth flow if refresh failed or no credentials
      if not creds:
          print("⟳ Starting OAuth2 authorization flow...")
          print("→ A browser window will open for you to authorize the application")

          client_config = get_client_config()
          flow = InstalledAppFlow.from_client_config(
              client_config,
              SCOPES
          )
          creds = flow.run_local_server(port=0)
          print("✓ Authorization successful!")

      # Save credentials for next run
      with open(TOKEN_FILE, 'w') as token:
          token.write(creds.to_json())
      print(f"✓ Credentials saved to {TOKEN_FILE}")
  else:
      print("✓ Using valid existing credentials")

  return creds


def get_gmail_service():
  """
  Get authenticated Gmail API service instance.

  Returns:
      Resource: Authenticated Gmail API service object

  Example:
      >>> service = get_gmail_service()
      >>> results = service.users().messages().list(userId='me').execute()
  """
  creds = get_credentials()
  service = build('gmail', 'v1', credentials=creds)
  print("✓ Gmail API service initialized")
  return service


def authenticate_gmail():
  """
  Main authentication function. Returns authenticated Gmail service.
  Alias for get_gmail_service() for backwards compatibility.

  Returns:
      Resource: Authenticated Gmail API service object
  """
  return get_gmail_service()


def test_connection() -> bool:
  """
  Test the Gmail API connection by fetching user profile.

  Returns:
      bool: True if connection successful, False otherwise
  """
  try:
      service = get_gmail_service()
      profile = service.users().getProfile(userId='me').execute()
      email = profile.get('emailAddress')
      print(f"✓ Successfully connected to Gmail as: {email}")
      return True
  except Exception as e:
      print(f"✗ Connection test failed: {e}")
      return False


if __name__ == "__main__":
  # Test authentication when run directly
  print("Testing Gmail API authentication...\n")
  test_connection()
