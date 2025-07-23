# -*- coding: utf-8 -*-
__author__ = "Самков Н.А. https://github.com/NikitaSamkov"
__maintainer__ = "Самков Н.А. https://github.com/NikitaSamkov"
__doc__ = "Классы для чтения и записи схемы"

import struct
from abc import ABC


class XSDFileReader:
    """Чтение и запись .xsd файла"""
    def __init__(self, file_path: str, mode: str):
        self.file = open(file_path, mode + 'b')

    def close(self):
        self.file.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    def find_end_symbol(self, bytes_):
        for i, byte in enumerate(bytes_):
            if byte == 0x00:
                return i
        return len(bytes_)

    # Методы чтения
    def read(self, size: int):
        return self.file.read(size)

    def read_all(self):
        return self.file.read()

    def read_byte(self):
        return self.read(1)[0]

    def read_unsigned_byte(self):
        return self.read(1)[0]

    def read_int16(self):
        chars = self.read(2)
        if len(chars) < 2:
            raise EOFError
        return struct.unpack('<H', chars)[0]

    def read_str(self, size: int):
        bytes_ = self.read(size)
        return str(bytes_[:self.find_end_symbol(bytes_)].decode('utf-8', errors='ignore'))

    def read_color(self):
        return list(self.read(3))

    # Методы записи
    def write(self, value):
        self.file.write(value)

    def write_unsigned_byte(self, value: int):
        self.write(bytes([value & 0xFF]))

    def write_byte(self, value: int):
        self.write(bytes([value & 0xFF]))

    def write_int16(self, value: int):
        self.write(struct.pack('<H', value))

    def write_str(self, value: str, size: int = 0):
        encoded_value = value.encode('utf-8')
        self.write(encoded_value)
        # Добавляем нулевой байт в конце строки
        self.write(b'\x00')
        if size > len(encoded_value) + 1:
            for _ in range(size - len(encoded_value) - 1):
                self.write(b'\x00')

    def write_color(self, color: list[int]):
        self.write(bytes(color))


class XSDEntity(ABC):
    """Абстрактный класс сущности схемы"""
    def __init__(self, reader: XSDFileReader):
        """Чтение сущности"""
        pass

    def save(self, reader: XSDFileReader):
        """Сохранение данных"""
        pass


class Header(XSDEntity):
    """Заголовок схемы"""
    def __init__(self, reader: XSDFileReader):
        # Байты заголовка, которые как бы не относятся к палитре
        self.start_bytes = reader.read(761)
        self.palette_size = reader.read_int16()

    def save(self, reader: XSDFileReader):
        """Сохранение заголовка"""
        reader.write(self.start_bytes)
        reader.write_int16(self.palette_size)


class BlendColor(XSDEntity):
    """Смесь цветов"""
    def __init__(self, reader: XSDFileReader):
        self.floss_code = reader.read_unsigned_byte()
        self.floss_number = reader.read_str(11)

    def save(self, reader: XSDFileReader):
        """Сохранение"""
        reader.write_unsigned_byte(self.floss_code)
        reader.write_str(self.floss_number, 11)


class PatternFloss(XSDEntity):
    """Мулине в схеме"""
    def __init__(self, reader: XSDFileReader):
        # Неинтересующие нас байты
        self.start_bytes = reader.read(2)

        self.code = reader.read_unsigned_byte()
        self.number = reader.read_str(11)
        self.name = reader.read_str(41)
        self.color = reader.read_color()
        self.available_flag = reader.read_byte()
        self.blend_count = reader.read_int16()
        self.blends = [BlendColor(reader) for _ in range(4)]
        self.blend_strands = [reader.read_byte() for _ in range(4)]
        self.bead_flag = reader.read_byte()

        # Неинтересующие нас байты
        self.end_bytes = reader.read(9)

        self.is_blend = self.code == 252

    def save(self, reader: XSDFileReader):
        """Сохранение цвета"""
        reader.write(self.start_bytes)
        reader.write_unsigned_byte(self.code)
        reader.write_str(self.number, 11)
        reader.write_str(self.name, 41)
        reader.write_color(self.color)
        reader.write_byte(self.available_flag)
        reader.write_int16(self.blend_count)
        for blend in self.blends:
            blend.save(reader)
        for strand in self.blend_strands:
            reader.write_byte(strand)
        reader.write_byte(self.bead_flag)
        reader.write(self.end_bytes)


class XSDPatternReader:
    """Парсинг и запись схемы"""
    def __init__(self, file_path: str):
        with XSDFileReader(file_path, 'r') as reader:
            self.header = Header(reader)
            self.palette = [PatternFloss(reader) for _ in range(self.header.palette_size)]

            # Неинтересующие нас байты
            self.rest_data = reader.read_all()

    def save(self, path: str):
        with XSDFileReader(path, 'w') as reader:
            self.header.save(reader)
            for floss in self.palette:
                floss.save(reader)
            reader.write(self.rest_data)
