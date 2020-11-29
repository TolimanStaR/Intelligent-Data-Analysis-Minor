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
    def is_valid_value(self, value: Any):
        pass

    @abstractmethod
    def standardise_value(self, value: Any) -> Any:
        pass

    @abstractmethod
    def get_raw_value(self):
        pass

    class InvalidValue(Exception):
        def __init__(self, exception_text):
            print(exception_text)

    def __str__(self):
        return 'class models.AbstractField'

    def __repr__(self):
        return self.__str__()


class Name(AbstractField):
    value_class = tuple

    def __init__(self, value: Any):
        if self.is_valid_value(value):
            self.value_1, self.value_2 = self.standardise_value(value)
            self.first_name = self.value_1
            self.last_name = self.value_2
        else:
            raise self.InvalidValue(invalid_value_sign)

    def is_valid_value(self, value: Any) -> bool:
        return bool(1)

    def standardise_value(self, value: Any) -> value_class:
        return self.value_class([None, None])

    def get_raw_value(self):
        return f'{self.value_1} {self.value_2}'


class PhoneNumber(AbstractField):
    pass


class DateTime(AbstractField):
    pass


class UserProfile(object):

    # Создание объекта

    def __init__(self, name: Name, mobile_phone: PhoneNumber, birth_date: DateTime):
        self.name = name
        self.mobile_phone = mobile_phone
        self.birth_date = birth_date

    # Получение уникального идентификатора

    def get_identifier(self):
        pass


class PhoneBook(object):

    # Считывание файла / БД и создание телефонной книги для использования в runtime

    def __init__(self, database_file_name: str):
        self.object_list = list()

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

    # Строковое представление объекта

    def __str__(self):
        string = str()
        return string

    def __repr__(self):
        return self.__str__()


class Command(object):
    pass
