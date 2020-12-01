phone_book = None

invalid_value_sign: str = 'Вы ввели некорректное значение поля'

database_file_name: str = 'data.csv'  # Значение по умолмчанию

phone_types = (
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

space: str = ' '
