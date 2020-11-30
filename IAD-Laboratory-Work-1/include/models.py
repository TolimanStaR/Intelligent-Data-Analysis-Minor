import datetime
import pyaudio
import logging

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
    def get_raw_value(self) -> str:
        """Быстрое получение значения поля в виде строки"""

    class InvalidValue(Exception):
        def __init__(self, exception_text):
            print(exception_text)

    def __str__(self):
        return 'class models.AbstractField'

    def __repr__(self):
        return self.__str__()


class Name(AbstractField):
    value_class = tuple

    def __init__(self, value: value_class):
        super(Name, self).__init__()

        if self.is_valid_value(value):
            self.value: Name.value_class = self.standardise_value(value)
            self.first_name: str = self.value[0]
            self.last_name: str = self.value[1]
        else:
            raise self.InvalidValue(invalid_value_sign)

    def is_valid_value(self, value: Any) -> bool:
        return bool(1)

    def standardise_value(self, value: Any) -> value_class:
        return self.value_class([None, None])

    def get_raw_value(self) -> str:
        return f'{self.value[0]} {self.value[1]}'


class PhoneNumber(AbstractField):
    value_class = str

    def __init__(self, value: value_class, value_type: str = phone_types[0]):
        super().__init__()

        if self.is_valid_value(value):
            self.value: PhoneNumber.value_class = self.standardise_value(value)
            self.phone_type: str = value_type
        else:
            raise self.InvalidValue(invalid_value_sign)

    def get_raw_value(self) -> str:
        pass

    def standardise_value(self, value: Any) -> value_class:
        pass

    def is_valid_value(self, value: Any) -> bool:
        pass


class DateTime(AbstractField):
    value_class = datetime.date

    def __init__(self, value: value_class):
        super().__init__()

        if self.is_valid_value(value):
            self.value: DateTime.value_class = self.standardise_value(value)
        else:
            raise self.InvalidValue(invalid_value_sign)

    def get_raw_value(self) -> str:
        pass

    def standardise_value(self, value: Any) -> value_class:
        pass

    def is_valid_value(self, value: Any) -> bool:
        pass


class UserProfile(object):

    # Создание объекта

    def __init__(self, name: Name, mobile_phone: PhoneNumber, birth_date: DateTime):
        self.name = name
        self.mobile_phone = mobile_phone
        self.birth_date = birth_date
        self.extra_phones = list()

    # Получение уникального идентификатора

    def get_identifier(self) -> int:
        hash_sum = sum(map(hash, (self.name.get_raw_value(),
                                  self.mobile_phone.get_raw_value(),
                                  self.birth_date.get_raw_value()))
                       )
        return hash_sum


class PhoneBook(object):

    # Записная книга всегда одна.
    # таким образом, инициализируя экземпляр класса где угодно,
    # мы получаем доступ к ней из любой части программы

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(PhoneBook, cls).__new__(cls)
        return cls.instance

    # Считывание файла / БД и создание телефонной книги для использования в runtime

    def __init__(self, db_file_name: str = database_file_name):
        self.object_list = self.parse_database(db_file_name)

    @staticmethod
    def parse_database(database_file_name: str) -> list:
        object_list: list = list()
        return object_list

    # Добавление нового пользователя в справочник

    def __add__(self, other):
        self.add_user(other)

    def add_user(self, user: UserProfile):
        pass

    # Удаление пользователя из справочника

    def delete_user(self, user: UserProfile):
        pass

    # Изменение информации о пользователе

    def edit_user(self, user: UserProfile):
        pass

    # Поиск конкретного пользователя
    #
    # Некоторые поля могут быть не инициализированы,
    # тогда возвращается первый подходящий объект

    def search_user(self, user: UserProfile):
        pass

    # Поиск пользователей в справочнике по критериям / полям

    @staticmethod
    def search_by_fields(self, *fields: 'class : Name, PhoneNumber, DateTime') -> None:
        object_list: list = list()

        for user in object_list:
            print(user)

    # Сохранение изменений в книге

    def save(self):
        pass

    # Строковое представление объекта

    def __str__(self):
        string = str()
        return string

    def __repr__(self):
        return self.__str__()


class Command(object):
    pass
