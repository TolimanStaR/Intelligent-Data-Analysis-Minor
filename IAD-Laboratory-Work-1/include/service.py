from .models import *


def greeting():
    print(f'Привет, {os.getlogin()}')
    print(greeting_text)


def farewell():
    print(farewell_text)


def list_action(*args):
    print(PhoneBook())


def search(*args):
    string = args[0]
    name, phone, date = Name(Name.parse_argument(string)), \
                        PhoneNumber(PhoneNumber.parse_argument(string)), \
                        DateTime(DateTime.parse_argument(string))

    pattern_user: UserProfile = UserProfile(name, phone, date)

    PhoneBook().search_by_fields(pattern_user)


def add(*args):
    string = args[0]
    name, phone, date = Name(Name.parse_argument(string)), \
                        PhoneNumber(PhoneNumber.parse_argument(string)), \
                        DateTime(DateTime.parse_argument(string))

    if not type(name.value) == EmptyField and not type(phone.value) == EmptyField:
        new_user = UserProfile(
            name,
            phone,
            date,
        )
        if not PhoneBook().search_user(new_user):
            PhoneBook().add_user(new_user)
        else:
            print(user_exists)
            if approve('Вы хотите редактировать запись пользователя?'):
                edit(args[0] + space, new_user.identifier)


def edit(*args, id: int = -1):
    string = args[0]

    if id == -1:
        id: int = UserProfile().parse_id(string)

    if type(id) != EmptyField:
        PhoneBook().edit_user(id, string)


def delete(*args):
    string = args[0]
    new_name = Name.parse_argument(string)
    template_user: UserProfile = UserProfile(Name(new_name))
    if type(template_user.name.value) is not EmptyField:
        PhoneBook().delete_user(template_user)
    else:
        print(user_does_not_exist)


def get_age(*args):
    string = args[0]
    new_name = Name.parse_argument(string)
    new_phone = PhoneNumber.parse_argument(string)
    template_user: UserProfile = UserProfile(Name(new_name), PhoneNumber(new_phone))
    if type(template_user.name.value) is not EmptyField or type(template_user.mobile_phone.value) is not EmptyField:
        index = PhoneBook().get_user_index(template_user)
        try:
            delta = datetime.date.today() - PhoneBook().object_list[index].birth_date.value
            print(f'Возраст - {int((delta.days - (delta.days // 365) / 4) // 365)} лет')
        except TypeError:
            print('У пользователя не указан год рождения')
    else:
        print(user_does_not_exist)


def delete_by_phone(*args):
    string = args[0]
    new_phone = PhoneNumber.parse_argument(string)
    template_user: UserProfile = UserProfile(mobile_phone=PhoneNumber(new_phone))
    if type(template_user.mobile_phone.value) is not EmptyField:
        PhoneBook().delete_user(template_user)
    else:
        print(user_does_not_exist)


def help_action(*args):
    print(tutorial)


def empty_action() -> None:
    pass
