import sys

class Choice:
	#TODO: Document this somewhat magic bastard
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
		self.message += f"\n\t[Input q] Quit"
		self.message +="\nInput: "

	def chosen(self, userinput):
		userinput = userinput.strip()
		if userinput.lower() in ("q", "quit"): return CLIApp.quit, ''
		if not self.make_decision: return self.callables, userinput

		try: chosen = self.callables[int(userinput)- 1]
		except (ValueError, IndexError):
			print(f"\t [ERROR]: You must input a number from 1 to {len(self.callables)} but you inputted {userinput}")
			return CLIApp.rerun, self

		# Success
		return chosen, ''


class CLIApp:
	#TODO: Document this
	choices: dict

	def run_event_loop(self, first_choice: str):
		choice = self.choices[first_choice]
		while True:
			print()
			userin = input(choice.message)
			choice = self.receive(choice, userin)


	def receive(self, choice: Choice, userinput: str):
		chosen, args = choice.chosen(userinput)
		if isinstance(chosen, str): return self.choices[chosen]
		choice = chosen(args) if args else chosen()
		return choice

	@staticmethod
	def quit():
		print("Bye!")
		sys.exit()

	@staticmethod
	def rerun(choice: Choice): return choice
