import gspread
from oauth2client.service_account import ServiceAccountCredentials

class Database:
	""" """
    def __init__(self, secret_path: str = 'secret.json'):
		"""
		Sets up a connection to a Google Spreadsheet/Google Drive database.
		A secret.json and external setup is required in the Google account ecosystem:
			1. Create a new project in the Google API's console: https://console.developers.google.com/
			2. Click Enable API and choose Google Drive API
			3. Create credientials for a Web Server with access to Application Data
			4. Download the given JSON file and save it in src/ folder as secret.json
			5. Go to the relevant Google Sheets spreadshirt and click Share. As the email, pyt in the client email found
				in the JSON access file.




		"""
        scope = ['https://www.googleapis.com/auth/spreadsheets',  'https://www.googleapis.com/auth/drive']
        credentials = ServiceAccountCredentials.from_json_keyfile_name(secret_path, scopes=scope)
        self.client = gspread.authorize(credentials)


if __name__ == '__main__':
    syncer = Syncer()
    syncer.read_data()
