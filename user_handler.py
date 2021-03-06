from abc import ABC, abstractmethod
from typing import Optional
from enum import Enum, auto

reply_state_type = tuple[str, Optional[tuple[str, ...]]]


class IState(ABC):
	"""User state interaction interface"""
	_user: Optional['User'] = None

	@property
	def user(self) -> 'User':
		return self._user

	@user.setter
	def user(self, user: 'User') -> None:
		self._user = user

	@abstractmethod
	def handle_message(self, message: str):
		raise NotImplementedError

	@abstractmethod
	def state_reply(self) -> reply_state_type:
		raise NotImplementedError


class DefaultState(IState):

	def __init__(self):
		self.reply: Optional[str] = 'DefaultState'
		self.states = {
			'Инфо': GetUserState.INFO,
			'Добавить еду': GetUserState.FOOD,
			'Авторизация': GetUserState.AUTH,
		}

	def handle_message(self, message: str):

		if message not in self.states:
			self.reply = "Я не знаю такой команды"
		else:
			self.user.state_transition(new_state=self.states[message])

	def state_reply(self) -> reply_state_type:
		return self.reply, tuple(self.states.keys())


class InfoState(IState):
	"""User state by default"""
	buttons = ('Вся информация', 'Назад')

	def __init__(self):
		self.reply: Optional[str] = 'InfoState'

	def handle_message(self, message: str):
		self.reply = 'InfoState'
		if message == 'Назад':
			self.reply = 'Возврат'
			self.user.state_transition(GetUserState.DEFAULT)

	def state_reply(self) -> reply_state_type:
		return self.reply, self.buttons


class AuthState(IState):
	"""User authorization status"""
	buttons = ('Назад',)

	def __init__(self):
		self.reply: Optional[str] = 'AuthState'

	def handle_message(self, message: str):
		self.reply = 'AuthState'
		if message == 'Назад':
			self.reply = 'Возврат'
			self.user.state_transition(GetUserState.DEFAULT)

	def state_reply(self) -> reply_state_type:
		return self.reply, self.buttons


class FoodAddState(IState):
	"""State of adding food"""
	buttons = ('Добавление', 'Назад', )

	def __init__(self):
		self.reply: Optional[str] = 'FoodAddState'
		self.step_names = ('name', 'kcal', 'gram')
		self.food_iterator = None
		self.food_data = []

	def handle_message(self, message: str):
		self.reply = 'FoodAddState'
		if message == 'Назад':
			self.user.state_transition(GetUserState.DEFAULT)
		elif message == 'Добавление':
			self.food_iterator = iter(self.step_names)
			self.reply = next(self.food_iterator)
		else:
			self.food_data.append(message)
			try:
				self.reply = next(self.food_iterator)
			except StopIteration:
				foods = {x: y for x in self.step_names for y in self.food_data}
				self.user.user_data['food'].append(foods)
				self.reply = f"{self.user.user_data['food']}"

	def state_reply(self) -> reply_state_type:
		return self.reply, self.buttons


class GetUserState(Enum):
	"""Contain user state class constructor"""
	DEFAULT = DefaultState
	INFO = InfoState
	AUTH = AuthState
	FOOD = FoodAddState


class User:
	"""Main user class"""
	def __init__(self, user_id: int):
		self.user_id: 				int = user_id
		self.active_state: 			IState = GetUserState.DEFAULT.value()
		self.user_data = {
			'food': []
		}
		self.active_state.user = self

	def user_message(self, message: str):
		"""Handle user message"""
		state = self.active_state
		state.handle_message(message=message)

	def bot_message(self) -> reply_state_type:
		"""Reply for user"""
		reply = self.active_state.state_reply()
		return reply

	def state_transition(self, new_state: GetUserState = GetUserState.DEFAULT):
		"""Set new user state"""
		self.active_state: IState = new_state.value()
		self.active_state.user = self


class UserHandler:
	"""
	Class handle active_user
	Singleton pattern
	"""
	__users = {}
	__instance = None

	def __new__(cls, *args, **kwargs):
		if not cls.__instance:
			cls.__instance = super().__new__(cls)
			return cls.__instance
		return cls.__instance

	@property
	def users(self):
		return self.__users

	@users.setter
	def users(self, value):
		self.__users[value] = User(value)

	def get_user(self, user_id) -> User:
		"""Return user instance and add this into main users dictionary"""
		try:
			return self.users[user_id]
		except KeyError:
			self.users = user_id
			return self.users[user_id]


if __name__ == '__main__':
	user_handler = UserHandler()
	user1 = user_handler.get_user(123)
	user2 = user_handler.get_user(1233)
	user3 = user_handler.get_user(12143)
	print(user1)
	print(user2)
	print(user3)
