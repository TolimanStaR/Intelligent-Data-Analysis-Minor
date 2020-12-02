phone_book = None

invalid_value_sign: str = 'Вы ввели некорректное значение поля'


# Имя файла базы данных по умолчанию:

database_file_name: str = 'data.csv'

# можно заменить на свое,
# но лучше делать это через аргументы


phone_types: tuple = (
    'Мобильный',
    'Домашний',
    'Рабочий',
    'Запасной',

)

available_commands: tuple = (
    'list',
    'get_id',
    'search',
    'add',
    'delete',
    'edit',
    'get_age',
    'add_phone',
    'quit',
)

abs_field_class_str: str = 'AbstractField'

default_class_value_name: str = 'value'

space: str = ' '
