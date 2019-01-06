import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pprint
from random import randint

def fetch_command():
    scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name("Master-GoogleSheets.json", scope)
    client = gspread.authorize(creds)

    sheet = client.open('Ajax').sheet1
    command = sheet.row_values(randint(2, 28))
    return command
