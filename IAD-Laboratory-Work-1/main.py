from include.dispatch import *
from include.staticdata import *

import argparse


if __name__ == '__main__':
    pass


    a = Name('Ivan susanin')
    print(a)

    b = PhoneNumber('+7 905 195 53-97')
    print(b)

    command = 'command --name=Vladimir lenin --phone=+7 905 195 53 97  --birth=2001 . 3 ; 20 '

    print(a.parse_argument(command))
    print(b.parse_argument(command))
    print(DateTime(DateTime.parse_argument('--birth=3452 7 4 ')))

    p = PhoneBook()
    print(p)

    for x in p.object_list:
        for y in x:
            print(y)
    p.save()