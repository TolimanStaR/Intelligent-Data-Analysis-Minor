from .service import *

import multiprocessing
import threading

__recognizer = None


def init_session(*args) -> None:
    global __recognizer

    # __recognizer = LiveSpeech()
    # daemon = multiprocessing.Process(target=__recognizer.daemon(), args=(), )
    # daemon.start()

    # r = threading.Thread(target=shell, args=(0,))
    # r.start()
    # p = multiprocessing.Process(target=LiveSpeech().daemon(), args=(), daemon=True)
    # p.start()

    __narrator = FRIDAY()

    # Инициализация записной книги

    __database = PhoneBook()

    greeting()


def complete_session(*args) -> None:
    __database = PhoneBook()
    __database.save()

    farewell()

    quit(0)


def shell(mode: int = 0) -> None:

    while True:
        print('>>> ', end='')

        action = Command()

        if mode == 0:
            command = InputData()
            command.get_data()

            if not command.data:
                continue

            action.recognize_command_from_text(command.data)

        else:
            FRIDAY().say(random.choice(AI_command_prompt))
            command = __recognizer
            command.listen()
            action.recognize_command_from_speech()

        try:
            if mode == 1:
                FRIDAY().say(random.choice(AI_ask_args))
                arguments = InputData()
                arguments.get_data()

                command.data = arguments.data

            command_action[action.command](command.data + space)

        except KeyError:
            print(command_not_found)


command_action: dict = {
    'list': list_action,
    'search': search,
    'add': add,
    'delete': delete,
    'pdelete': delete_by_phone,
    'edit': edit,
    'get_age': get_age,
    'quit': complete_session,
    'help': help_action,
}
