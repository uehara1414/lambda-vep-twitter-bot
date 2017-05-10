import os
import sys

sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'vendor'))  # noqa

import gspread
from oauth2client.service_account import ServiceAccountCredentials


def get_worksheet():
    scope = ['https://spreadsheets.google.com/feeds']
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client = gspread.authorize(creds)

    sheet = client.open("lambda-bot-log")
    for worksheet in sheet.worksheets():
        if worksheet.id == 'od6':
            return worksheet


def lambda_handler(event, context):
    worksheet = get_worksheet()
    print(worksheet.get_all_values())
    # worksheet.append_row(['tweet.id_str', 'tweet.author.screen_name', 'tweet.text', 'tweet.created_at'])


if __name__ == '__main__':
    lambda_handler(None, None)
