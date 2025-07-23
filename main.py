# -*- coding: utf-8 -*-
__author__ = "Самков Н.А. https://github.com/NikitaSamkov"
__maintainer__ = "Самков Н.А. https://github.com/NikitaSamkov"
__doc__ = "Основной модуль"

import os
from floss_getter import FLOSS_PATH, init_dmc_floss
from my_floss import MY_FLOSS_PATH
from readers import XSDPatternReader
from color_replacer import ColorReplacer


INPUT_DIR = os.path.join(os.path.dirname(__file__), 'input')
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), 'output')


def prepare():
    if not os.path.exists(MY_FLOSS_PATH):
        raise Exception('Не проинициализирован список имеющихся у вас мулине! Запустите my_floss.py для инициализации!')
    if not os.path.exists(FLOSS_PATH):
        init_dmc_floss()
    for sys_dir in [INPUT_DIR, OUTPUT_DIR]:
        if not os.path.exists(sys_dir):
            os.mkdir(sys_dir)


def main():
    """Основная точка входа. Запуск коррекции мулине для файлов в INPUT_DIR и сохранение в OUTPUT_DIR"""
    prepare()
    for pattern in os.listdir(INPUT_DIR):
        if not pattern.endswith('.xsd'):
            print(f'Пропущен {pattern}')
            continue
        reader = XSDPatternReader(os.path.join(INPUT_DIR, pattern))
        print(f'Прочитал файл {pattern}')

        ColorReplacer(reader).replace_palette()
        print(f'Заменил цвета палитры на пользовательские')

        reader.save(os.path.join(OUTPUT_DIR, pattern))
        print(f'Сохранил файл {pattern}')

        print('Проверка целостности полученного файла... ', end='')
        XSDPatternReader(os.path.join(OUTPUT_DIR, pattern))
        print('OK', end='\n\n')


if __name__ == '__main__':
    main()
