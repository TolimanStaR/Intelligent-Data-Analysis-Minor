from include.dispatch import *
from include.staticdata import *

import argparse


if __name__ == '__main__':
    pass


    a = Name('Ivan сусanin')
    print(a)

    b = PhoneNumber('+7 905 195 53-97')
    print(b)

    command = 'command --name=Vladimir lenin --phone=+7 905 195 53 97  '

    print(a.parse_argument(command))
    print(b.parse_argument(command))
