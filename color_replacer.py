# -*- coding: utf-8 -*-
__author__ = "Самков Н.А. https://github.com/NikitaSamkov"
__maintainer__ = "Самков Н.А. https://github.com/NikitaSamkov"
__doc__ = "Замена цветов в палитре на ближайшие по RGB"

import json
from floss_getter import FLOSS_PATH
from my_floss import MY_FLOSS_PATH
from readers import XSDPatternReader, PatternFloss


class ColorReplacer:
    """Замена цветов палитры по ближайшим, которые есть у пользователя"""
    def __init__(self, pattern_reader: XSDPatternReader):
        self.pattern = pattern_reader
        with open(FLOSS_PATH, 'r', encoding='utf-8') as all_f, open(MY_FLOSS_PATH, 'r', encoding='utf-8') as my_f:
            all_floss = json.load(all_f)
            my_floss = json.load(my_f)
            self.my_floss = {floss: all_floss.get(floss) for floss in my_floss if floss in all_floss}
            self.floss = all_floss

    def get_nearest_my_floss(self, color: list[int]) -> str:
        """Поиск ближайшего цвета переданному среди тех, что в наличии"""
        def get_distance(floss):
            """Нахождение расстояния между двумя цветами"""
            return sum((a - b) ** 2 for a, b in zip(color, floss[1].get('RGB')))

        return min(self.my_floss.items(), key=get_distance)[0]

    def replace_color(self, floss: PatternFloss):
        """Замена цвета ближайшим по RGB"""
        if floss.number in self.my_floss:
            return
        if floss.is_blend:
            self.replace_blend_color(floss)
            return
        my_floss_num = self.get_nearest_my_floss(floss.color)
        my_floss = self.my_floss.get(my_floss_num)
        floss.number = my_floss_num
        floss.name = my_floss.get('floss_name')
        floss.color = my_floss.get('RGB')

    def blend_color(self, floss: PatternFloss):
        """Миксует цвета"""
        blend_count = floss.blend_count
        color_sum = sum(map(lambda blend: self.floss.get(blend.floss_number).get('RGB'), floss.blends[:blend_count]),
                        start=[0, 0, 0])
        return [color // blend_count for color in color_sum]

    def replace_blend_color(self, floss: PatternFloss):
        """Замена смешанного цвета"""
        for blend in floss.blends[:floss.blend_count]:
            if blend.floss_number in self.my_floss:
                continue
            blend.floss_number = self.get_nearest_my_floss(self.floss.get(blend.floss_number).get('RGB'))
        self.blend_color(floss)

    def replace_palette(self):
        """Замена палитры на подходящие цвета из имеющихся у пользователя"""
        for floss in self.pattern.palette:
            self.replace_color(floss)
