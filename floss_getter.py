# -*- coding: utf-8 -*-
__author__ = "Самков Н.А. https://github.com/NikitaSamkov"
__maintainer__ = "Самков Н.А. https://github.com/NikitaSamkov"
__doc__ = "Модуль для получения информации о мулине"

import os
import json
import requests
from bs4 import BeautifulSoup


# Я решил взять этот URL для парсинга, т.к. официального сайта не нашёл, а данные меняются от источника к источнику
FLOSS_URL = 'https://floss.maxxmint.com/dmc_to_rgb.php'
FLOSS_PATH = os.path.join(os.path.dirname(__file__), 'floss.json')


def parse_dmc_table(url):
    """Парсит HTML-страницу"""
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find('table')

    if not table:
        return {}

    dmc_data = {}
    rows = table.find_all('tr')[1:]  # Исключаем первую строку (заголовок)

    for row in rows:
        cells = row.find_all('td')
        if len(cells) == 7:
            dmc_number = cells[1].text.strip()
            floss_name = cells[2].text.strip()
            hex_code = cells[3].text.strip()
            red = int(cells[4].text.strip())
            green = int(cells[5].text.strip())
            blue = int(cells[6].text.strip())

            dmc_data[dmc_number] = {
                'floss_name': floss_name,
                'hex_code': hex_code,
                'red': red,
                'green': green,
                'blue': blue,
                'RGB': [red, green, blue]
            }

    return dmc_data


def init_dmc_floss(url: str = FLOSS_URL):
    """Инициализация списка мулине DMC"""
    floss_data = parse_dmc_table(FLOSS_URL)
    with open(FLOSS_PATH, 'w', encoding='utf-8') as f:
        json.dump(floss_data, f, indent=2, ensure_ascii=False)


if __name__ == '__main__':
    init_dmc_floss()
