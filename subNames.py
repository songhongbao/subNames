#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
    subNames 1.0
    Names combination tool
    shy[at]ranshy.com
"""

import optparse
import sys
import lunarcalendar

reload(sys)
sys.setdefaultencoding('utf8')


class SubNames:
    def __init__(self, info):
        self.split = '!@#$%&*_+-=/.\\\''
        self.combination = []
        self.length = info.length
        self._load_name(info.xing, info.ming, info.en_name)
        print len(self.combination)
        self._load_birthday(info.birthday)
        print len(self.combination)
        self._load_company(info.company)
        print len(self.combination)
        print self.combination
        # print self.names

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
                combination.append(_a + _b)
                combination.append(_b + _a)
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
            rules = [lambda s: any(x.isupper() for x in s),
                     lambda s: any(x.isdigit() for x in s),
                     lambda s: any(x in self.split for x in s)
                     ]
            num = sum([int(rule(value)) for rule in rules])
            if num > 1:
                continue
            filter_combination.append(value)
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
        name_combination += self.combine(xing, ming, name_split)
        name_combination += self.combine(xing, en_name, name_split)
        name_combination += self.combine(ming, en_name, name_split)
        name_combination = list(set(name_combination))
        self.names = self.save(name_combination)
        self.save(self.combine(self.names, en_name, name_split))

    def _load_birthday(self, birthday):
        birthday_combination = []
        birthday_split = '._-@!#'
        if birthday.isdigit():
            if len(birthday) == 8:
                for birth in [birthday, lunarcalendar.get_ludar_date(birthday)]:
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
        company_split = '@/.'
        self.company = [company.lower(), company.capitalize()]
        self.save(self.combine(self.names, self.company, company_split))

if __name__ == '__main__':
    args = ['-x', 'teng', '-m', 'jun', '-e', 'nick', '-b', '19890624', '-c', 'intsig']
    msg = '-x zhang -m san -e Tony -b 19940509 -l apple -c google'
    parser = optparse.OptionParser('usage: %prog ' + msg, version="%prog 1.0")
    parser.add_option('-x', '--xing', dest='xing', default='', type='string', help='姓')
    parser.add_option('-m', '--ming', dest='ming', default='', type='string', help='名')
    parser.add_option('-e', '--en', dest='en_name', default='', type='string', help='英文名')
    parser.add_option('-b', '--birthday', dest='birthday', default=None, type='string', help='出生日期（阳历）')
    parser.add_option('-c', '--company', dest='company', default=None, type='string', help='公司')
    parser.add_option('--length', dest='length', default=6, type='int', help='密码长度')
    (options, args) = parser.parse_args(args)
    d = SubNames(options)

