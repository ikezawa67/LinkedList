import time
from linked_list import *

APPEND_NUMBER = 1000


def _append_timer(_list):
    start = time.time()
    for i in range(APPEND_NUMBER):
        _list.append(i)
    return time.time() - start


print(f'python list {APPEND_NUMBER} append time: \
    {_append_timer(list())}')
print(f'singly linked list {APPEND_NUMBER} append time: \
    {_append_timer(SinglyLinked())}')
print(f'doubly linked list {APPEND_NUMBER} append time: \
    {_append_timer(DoublyLinked())}')
print(f'singly circularly linked list {APPEND_NUMBER} append time: \
    {_append_timer(SinglyCircularlyLinkedList())}')
print(f'doubly circularly linked list {APPEND_NUMBER} append time: \
    {_append_timer(DoublyCircularlyLinkedList())}')
