#!/usr/bin/env python3
import argparse
import datetime
import random


class Prototype:
    ALPHABET = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

    def __init__(self, symbol):
        MAP = {'t': self._randomText, 'T': self._randomTimestamp, 'i': self._randomInteger}
        self.instance = MAP[symbol]

    def _randomText(self):
        return ''.join(random.choice(self.ALPHABET) for _ in range(10))

    def _randomInteger(self):
        return random.randint(1, 100000000)

    def _randomTimestamp(self):
        year = random.randint(1900, 2016)
        month = random.randint(1, 12)
        day = random.randint(1, 28)
        hour = random.randint(1, 23)
        minute = random.randint(0, 59)
        second = random.randint(0, 59)
        return datetime.datetime(year, month, day, hour, minute, second)


class GenerateCSV:
    def __init__(self, lines, pattern):
        self._prototypes = [Prototype(symbol) for symbol in pattern]
        for _ in range(lines):
            instances = self._generate()
            line = ','.join(str(instance) for instance in instances)
            print(line)

    def _generate(self):
        return [prototype.instance() for prototype in self._prototypes]


parser = argparse.ArgumentParser()
parser.add_argument('lines', type=int, help='number of lines to generate')
parser.add_argument('pattern', help='pattern of each line. Every character means some datatype, e.g. tiTt stands for text,integer,timedatmp,text')
arguments = parser.parse_args()

GenerateCSV(arguments.lines, arguments.pattern)
