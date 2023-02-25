# LinkedList

これは、Pythonで実装したリンクドリストのモジュールです。

## 実装環境

Windows 11 64bit

Python 3.11.1 64bit

## 実装したリンクドリスト一覧

* singly_linked_list（片方向リスト）
  * SinglyLinkedList
  * SinglyLinkedNone
* doubly_linked_list（双方向リスト）
  * DoublyLinkedList
  * DoublyLinkedNode
* singly_circularly_linked_list（片方向循環リスト）
  * SinglyCircularlyLinkedList
  * SinglyCircularlyLinkedNone
* doubly_circularly_linked_list（双方向循環リスト）
  * DoublyCircularlyLinkedList
  * DoublyCircularlyLinkedNode

## 使用方法

```python
from linked_list import SinglyLinkedList


list = SinglyLinkedList([0, 1, 2, 3, 4])
print(list)  # [0, 1, 2, 3, 4]
print(list[0] == 0)  # True

```
