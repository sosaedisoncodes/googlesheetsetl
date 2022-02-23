from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dotenv import load_dotenv
import argparse
import PyPDF2


load_dotenv()


# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = "1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms"
SAMPLE_RANGE_NAME = "Class Data!A2:E"


def main(pdf_path, sheet=None):
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(host="127.0.0.1", port=4000)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    # Accessing the PDF data
    with open(pdf_path, "rb") as pdf:
        pdf_obj = PyPDF2.PdfFileReader(pdf)
        page = pdf_obj.getPage(0)
        print(page.extractText())


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Arguments for parsing PDF data to google sheets"
    )
    parser.add_argument("-pdf_path", action="store", nargs="?", type=str)
    parser.add_argument("-sheet", action="store", nargs=1)
    args = parser.parse_args()
    main(pdf_path=args.pdf_path)
