#! /usr/bin/env python

import numpy as np
import sys

def fastaparser(path):
    book = {}
    with open(path, 'r') as file:
        for line in file:
            line = line.strip()
            if line.startswith('>'):
                key = line
                book[line] = ''
            else:
                book[key] += line
    return dict(sorted(book.items()))

def al_encoding_gn(book): #gn - GapNumbers
    enc = {}
    for h in book.items():
        dws = []
        last = 0
        flag = True
        for elem in h[1].split('-'):
            if elem == '':
                dws.append(last)
            else:
                to_app = range(last+1, len(elem)+last+1)
                dws.extend(np.array(to_app))
                last = to_app[-1]
                dws.append(last)
                flag = True
        enc[h[0]] = dws
    return enc

def to_mx(encoded_book):
    return np.array([np.array(k) for k in encoded_book.values()])

def comparison(alA, alB):
    counter = 0
    samecols = []
    for r in range(min(len(alA.T), len(alB.T))):
        if np.array_equal(alA.T[r], alB.T[r]) == True:
            samecols.append(r)
            counter += 1
    return counter/min(len(alA), len(alB)), np.array(samecols)

if sys.argv[1] == '-f':
    print('Программа malvsmal сравнивает два множественных выравнивания.',
'На вход в качестве аргументов 1 и 2 принимаются два множественных выравнивания в формате fasta.', 'Названия выровненных последовательностей в файлах должны совпадать, это важно для сортировки словарей по ключам.', 'Выходной файл содержит долю совпавших колонок и список их индексов.', sep='\n')
    sys.exit()

path1 = sys.argv[1]
path2 = sys.argv[2]

f1 = fastaparser(path1)
f2 = fastaparser(path2)
f1 = al_encoding_gn(f1)
f2 = al_encoding_gn(f2)
f1 = to_mx(f1)
f2 = to_mx(f2)
with open('malvsmal.out',  'w') as out:
    res = comparison(f1, f2)
    print(f'Процент совпадений: {res[0]}', file = out)
    print(f'Список совпавших колонок: {res[1]}', file = out)
