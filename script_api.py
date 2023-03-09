from __future__ import print_function

import os.path

from pprint import pprint
from googleapiclient import discovery
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1JGpUQbOLdQfJMS8LYeuRx2O25R7x5Y1YoRbuApZZTEk'
# SAMPLE_RANGE_NAME = '01!A22'
value_input_option = "USER_ENTERED"

def getCatalogo(creds):

    service = discovery.build('sheets', 'v4', credentials=creds)

    # The ID of the spreadsheet to retrieve data from.
    spreadsheet_id = SAMPLE_SPREADSHEET_ID  # TODO: Update placeholder value.

    # The A1 notation of the values to retrieve.
    range_ = 'LOGIN!A2:C158'  # TODO: Update placeholder value.

    request = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=range_)
    response = request.execute()

    # TODO: Change code below to process the `response` dict:
    pprint(response)

def appendValues(creds, matricula):
    try:
        service = build('sheets', 'v4', credentials=creds)
        values = [
            [
                matricula
            ],
            # Additional rows ...
        ]
        body = {
            'values': values
        }

        # Call the Sheets API
        sheet = service.spreadsheets()
        result = sheet.values().append(
            spreadsheetId=SAMPLE_SPREADSHEET_ID,
            range='01!A22', valueInputOption=value_input_option, body=body).execute()
        print(f"{result.get('updatedCells')} cells updated.")
        return result

    except HttpError as err:
        print(err)

def main():

    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=8080)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds
    # while True:
    #     x = input()
    #     if x == 'p':
    #         appendValues(creds, 'A01720623', 'Ricardo Jasso', 'ITC', 'Octavo Semestre', 'Acreditado(a)', 'TEC21', 'Monterrey')

if __name__ == '__main__':
    main()

    # while True:
    #     x = input()
    #     if x == 'p':
            # appendValues(credentials, 'A01720623', 'Ricardo Jasso', 'ITC', 'Octavo Semestre', 'Acreditado(a)', 'TEC21', 'Monterrey')
