from __future__ import print_function

import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


def get_events(creds=None):
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                          singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])
    return events


def main():
    events=get_events()
    with open("calendar.txt", "w") as file:
        file.write("Date,StartTime,EndTime,Title,Length")
        for event in events:
            start = event['start'].get('dateTime')
            stats = (start.split("T"))
            end = event['end'].get('dateTime')
            stats2 = (end.split("T"))
            date = stats[0].split("-")
            length = int(".".join(((stats2[1].split('+')[0]).split(":"))[:1])) - int(
                ".".join(((stats[1].split('+')[0]).split(":"))[:1]))
            if length > 0:
                file.write(
                    f"\n{date[2]}/{date[1]}--::{stats[1].split('+')[0]}--::{stats2[1].split('+')[0]}--::'{event['summary']}'--:: {length}")
            else:
                file.write(
                    f"\n{date[2]}/{date[1]}--::{stats[1].split('+')[0]}--::{stats2[1].split('+')[0]}--::'{event['summary']}'--:: {length+24}")

