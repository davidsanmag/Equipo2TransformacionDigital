from __future__ import print_function

import os.path
import pandas as pd

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

def isEnrolled(creds, student_id):
    service = discovery.build('sheets', 'v4', credentials=creds)

    # The ID of the spreadsheet to retrieve data from.
    spreadsheet_id = SAMPLE_SPREADSHEET_ID  # TODO: Update placeholder value.

    # The A1 notation of the values to retrieve.
    range_ = 'ListadoCompletoTest!A:A'  # TODO: Update placeholder value.

    request = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=range_)
    response = request.execute()
    data = response.get('values')

    df = pd.DataFrame(data[1:], columns=data[0])

    if student_id in df.values:
        return True
    return False


def getRemainingPlaces(creds, crn):
    service = discovery.build('sheets', 'v4', credentials=creds)

    # The ID of the spreadsheet to retrieve data from.
    spreadsheet_id = SAMPLE_SPREADSHEET_ID  # TODO: Update placeholder value.

    # The A1 notation of the values to retrieve.
    range_ = 'CUPO'  # TODO: Update placeholder value.

    request = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=range_)
    response = request.execute()
    data = response.get('values')

    df = pd.DataFrame(data[1:], columns=data[0])

    values = df[df['CRN'] == crn]['Cupo Restante'].tolist()
    if len(values) > 0:
        return int(values[0])

    return False

def getStudentID(creds, student_id):
    service = discovery.build('sheets', 'v4', credentials=creds)

    # The ID of the spreadsheet to retrieve data from.
    spreadsheet_id = SAMPLE_SPREADSHEET_ID  # TODO: Update placeholder value.

    # The A1 notation of the values to retrieve.
    range_ = 'Historial!A:A'  # TODO: Update placeholder value.

    request = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=range_)
    response = request.execute()
    data = response.get('values')

    df = pd.DataFrame(data[1:], columns=data[0])
    if student_id in df.values:
        return True

    return False


def getCatalog(creds):

    service = discovery.build('sheets', 'v4', credentials=creds)

    # The ID of the spreadsheet to retrieve data from.
    spreadsheet_id = SAMPLE_SPREADSHEET_ID  # TODO: Update placeholder value.

    # The A1 notation of the values to retrieve.
    range_ = 'LOGIN'  # TODO: Update placeholder value.

    request = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=range_)
    response = request.execute()
    data = response.get('values')

    df = pd.DataFrame(data[1:], columns=data[0])

    return df

def appendValues(creds, student_id, crn):
    try:
        service = build('sheets', 'v4', credentials=creds)
        values = [
            [
                student_id, crn
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
            range='ListadoCompletoTest!A2:B', valueInputOption=value_input_option, body=body).execute()
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

if __name__ == '__main__':
    main()