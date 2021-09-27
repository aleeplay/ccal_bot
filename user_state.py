from abc import ABC, abstractmethod


class State(ABC):
	def __init__(self, user_data: dict):
		self.user_data = user_data

	@abstractmethod
	def reply(self) -> str:
		raise NotImplementedError

	@abstractmethod
	def handle_message(self, message: str) -> dict:
		raise NotImplementedError


class InfoState(State):
	name = 'InfoState'

	def handle_message(self, message: str) -> dict:
		pass

	def reply(self) -> str:
		return self.name


class FoodState(State):
	name = 'FoodState'

	def __init__(self, user_data: dict):
		super().__init__(user_data)

	def handle_message(self, message: str) -> dict:
		self.user_data[self.name] = message
		return self.user_data

	def reply(self) -> str:
		return self.name


class TestState1(State):
	name = 'TestState1'

	def handle_message(self, message: str) -> dict:
		pass

	def reply(self) -> str:
		return self.name


class TestState2(State):
	name = 'TestState1'

	def handle_message(self, message: str) -> dict:
		pass

	def reply(self) -> str:
		return self.name
