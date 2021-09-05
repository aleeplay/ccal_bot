from typing import Optional, Union


class PersonalCcalCalculator:
    def __init__(self, user_id: str, username: str):
        self.user_id = user_id
        self.username = username
        self.max_ccal = 2000
        self._food_list = []
        self._ccal_left = None

    def __str__(self):
        return self.user_id

    @staticmethod
    def how_much_ccal(text_of_message: str) -> (str, int):
        data: tuple = tuple(text_of_message.split())
        food_name, ccal_100, ccal = data[0], int(data[1]), int(data[2])
        return food_name, ccal_100 * ccal // 100

    def ccal_left_counter(self) -> int:
        return self.max_ccal - sum([ccal['ccal'] for ccal in self._food_list])

    @property
    def food(self):
        return self._food_list

    @food.setter
    def food(self, value: Union[tuple[str, int], int]):
        if isinstance(value, int):
            self._food_list.pop(value)
        elif len(value) == 2:
            food_name, ccal = value
            self._food_list.append({'label': food_name, 'ccal': ccal})
        else:
            raise Exception('Параметры пустые')
        self.ccal_left = self.ccal_left_counter()

    @food.deleter
    def food(self):
        self._food_list = []

    @property
    def ccal_left(self):
        if not self._ccal_left:
            self._ccal_left = self.ccal_left_counter()
        return self._ccal_left

    @ccal_left.setter
    def ccal_left(self, value: int):
        self._ccal_left = value


if __name__ == '__main__':
    a = PersonalCcalCalculator('123123', 'qwe')
    ood, cal = a.how_much_ccal('qwe 111 312 312')
    a.food = 'qwe', 123
    print(a.food)