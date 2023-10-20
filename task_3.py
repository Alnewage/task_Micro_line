'''
Задание: https://docs.google.com/document/d/1QrGQ_KR2N4duvgv5QS7d3S1fbkWCaLN7BClH59VoQLc/edit
'''

import struct
import zlib

# Заголовок пакета (в виде байтов)
header = b'\x01\x00\x03\x0B\x00\x13\x00\x86\x00\x01'


# Создание класса для работы с протоколом EGTS
class EGTSProtocol:
    def __init__(self):
        self.packet = b''
        self.authenticated = False  # Флаг авторизации

    def receive_packet(self, data):
        self.packet += data

    def parse_packet(self):
        while len(self.packet) >= 10:  # Минимальный размер пакета
            packet_header = self.packet[:10]  # Исправленная строка

            # Разбор заголовка
            prv, skid, prf, hl, he, fdl, pid, pt = struct.unpack(
                'B B B B B H H B B', packet_header + b'\x00')

            # Проверка контрольной суммы заголовка
            if self.check_header_checksum(packet_header):
                data = self.packet[10:10 + fdl]

                # Объединение пакетов, если fdl меньше полного размера данных
                if len(data) < fdl:
                    while len(data) < fdl:
                        self.packet = self.packet[10:]
                        data += self.packet[:fdl - len(data)]
                        self.packet = self.packet[fdl - len(data):]

                # Определение типа пакета
                if pt == 1:
                    auth_packet = AuthPacket(data)
                    if not self.authenticated:
                        self.authenticated = auth_packet.authenticate()
                        if self.authenticated:
                            print("Авторизация успешна.")
                    useful_data = auth_packet.parse_auth_packet()
                elif pt == 2:
                    if self.authenticated:
                        data_packet = DataPacket(data)
                        useful_data = data_packet.parse_data_packet()
                        if useful_data:
                            print(f"Получены данные: {useful_data}")
                    else:
                        print("Ошибка: Данные не могут быть обработаны "
                              "до авторизации.")
                        useful_data = None

                if useful_data is not None:
                    # Обработка полезных данных.
                    pass

                # Удаление обработанных данных из пакета
                self.packet = self.packet[10 + fdl:]
            else:
                # Некорректная контрольная сумма, игнорируем пакет
                self.packet = self.packet[10:]

            def check_header_checksum(self, header):
                hcs = struct.unpack('B', header[-2:-1])[0]
                calculated_hcs = zlib.crc32(header[:-2]) & 0xFF

                # Проверка контрольной суммы заголовка
                return calculated_hcs == hcs

                # Создание класса для работы с авторизационными пакетами.

            class AuthPacket:
                def __init__(self, data):
                    self.data = data

                def authenticate(self):
                    # Пример авторизации: Проверка, что в данных
                    # есть ключ "authorized".
                    if b'authorized' in self.data:
                        return True
                    return False

                def parse_auth_packet(self):
                    # Разбор данных авторизации
                    useful_data = self.data
                    return useful_data

                # Создание класса для работы с пакетами данных

            class DataPacket:
                def __init__(self, data):
                    self.data = data

                def parse_data_packet(self):
                    # Пример разбора данных:
                    # попросту возвращаем данные как есть.
                    useful_data = self.data
                    return useful_data

                # Создание экземпляра протокола EGTS

            egts_protocol = EGTSProtocol()

            # Получение пакета данных
            egts_protocol.receive_packet(header + b'data packet')

            # Парсинг пакета данных
            egts_protocol.parse_packet()
