import sys

from db import Database

class Choice:
	def __init__(self, message: str, decisions: dict=None, only_call=None):
		self.message = message
		self.make_decision = only_call is None
		self.callables = list()

		if self.make_decision:
			self.message += "\n\tOptions:"
			for i, (call, text) in enumerate( decisions.items() ):
				self.callables.append(call)
				self.message += f"\n  [Input {i+1}] {text}"
		else: self.callables = only_call
		self.message += f"\n\t\tInput q for quit."
		self.message +="\nInput: "
	def chosen(self, userinput):
		userinput = userinput.strip()
		if userinput.lower() in ("q", "quit"): return App.quit, ''
		if not self.make_decision: return self.callables, userinput

		# User errors
		try: choice = int(userinput)
		except ValueError:
			print(f"\t [ERROR]: You must input a number corresponding to your choice, but you inputted {userinput}")
			return 'rerun', self
		try: chosen = self.callables[choice - 1]
		except IndexError:
			print(f"\t [ERROR]: You must input a number from 1 to {len(self.callables) + 1} but you inputted {userinput}")
			return 'rerun', self

		# Success
		return chosen, ''

class App:
	def __init__(self):
		self.choices = {
			"main":
				Choice("Choose action.",
					decisions={"new_intake": "Add new intake", "analyze": "Analyze previous intake"}),
			"new_intake":
				Choice("Input a calorie intake in the following form [foodname], [weight in g], [number of calories]",
					only_call=self.new_intake ),
			"analyze":
				Choice("Not implemented", only_call="welcome"),
		}

		print("\tConnecting to your database ... ", end='')
		self.db = Database()
		print("✔️")

		print("\nWelcome to PyCal, the Python Calorie counter\n")

	def receive(self, choice: Choice, userinput: str):
		chosen, args = choice.chosen(userinput)
		if isinstance(chosen, str): return self.choices[chosen]
		choice = chosen(args) if args else chosen()
		return choice


	def new_intake(self, userin: str): raise NotImplementedError

	@staticmethod
	def quit(): sys.exit()

	@staticmethod
	def rerun(choice: Choice): return choice


def run_event_loop():
	app = App()
	choice = app.choices["main"]
	while True:
		userin = input(choice.message)
		choice = app.receive(choice, userin)

if __name__ == '__main__':
	run_event_loop()
