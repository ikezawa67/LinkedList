import time
from typing import MutableSequence
from linked_list import *

ELEMENT_COUNT = 10000


def list_performance_check(_list: MutableSequence, _print: bool = False):
    '''list performance check method'''
    print(f'{_list.__class__.__name__}, element count {ELEMENT_COUNT}')
    start = time.time()
    for i in range(ELEMENT_COUNT):
        _list.append(i)
    print(f'\tappend time: {time.time() - start}')
    if _print:
        print(f'\t{_list}')
    start = time.time()
    _list.reverse()
    print(f'\treverse time: {time.time() - start}')
    if _print:
        print(f'\t{_list}')
    start = time.time()
    _list.clear()
    print(f'\tclear time: {time.time() - start}')
    if _print:
        print(f'\t{_list}')
    tmp = [i for i in range(ELEMENT_COUNT)]
    start = time.time()
    _list.extend(tmp)
    print(f'\textend time: {time.time() - start}')
    if _print:
        print(f'\t{_list}')
    start = time.time()
    for _i in _list:
        if _print:
            print(f'\t{_i}', end=' ')
    if _print:
        print()
    print(f'\tfor time: {time.time() - start}')
    start = time.time()
    for _i in reversed(_list):
        if _print:
            print(f'\t{_i}', end=' ')
    if _print:
        print()
    print(f'\tfor reversed time: {time.time() - start}')


list_performance_check(list())
list_performance_check(SinglyLinkedList())
list_performance_check(DoublyLinkedList())
list_performance_check(SinglyCircularlyLinkedList())
list_performance_check(DoublyCircularlyLinkedList())
