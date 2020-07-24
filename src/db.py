import gspread

def resource_error(f):
	def wrap(*args, **kwargs):
		try: return f(*args, **kwargs)
		except gspread.exceptions.APIError as e:
			if '429' in str(e):
				print("You have exceeded the usage limit on Googles Sheets API.\n\
					(100 requests per 100 secs, see: https://developers.google.com/sheets/api/limits).\
					\n You can wait for some time and try again")
			raise e
	return wrap

class Database:
	""" A Database object maintains all contact to the Gspread tables """
	@resource_error
	def __init__(self,
			secret_path: str = 'secret.json',
			sheet_name:  str = 'Pycal',
			):
		"""
		Sets up a connection to a Google Spreadsheet/Google Drive database.
		A secret.json and external setup is required in the Google account ecosystem:
			1. Create a new project in the Google API's console [1]
			2. Click Enable API and choose Google Drive API
			3. Create credientials for a Web Server with access to Application Data
			4. Download the given JSON file and save it in repo folder as secret.json
			5. Go to the relevant Google Sheets spreadshirt and click Share. As the email, pyt in the client email found
				in the JSON access file.
		This is based on a twilio tutorial [2] and the gspread docs [3].

		[1] https://console.developers.google.com/
		[2] https://www.twilio.com/blog/2017/02/an-easy-way-to-read-and-write-to-a-google-spreadsheet-in-python.html
		[3] https://gspread.readthedocs.io/en/latest/oauth2.html#enable-api-access-for-a-project
		"""
		scopes = ('https://www.googleapis.com/auth/spreadsheets',  'https://www.googleapis.com/auth/drive')
		self.client = gspread.service_account(filename=secret_path, scopes=scopes)
		try:
			self.data = self.client.open(sheet_name)
		except	gspread.exceptions.SpreadsheetNotFound:
			raise gspread.exceptions.SpreadsheetNotFound( f"Spreadsheet not found:\
				Are you sure you have created and clicked 'Share' for spreadsheet {sheet_name}")
		sheets = self.data.worksheets()
		self._tables = { w.title: w for w in sheets }

	def get_all_tables(self) -> list:
		return list(self._tables.keys())

	@resource_error
	def create_table(self, name: str, rows: int=1000, cols: int=20):
		if name in self.get_all_tables(): raise NameError(f"Table name {name} already used")
		self._tables[name] = self.data.add_worksheet(title=name, rows=str(rows), cols=str(cols))

	@resource_error
	def fetch_table(self, name: str) -> list:
		return self._tables[name].get_all_values()

	@resource_error
	def append_rows(self, name: str, values: list):
		self._tables[name].append_rows(values)

if __name__ == '__main__':
	db = Database()
