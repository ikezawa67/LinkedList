'''linked list module'''
from .singly_linked_list import List as SinglyLinkedList, Node as SinglyLinkedNone
from .doubly_linked_list import List as DoublyLinkedList, Node as DoublyLinkedNode
from .singly_circularly_linked_list import List as SinglyCircularlyLinkedList, Node as SinglyCircularlyLinkedNone
from .doubly_circularly_linked_list import List as DoublyCircularlyLinkedList, Node as DoublyCircularlyLinkedNode

SinglyLinkedList.__name__ = 'SinglyLinkedList'
SinglyLinkedNone.__name__ = 'SinglyLinkedNone'
DoublyLinkedList.__name__ = 'DoublyLinkedList'
DoublyLinkedNode.__name__ = 'DoublyLinkedNode'
SinglyCircularlyLinkedList.__name__ = 'SinglyCircularlyLinkedList'
SinglyCircularlyLinkedNone.__name__ = 'SinglyCircularlyLinkedNone'
DoublyCircularlyLinkedList.__name__ = 'DoublyCircularlyLinkedList'
DoublyCircularlyLinkedNode.__name__ = 'DoublyCircularlyLinkedNode'

__all__ = [
    'SinglyLinkedList', 'SinglyLinkedNone',
    'DoublyLinkedList', 'DoublyLinkedNode',
    'SinglyCircularlyLinkedList', 'SinglyCircularlyLinkedNone',
    'DoublyCircularlyLinkedList', 'DoublyCircularlyLinkedNode',
]
