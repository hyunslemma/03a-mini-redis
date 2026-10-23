"""이전/다음 참조와 소유자 확인을 사용하는 이중 연결 리스트."""


class Node:
    """리스트에 속한 동안 앞뒤 노드와 소유 리스트를 기억한다."""

    __slots__ = ("data", "prev", "next", "owner")

    def __init__(self, data):
        self.data = data
        self.prev = None
        self.next = None
        self.owner = None


class LinkedList:
    """노드 참조가 있으면 삽입·제거·맨 앞으로 이동을 O(1)에 처리한다."""

    def __init__(self):
        self.head = None
        self.tail = None
        self._size = 0

    def __len__(self):
        return self._size

    def append_left(self, data):
        """앞에 삽입하고, 이후 O(1) 제거/이동에 사용할 노드를 반환한다."""
        node = Node(data)
        node.owner = self
        node.next = self.head
        if self.head is None:
            self.tail = node
        else:
            self.head.prev = node
        self.head = node
        self._size += 1
        return node

    def append_right(self, data):
        """뒤에 삽입하고 새 노드 참조를 반환한다."""
        node = Node(data)
        node.owner = self
        node.prev = self.tail
        if self.tail is None:
            self.head = node
        else:
            self.tail.next = node
        self.tail = node
        self._size += 1
        return node

    def remove(self, node):
        """주어진 노드를 제거한다. 다른 리스트/이미 제거된 노드는 거부한다."""
        if node.owner is not self:
            raise ValueError("node does not belong to this list")
        if node.prev is None:
            self.head = node.next
        else:
            node.prev.next = node.next
        if node.next is None:
            self.tail = node.prev
        else:
            node.next.prev = node.prev
        node.prev = None
        node.next = None
        node.owner = None
        self._size -= 1
        return node.data

    def pop_left(self):
        """첫 값을 제거해 반환한다. 빈 리스트에서는 IndexError를 낸다."""
        if self.head is None:
            raise IndexError("pop from empty list")
        return self.remove(self.head)

    def pop_right(self):
        """마지막 값을 제거해 반환한다. 빈 리스트에서는 IndexError를 낸다."""
        if self.tail is None:
            raise IndexError("pop from empty list")
        return self.remove(self.tail)

    def move_to_front(self, node):
        """기존 노드의 정체성과 길이를 유지하며 맨 앞으로 이동한다."""
        if node.owner is not self:
            raise ValueError("node does not belong to this list")
        if node is self.head:
            return
        node.prev.next = node.next
        if node.next is None:
            self.tail = node.prev
        else:
            node.next.prev = node.prev
        node.prev = None
        node.next = self.head
        self.head.prev = node
        self.head = node

    def iter_forward(self):
        """앞에서부터 값을 순회한다. 순회 중 구조 변경은 지원하지 않는다."""
        node = self.head
        while node is not None:
            yield node.data
            node = node.next

    def iter_reverse(self):
        """뒤에서부터 값을 순회한다."""
        node = self.tail
        while node is not None:
            yield node.data
            node = node.prev
