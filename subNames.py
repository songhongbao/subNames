#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
    subNames 1.0
    Names combination tool
    shy[at]ranshy.com
"""

import optparse
import sys
import nongli

reload(sys)
sys.setdefaultencoding('utf8')


class SubNames:
    def __init__(self, info):
        self.split = '!@#$%&*_+-=/.\\\''
        self.combination = []
        self.length = info.length
        self._load_name(info.xing, info.ming, info.en_name)
        self._load_birthday(info.birthday)
        self._load_company(info.company)
        self._load_love(info.love)
        # print len(self.combination)

    def output(self, file_name='result'):
        level_1 = ''
        level_2 = ''
        level_3 = ''
        level_4 = ''
        rules = [lambda s: any(x.isupper() for x in s),
                 lambda s: any(x.islower() for x in s),
                 lambda s: any(x.isdigit() for x in s),
                 lambda s: any(x in self.split for x in s)
                 ]
        for value in self.combination:
            level = sum([int(rule(value)) for rule in rules])
            if level == 1:
                level_1 += value + "\n"
            elif level == 2:
                level_2 += value + "\n"
            else:
                level_3 += value + "\n"
        f = open(file_name + '_1.txt', 'w')
        f.write(level_1)
        f = open(file_name + '_2.txt', 'w')
        f.write(level_2)
        f = open(file_name + '_3.txt', 'w')
        f.write(level_3)

    @staticmethod
    def load_file(file_name):
        data = []
        with open(file_name) as f:
            for line in f:
                if line.strip() != '':
                    data.append(line.strip())
        return data

    def combine(self, a, b, split):
        combination = []
        if not a or not b:
            return combination
        for _a in a:
            for _b in b:
                # upper combine upper filter
                if any(x.isupper() for x in _a) and any(x.isupper() for x in _a) and any(x.islower() for x in str(_a + _b)):
                    continue
                combination.append(_a + _b)
                combination.append(_b + _a)
                # split char only once filter
                if list(set(_a).intersection(set(self.split))) or list(set(_b).intersection(set(self.split))):
                    continue
                for _split in split:
                    combination.append(_a + _split + _b)
                    combination.append(_b + _split + _a)
        return combination

    def parse_pinyin(self, pinyin):
        pinyin = pinyin.lower()
        pinyin_list = self.load_file('dict/pinyin.txt')
        combination = []
        length = 5
        while length:
            if pinyin[0:length] in pinyin_list:
                combination = [pinyin[0:length] + pinyin[length:],
                               pinyin[0:length].capitalize() + pinyin[length:],
                               # pinyin[0:length].capitalize() + pinyin[length:].capitalize(),
                               # pinyin[0:length].upper() + pinyin[length:].upper(),
                               pinyin[0:1] + pinyin[length:length + 1],
                               pinyin[0:1].upper() + pinyin[length:length + 1].upper()
                               ]
                break
            length -= 1
        '''
        if len(pinyin) > 2:
            combination.append(pinyin[0:1])
            combination.append(pinyin[0:2])
        '''
        return list(set(combination))

    def save(self, combination):
        filter_combination = []
        for value in combination:
            if len(value) > 14:
                continue
            if len(value) > self.length:
                self.combination.append(value)
            # filter: length_max 12, diff type
            if len(value) > 12:
                continue
            rules = [lambda s: sum([int(x.isupper()) for x in s]),
                     lambda s: any(x.isdigit() for x in s),
                     lambda s: sum([int(x in self.split) for x in s])
                     ]
            num = sum([int(rule(value)) for rule in rules])
            if num > 1:
                continue
            filter_combination.append(value)
        self.combination = list(set(self.combination))
        return filter_combination

    def _load_name(self, xing, ming, en_name):
        name_combination = []
        name_split = '._-'
        xing = self.parse_pinyin(xing)
        ming = self.parse_pinyin(ming)
        if en_name:
            en_name = [en_name.lower(), en_name.capitalize()]
        else:
            en_name = []
        name_combination += xing
        name_combination += ming
        name_combination += en_name
        name_combination += self.combine(xing, ming, name_split)
        self.save(self.combine(name_combination, en_name, name_split))
        name_combination += self.combine(xing, en_name, name_split)
        name_combination += self.combine(ming, en_name, name_split)
        name_combination = list(set(name_combination))
        self.names = self.save(name_combination)

    def _load_birthday(self, birthday):
        birthday_combination = []
        birthday_split = '._-@!#'
        if birthday.isdigit():
            if len(birthday) == 8:
                for birth in [birthday, nongli.get_nongli(birthday)]:
                    birthday_combination += [birth[0:4], birth[4:], birth[0:]]
                    birthday_combination += [str(int(birth[4:6])) + str(int(birth[6:8]))]
                    # birth[0:4] + str(int(birth[4:6])) + str(int(birth[6:8]))]
            elif len(birthday) == 4:
                birthday_combination += [birthday]
                if int(birthday[0:2]) <= 12:
                    birthday_combination += [str(int(birthday[0:2])) + str(int(birthday[2:4]))]
        self.birthday = list(set(birthday_combination))
        self.save(self.combine(self.names, self.birthday, birthday_split))

    def _load_company(self, company):
        company_split = '@/_.'
        self.company = [company.lower(), company.capitalize()]
        self.save(self.combine(self.names, self.company, company_split))

    def _load_love(self, love):
        love_split = '@_/.'
        love_combination = []
        love_combination += list('0123456789')
        # love_combination += list('abcdefghijklmnopqrstuvwxyz')
        # love_combination += list('abcdefghijklmnopqrstuvwxyz'.upper())
        love_combination += ['123', '132', '213', '231', '312', '321', '1234', '12345', '123456', '521', '1314']
        if love not in love_combination:
            love_combination.append(love)
        self.save(self.combine(self.names, love_combination, love_split))
        self.save(self.combine(self.birthday, love_combination, love_split))
        self.save(self.combine(self.company, love_combination, love_split))

if __name__ == '__main__':
    msg = '-x zhang -m san -e Tony -b 19940509 -l apple -c google -l apple'
    parser = optparse.OptionParser('usage: %prog ' + msg, version="%prog 1.0")
    parser.add_option('-x', '--xing', dest='xing', default='', type='string', help='姓')
    parser.add_option('-m', '--ming', dest='ming', default='', type='string', help='名')
    parser.add_option('-e', '--en', dest='en_name', default='', type='string', help='英文名')
    parser.add_option('-b', '--birthday', dest='birthday', default='', type='string', help='出生日期（阳历）')
    parser.add_option('-c', '--company', dest='company', default='', type='string', help='公司')
    parser.add_option('-l', '--love', dest='love', default='', type='string', help='喜爱')
    parser.add_option('--length', dest='length', default=6, type='int', help='密码最小长度，默认为6位')
    (options, args) = parser.parse_args()
    sub_names = SubNames(options)
    sub_names.output()


