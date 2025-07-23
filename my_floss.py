# -*- coding: utf-8 -*-
__author__ = "Самков Н.А. https://github.com/NikitaSamkov"
__maintainer__ = "Самков Н.А. https://github.com/NikitaSamkov"
__doc__ = "Формирование списка номеров мулине (DMC), которые есть у пользователя"

import os
import json


MY_FLOSS_PATH = os.path.join(os.path.dirname(__file__), 'my_floss.json')


def init_my_floss():
    """Формирование списка цветов DMC пользователя"""
    my_floss = []
    print('Вводите номера мулине, которые у вас есть. По одному номеру на строку.')
    print('Оставьте пустую строку для окончания выполнения программы.')
    while (floss_num := input()) != '':
        if floss_num == '5200':
            floss_num = 'B5200'
        if floss_num in my_floss:
            print('!!! ВНИМАНИЕ!!! ПОВТОРЯЮЩИЙСЯ ЦВЕТ !!!')
        else:
            my_floss.append(floss_num)
    with open(MY_FLOSS_PATH, 'w') as f:
        json.dump(my_floss, f, indent=2, ensure_ascii=False)
    print(f'Список цветов мулине успешно сохранён по пути {MY_FLOSS_PATH}. Нажмите enter для продолжения...')


def real_time_floss_check():
    """Проверка наличия у пользователя переданных цветов в формате IO"""
    with open(MY_FLOSS_PATH, 'r') as f:
        data = json.load(f)

    while (floss_num := input()) != '':
        if floss_num == '5200':
            floss_num = 'B5200'
        if floss_num in data:
            print('Есть в наличии!')
        else:
            print('Нет в наличии!')


if __name__ == '__main__':
    mode = 0  # 0 - Инициализация списка мулине, 1 - IO проверка мулине в списке

    match mode:
        case 0: init_my_floss()
        case 1: real_time_floss_check()
