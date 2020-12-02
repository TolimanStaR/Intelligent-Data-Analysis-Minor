import datetime
import pyaudio
import logging
import re as regexp

from typing import Any
from abc import ABC, abstractmethod

import speech_recognition as rs
import pocketsphinx as ps

from .staticdata import *


class AbstractField(ABC):

    @abstractmethod
    def __init__(self):
        """Каждое поле необходимо инициализировать перед использованием"""

    @abstractmethod
    def is_valid_value(self, value: Any) -> bool:
        """Переданное значение поле необходимо проверить на валидность"""

    @abstractmethod
    def standardise_value(self, value: Any) -> Any:
        """Корректное значение требуется привести к стандартному для поля виду"""

    @abstractmethod
    def get_string_value(self) -> str:
        """Быстрое получение значения поля в виде строки"""

    @staticmethod
    @abstractmethod
    def parse_argument(command_string: str, class_arg_name: str):
        """Получение значения для создания экземпляра класса из строки аргументов команды"""

        result = regexp.findall(AbstractField.get_command_string_arg_pattern(class_arg_name), command_string)

        if result:
            return result[0]

    @staticmethod
    def get_command_string_arg_pattern(arg_name: str) -> str:
        return rf'--{arg_name}=([a-zA-Z0-9 \+.;]*)[-$\s\n\t ]+'

    class InvalidValue(Exception):
        def __init__(self, exception_text):
            print(exception_text)

    def __eq__(self, other):
        return self.get_string_value() == other.get_string_value()

    def __str__(self):
        return f'class models.{abs_field_class_str}'

    def __repr__(self):
        return abs_field_class_str


class Name(AbstractField):
    value_class = tuple
    class_arg_name = 'name'

    def __init__(self, value: str):
        super(Name, self).__init__()

        if self.is_valid_value(value):
            self.value: Name.value_class = self.standardise_value(value)
            self.first_name: str = self.value[0]
            self.last_name: str = self.value[1]
        else:
            raise self.InvalidValue(invalid_value_sign)

    def is_valid_value(self, value: Any) -> bool:

        is_valid = True

        if not type(value) is str:
            is_valid = False
            return is_valid

        if not value.replace(space, str()).isalpha():
            is_valid = False

        if not len(value.split()) == 2:
            is_valid: bool = False

        return is_valid

    def standardise_value(self, value: Any) -> value_class:
        return self.value_class(value.strip().title().split())

    @staticmethod
    def parse_argument(command_string: str, class_arg_name: str = class_arg_name):
        return AbstractField.parse_argument(command_string, class_arg_name)

    def __str__(self):
        return f'{self.value[0]} {self.value[1]}'

    def __repr__(self):
        return self.__str__()

    def get_string_value(self) -> str:
        return self.__str__()


class PhoneNumber(AbstractField):
    value_class = str
    class_arg_name = 'phone'

    def __init__(self, value: value_class, value_type: str = phone_types[0]):
        super().__init__()

        if self.is_valid_value(value):
            self.value: PhoneNumber.value_class = self.standardise_value(value)
            self.phone_type: str = value_type
        else:
            raise self.InvalidValue(invalid_value_sign)

    def standardise_value(self, value: Any) -> value_class:
        phone_number = self.reduce(value)
        result = f'+7 {phone_number[1:4]}-{phone_number[4:7]}-{phone_number[7:9]}-{phone_number[9:11]}'
        return result

    @staticmethod
    def parse_argument(command_string: str, class_arg_name: str = class_arg_name):
        return AbstractField.parse_argument(command_string, class_arg_name)

    @staticmethod
    def reduce(value: str) -> str:
        return value.strip().replace(space, str()).replace('-', str()).replace('+7', '8')

    def is_valid_value(self, value: Any) -> bool:

        is_valid: bool = True

        if not type(value) is str:
            is_valid = False
            return is_valid

        edited_value: str = self.reduce(value)

        if not edited_value.isdigit():
            is_valid = False

        if not len(edited_value) == 11:
            is_valid = False

        return is_valid

    def __str__(self):
        return f'{self.value}'

    def __repr__(self):
        return self.__str__()

    def get_string_value(self) -> str:
        return self.__str__()


class DateTime(AbstractField):
    value_class = datetime.date
    class_arg_name = 'birth'

    def __init__(self, value: value_class):
        super().__init__()

        if self.is_valid_value(value):
            self.value: DateTime.value_class = self.standardise_value(value)
        else:
            raise self.InvalidValue(invalid_value_sign)

    def standardise_value(self, value: Any) -> value_class:
        date_data: list = list(map(int, self.reduce(value).split()))

        date = datetime.date(
            year=date_data[0],
            month=date_data[1],
            day=date_data[2],
        )

        return date

    @staticmethod
    def parse_argument(command_string: str, class_arg_name: str = class_arg_name):
        return AbstractField.parse_argument(command_string, class_arg_name)

    @staticmethod
    def reduce(value: str) -> str:
        return value.strip().replace('-', space).replace('.', space).replace(';', space)

    @staticmethod
    def isdigit(string: str) -> bool:
        return string.isdigit()

    def is_valid_value(self, value: Any) -> bool:

        is_valid = True

        if not type(value) is str:
            is_valid = False
            return is_valid

        date: list = self.reduce(value).split()

        if not len(date) == 3:
            is_valid = False

        if not (len(date[0]) == 4 and 1 <= len(date[1]) <= 2 and 1 <= len(date[2]) <= 2):
            is_valid = False

        if not sum(map(self.isdigit, date)) == 3:
            is_valid = False
            return is_valid

        date = list(map(int, date))

        try:
            test_date = datetime.date(
                year=date[0],
                month=date[1],
                day=date[2],
            )
        except ValueError:
            print(f'Значение {value} некорректно. Попробуйте заново')
            is_valid = False
            return is_valid

        return is_valid

    def __str__(self):
        return f'{self.value.year}.{self.value.month}.{self.value.day}'

    def __repr__(self):
        return self.__str__()

    def get_string_value(self) -> str:
        return self.__str__()


