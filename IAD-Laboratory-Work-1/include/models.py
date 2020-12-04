import datetime
import random

import pyaudio
import logging
import pyttsx3
import csv
import os
import time
import re as regexp

from typing import Any
from abc import ABC, abstractmethod

import speech_recognition as rs
import pocketsphinx as psx

from .staticdata import *

# from .service import *

from include import dispatch


def approve(string: str) -> bool:
    print(string)
    print('Введите что-то по типу: да / ага / не')

    choice = input()

    if choice.lower() in yes:
        return True

    if choice.lower() in no:
        return False


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

        return str()

    @staticmethod
    @abstractmethod
    def parse_argument(command_string: str, class_arg_name: str):
        """Получение значения для создания экземпляра класса из строки аргументов команды"""

        result = regexp.findall(AbstractField.get_command_string_arg_pattern(class_arg_name), command_string)

        if result:
            return result[0]
        else:
            return EmptyField()

    @staticmethod
    def get_command_string_arg_pattern(arg_name: str) -> str:
        return rf'--{arg_name}=(-*[a-zA-Z0-9а-яА-Я \+.;]*)[-$\s\n\t ]+'

    class InvalidValue(Exception):
        def __init__(self, exception_text):
            print(exception_text)

    def __eq__(self, other):
        return self.get_string_value() == other.get_string_value()

    def __str__(self):
        return f'class models.{abs_field_class_str}'

    def __repr__(self):
        return abs_field_class_str


