import sys
import datetime

from db import Database
from cliapp import Choice, CLIApp

class PyCal(CLIApp):
	def __init__(self):
		super().__init__()

		self.choices = {
			"main":
				Choice("Choose action.",
					decisions={"new_intake": "Add new intake", "analyze": "Analyze previous intake"}),
			"new_intake":
				Choice("Input a calorie intake in the following form [foodname], [weight in g], [number of calories].\
						 Seperate with ;  to input more intakes.",
					only_call=self.new_intake ),
			"analyze":
				Choice("Not implemented", only_call="welcome"),
		}

		print("\tConnecting to your database ... ", end='')
		self.db = Database()
		self.nowtable = self._monthtable()
		print("✔️")

		print("\nWelcome to PyCal, the command line Calorie counter\n")

	def new_intake(self, userin: str):
		try: intakes = self._parse_intake(userin)
		except: #TODO: Handle expection type
			print(f"\t [ERROR]: Your input was not understood. Use comma for name, weight, calori seperation and semicolon for intake seperation.\
					\nPress arrow up to retrieve your input")
			return self.choices["new_intake"]

		print("\tSending intake to your database ... ", end='')
		self.db.append_rows(self.nowtable, intakes)
		print("✔️")

		return self.choices["main"]

	@staticmethod
	def _parse_intake(userin: str) -> str:
		raw_intakes = userin.split(";")
		clean_intakes = []
		for intake in raw_intakes:
			fields = intake.split(",")
			assert len(fields) == 3
			clean_intakes.append(
				(fields[0].strip().lower(), int(float(fields[1].strip())), int(float(fields[2].strip())))
				)
		return clean_intakes

	def _monthtable(self):
		target = datetime.datetime.now().strftime('%m%Y')
		if target in self.db.get_all_tables(): return target
		return self.db.create_table(target)


if __name__ == '__main__':
	app = PyCal()
	app.run_event_loop(first_choice="main")