class UserProfile(object):

    def __init__(self, name: Name = None, mobile_phone: PhoneNumber = None, birth_date: DateTime = None):
        """
        Инициализация объекта пользователя (контакта в справочнике)
        Каждое поле - отдельный класс, хранящий информацию
        """

        self.name: Name = name
        self.mobile_phone: PhoneNumber = mobile_phone
        self.birth_date: DateTime = birth_date
        self.extra_phones: list = list()

        self.identifier: int = self.get_identifier()

    def get_identifier(self) -> int:
        """Получение уникального идентификатора пользователя"""

        hash_sum = sum(map(hash, (self.name.get_string_value(),
                                  self.mobile_phone.get_string_value(),
                                  self.birth_date.get_string_value()))
                       )
        return hash_sum

    def recount_identifier(self):
        self.identifier = self.get_identifier()

    @staticmethod
    def parse_id(command_string: str, class_arg_name: str = 'id'):
        return AbstractField.parse_argument(command_string, class_arg_name)

    def __str__(self):
        return f'{self.name.get_string_value()} - ' \
               f'{self.mobile_phone.get_string_value()} ' \
               f'({self.birth_date.get_string_value()}) ' \
               f'id: {self.identifier}'

    def __repr__(self):
        return self.__str__()

    def __and__(self, other):
        """Сравнение пользователей на основе их уникального идентификатора"""

        return self.identifier == other.identifier

    def __eq__(self, other):
        """Сравнение пользователей на основе равенства их полей"""

        match = True

        if not (self.name == other.name and
                self.birth_date == other.birth_date and
                self.mobile_phone == other.mobile_phone):
            match = False

        return match

    def __xor__(self, other):
        """
        Перегрузка оператора '^' (XOR)
        Будет использоваться для проверки того, подходит ли
        Данный пользователь под определенные критерии поиска

        other - Пользователь, поля экземпляра которого
        могут быть заполнены не полностью, т.е. он служит неким 'паттерном'
        В этом случае считается, что поля не конфликтуют и равны
        """

        match = True

        if other.name:
            if not self.name == other.name:
                match = False

        if other.mobile_phone:
            if not self.mobile_phone == other.mobile_phone:
                match = False

        if other.birth_date:
            if not self.birth_date == other.birth_date:
                match = False

        return match


class PhoneBook(object):

    def __new__(cls, *args, **kwargs):
        """
        Записная книга всегда одна.
        таким образом, инициализируя экземпляр класса где угодно,
        мы получаем доступ к ней из любой части программы
        """

        if not hasattr(cls, 'instance'):
            cls.instance = super(PhoneBook, cls).__new__(cls)
        return cls.instance

    def __init__(self, db_file_name: str = database_file_name):
        """
        Считывание файла / БД
        И создание телефонной книги для использования в runtime
        """

        self.object_list = self.parse_database(db_file_name)

    @staticmethod
    def parse_database(database_file_name: str) -> list:  # todo: implement this function
        object_list: list = list()
        return object_list

    def add_user(self, user: UserProfile):
        """Добавление пользователя в справочник"""

        if user not in self.object_list:
            self.object_list.append(user)

    def __add__(self, other):
        self.add_user(other)

    def delete_user(self, target_user: UserProfile) -> None:
        """
        Удаление пользователя из справочника
        Удаление происходит по имени и фамилии
        """

        for index, user in enumerate(self.object_list):
            if target_user ^ user:
                self.object_list.pop(index)
                return

    def edit_user(self, identifier: int, command: str):
        """Изменение информации о пользователе"""

        user_index = self.get_user_index_by_id(identifier)
        new_name: Name = Name(Name.parse_argument(command_string=command))
        new_phone: PhoneNumber = PhoneNumber(PhoneNumber.parse_argument(command_string=command))
        new_date: DateTime = DateTime(DateTime.parse_argument(command_string=command))

        if not user_index == -1:
            if hasattr(new_name, default_class_value_name):
                self.object_list[user_index] = new_name
            if hasattr(new_phone, default_class_value_name):
                self.object_list[user_index] = new_phone
            if hasattr(new_date, default_class_value_name):
                self.object_list[user_index] = new_date

            self.object_list[user_index].recount_identifier()

    def search_user(self, target_user: UserProfile) -> UserProfile:
        for user in self.object_list:
            if target_user ^ user:
                return user

    def get_user_index(self, target_user: UserProfile) -> int:
        target_index = -1

        for index, user in enumerate(self.object_list):
            if target_user ^ user:
                target_index = index

        return target_index

    def get_user_index_by_id(self, identifier: int):
        for index, user in enumerate(self.object_list):
            if user.identifier == identifier:
                return index

    def __contains__(self, item):
        return not self.search_user(item)

    def contains(self, user):
        return self.__contains__(user)

    @staticmethod
    def search_by_fields(self, *fields: 'class : Name, PhoneNumber, DateTime') -> None:
        """Поиск пользователей в справочнике по разным полям"""

        object_list: list = list()

        for user in object_list:
            print(user)

    def save(self):
        """Сохранение изменений в справочнике"""
        pass

    def __str__(self):
        """Естественным образом, будет изпользоваться для отображения справочника пользователю"""
        string = str()
        return string

    def __repr__(self):
        return self.__str__()


class Command(object):
    pass