class EmptyField(object):
    @staticmethod
    def get_string_value():
        return str()

    def __str__(self):
        return str()


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
            self.value = EmptyField()

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
        if type(self.value) != EmptyField:
            return f'{self.value[0]} {self.value[1]}'
        return str()

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
            self.value = EmptyField()

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
            self.value = EmptyField()

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
            return is_valid

        if not (len(date[0]) == 4 and 1 <= len(date[1]) <= 2 and 1 <= len(date[2]) <= 2):
            is_valid = False

        if not sum(map(self.isdigit, date)) == 3:
            is_valid = False
            return is_valid

        date = list(map(int, date))

        try:
            datetime.date(
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
        if type(self.value) != EmptyField:
            return f'{self.value.year}.{self.value.month}.{self.value.day}'
        return str()

    def __repr__(self):
        return self.__str__()

    def get_string_value(self) -> str:
        return self.__str__()


class UserProfile(object):

    def __init__(self, name: Name = EmptyField(),
                 mobile_phone: PhoneNumber = EmptyField(),
                 birth_date: DateTime = EmptyField(),
                 extra_phones: list = EmptyField()):
        """
        Инициализация объекта пользователя (контакта в справочнике)
        Каждое поле - отдельный класс, хранящий информацию
        """

        self.name: Name = name
        self.mobile_phone: PhoneNumber = mobile_phone
        self.birth_date: DateTime = birth_date
        self.extra_phones = extra_phones

        self.identifier: int = self.get_identifier()
        self.array: list = []

    def get_identifier(self) -> int:
        """Получение уникального идентификатора пользователя"""

        hash_sum = sum(map(hash, (self.name.get_string_value(),
                                  self.mobile_phone.get_string_value(),
                                  self.birth_date.get_string_value()
                                  )))

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

    def __iter__(self):

        self.iterable: list = [
            self.name.get_string_value(),
            self.mobile_phone.get_string_value(),
        ]

        if not type(self.birth_date) is EmptyField:
            self.iterable.append(self.birth_date.get_string_value())

        if not type(self.extra_phones) is EmptyField:
            self.iterable.append(f'\'{self.extra_phones}\'')

        return self.iterable.__iter__()

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

        if type(other.name) != EmptyField:
            if type(other.name.value) != EmptyField:
                if not self.name == other.name:
                    match = False

        if type(other.mobile_phone) != EmptyField:
            if type(other.mobile_phone.value) != EmptyField:
                if not self.mobile_phone == other.mobile_phone:
                    match = False

        if type(other.birth_date) != EmptyField:
            if type(other.birth_date.value) != EmptyField:
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
    def parse_database(db_file_name: str = database_file_name) -> list:
        object_list: list = list()
        try:
            with open(db_file_name, 'r', newline='', encoding='utf-8') as database_file:
                reader = csv.reader(database_file)

                for user_data in list(reader):
                    new_name: Name = Name(user_data[0])
                    new_phone: PhoneNumber = PhoneNumber(user_data[1])

                    new_date: Any = EmptyField()
                    if len(user_data) >= 3:
                        new_date = DateTime(user_data[2])

                    new_extra_phones: Any = EmptyField()
                    if len(user_data) >= 4:
                        new_extra_phones: list = eval(user_data[3])

                    new_user = UserProfile(
                        new_name,
                        new_phone,
                        new_date,
                        new_extra_phones,
                    )
                    object_list.append(new_user)

        except FileNotFoundError:
            print('Файла базы данных не существует')

        return object_list

    def add_data(self, db_file_name: str):
        self.object_list += self.parse_database(db_file_name=db_file_name)

    def add_user(self, user: UserProfile):
        """Добавление пользователя в справочник"""

        if user not in self.object_list:
            self.object_list.append(user)
            self.save()

        else:
            print('Такой пользователь существует.')

    def __add__(self, other):
        self.add_user(other)

    def delete_user(self, target_user: UserProfile) -> None:
        """
        Удаление пользователя из справочника
        Удаление происходит по имени и фамилии
        """

        for index, user in enumerate(self.object_list):
            if user ^ target_user:
                if approve('Вы подтверждаете удаление пользователя? Введите да или нет'):
                    print(f'Пользователь {self.object_list[index].name} удален')
                    self.object_list.pop(index)
                    self.save()
                    return

        print(user_does_not_exist)

    def edit_user(self, identifier: int, command: str):
        """Изменение информации о пользователе"""

        user_index = self.get_user_index_by_id(identifier)

        new_name: Name = Name(Name.parse_argument(command_string=command))
        new_phone: PhoneNumber = PhoneNumber(PhoneNumber.parse_argument(command_string=command))
        new_date: DateTime = DateTime(DateTime.parse_argument(command_string=command))

        if user_index:

            if type(new_name.value) is not EmptyField:
                self.object_list[user_index].name = new_name

            if type(new_phone.value) is not EmptyField:
                self.object_list[user_index].mobile_phone = new_phone

            if type(new_date.value) is not EmptyField:
                self.object_list[user_index].birth_date = new_date

            # self.object_list[user_index].recount_identifier()

            self.save()

            print('Контакт изменен')
            return

        print('Контакт не найден')

    def search_user(self, target_user: UserProfile) -> bool:
        for user in self.object_list:
            if user ^ target_user:
                return True

        return False

    def get_user_index(self, target_user: UserProfile) -> int:
        target_index = -1

        for index, user in enumerate(self.object_list):
            if user ^ target_user:
                target_index = index

        return target_index

    def get_user_index_by_id(self, identifier: int):
        for index, user in enumerate(self.object_list):
            if int(user.identifier) - int(identifier) == 0:
                return index

    def __contains__(self, item):
        return not self.search_user(item)

    def contains(self, user):
        return self.__contains__(user)

    def search_by_fields(self, pattern_user_profile: UserProfile) -> None:
        """
        Поиск пользователей в справочнике по разным полям
        Все поисковые поля содержатся в экземпляре класса UserProfile
        С каждым пользователем производится нестрогое сравнение, что дает возможность
        Получить несколько объектов
        """

        object_list: list = list()

        for user in self.object_list:
            if user ^ pattern_user_profile:
                object_list.append(user)

        self.represent(object_list)

    def save(self, db_file_name: str = database_file_name):
        """Сохранение изменений в справочнике"""

        with open(db_file_name, 'w', encoding='utf-8', newline='') as data_base:
            writer = csv.writer(data_base)
            for row in self.object_list:
                writer.writerow(row)

    @staticmethod
    def represent(object_list):
        print(f'Всего {len(object_list)} объектов:')
        for index, user in enumerate(object_list):
            print(f'{index + 1}. {user}')

    def __str__(self):
        """Естественным образом, будет использоваться для отображения справочника пользователю"""

        string = str()

        string += f'Всего {len(self.object_list)} объектов:\n'
        for index, user in enumerate(self.object_list):
            string += f'{index + 1}. {user}\n'

        return string

    def __repr__(self):
        return self.__str__()


class LiveSpeech(object):

    def __new__(cls):
        """
        Определим речь как синглтон.
        Инициализация модели - затратная по времени операция, поэтому оптимально будет
        Инициализировать ее только один раз, и потом использовать
        """

        if not hasattr(cls, 'instance'):
            cls.instance = super(LiveSpeech, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.model_path = psx.get_model_path()
        self.speech_stream = psx.LiveSpeech(
            verbose=False,
            sampling_rate=16000,
            buffer_size=2048,
            no_search=False,
            full_utt=False,
            hmm=os.path.join(self.model_path, 'zero_ru.cd_cont_4000'),
            lm=os.path.join(self.model_path, 'ru.lm'),
            dic=os.path.join(self.model_path, 'ru.dic')
        )
        self.data: str = str()

    def listen(self):
        for phrase in self.speech_stream:
            self.data = phrase
            break

    def daemon(self):
        for phrase in self.speech_stream:
            if str(phrase) in AI_name or AI_name in str(phrase):
                FRIDAY.say(FRIDAY(), random.choice(AI_greeting))
                dispatch.shell(1)
                pass

    def get_most_similar_action(self, action_list: list = rus_available_commands):
        """
        Добавим чуть чуть интеллектуальности. На иаде все-таки учимся
        Будем искать максимально похожее доступное действие с помощью динамики по строкам
        """

        current_coincidence: float = .0
        most_similar_command: str = str()

        data_arr = reversed(self.data.split())

        for statement in data_arr:
            for action in action_list:
                reward: float = (len(action) * len(statement)) ** .5 * (1 / abs(len(action) - len(statement) + 1)) ** .5
                print(statement, action, reward)

                matrix = [[.0] * (len(action) + 1) for _ in range(len(statement) + 1)]

                for i, x in enumerate(statement):
                    for j, y in enumerate(action):
                        if x == y:
                            matrix[i + 1][j + 1] = matrix[i][j] + reward
                        else:
                            matrix[i + 1][j + 1] = max(matrix[i][j + 1], matrix[i + 1][j])

                coincidence_in_place: float = max(map(max, matrix))

                if coincidence_in_place > current_coincidence:
                    current_coincidence = coincidence_in_place
                    most_similar_command = action

        return most_similar_command


class InputData(object):
    """
    Входные данные - это просто текст
    Входные данные не знают, что они команда, которая что-то делает
    """

    def __init__(self):
        self.data: str = str()

    def get_data(self):
        # todo: добавить приглашение
        try:
            self.data: str = str(input())
        except EOFError:
            pass

    @staticmethod
    def dumb_get_most_similar_action(data: str, action_list: list = available_commands):

        data_arr = list(reversed(data.split()))

        for action in action_list:
            for statement in data_arr:
                if statement == action:
                    return action


class FRIDAY(object):
    """
    Синтезатор голоса.
    До Джарвиса ей далековато, в плане харизмы,
    Но команды озвучивает и юмора программе она добавляет :)
    Тоже синглтон, к удивлению
    """

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(FRIDAY, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.synthesizer = pyttsx3.init()
        self.voices_list = self.synthesizer.getProperty('voices')
        self.synthesizer.setProperty('voice', 'ru')

    def say(self, text: str):
        self.synthesizer.say(f'{text}')
        self.synthesizer.runAndWait()

    def init(self):
        self.__init__()

    def __str__(self):
        return 'class models.FRIDAY'


class Command(object):
    """
    Команда как что-то абстрактное.
    Класс не должен знать, что это текст или речь, полученная от пользователя
    Класс может попросить ввести команду, но не знать, как это происходит
    """

    def __init__(self):
        self.command = None

    @staticmethod
    def invite_to_enter_command():
        print(command_enter_invitation)

    def recognize_command_from_text(self, string: str = str()):
        """Распознавание команды из текста"""

        self.command = InputData.dumb_get_most_similar_action(string)

    def recognize_command_from_speech(self):
        """Распознавание команды из речи"""

        self.command = LiveSpeech.get_most_similar_action(LiveSpeech().instance)
