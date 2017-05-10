import os
import sys

sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'vendor'))  # noqa

import gspread
from oauth2client.service_account import ServiceAccountCredentials


# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

# Find a workbook by name and open the first sheet
# Make sure you use the right name here.
sheet = client.open("lambda-bot-log").sheet1


def lambda_handler(event, context):
    list_of_hashes = sheet.get_all_records()
    print(list_of_hashes)

    print('hello world')


if __name__ == '__main__':
    lambda_handler(None, None)
