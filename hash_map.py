"""직접 계산한 문자열 해시와 이중 연결 리스트 체이닝을 쓰는 해시맵."""

from linked_list import LinkedList


class HashMap:
    """문자열 키/값 저장소. 버킷 배열은 인덱스 읽기·쓰기와 길이만 사용한다."""

    def __init__(self, capacity=8):
        if capacity < 1:
            raise ValueError("capacity must be positive")
        self._buckets = [None] * capacity
        self._size = 0

    def __len__(self):
        return self._size

    @property
    def capacity(self):
        return len(self._buckets)

    @property
    def load_factor(self):
        return self._size / self.capacity

    @staticmethod
    def _hash_key(key):
        """문자 순서를 반영하는 31진 누적값을 매 단계 32비트로 제한한다."""
        value = 0
        for char in key:
            value = (value * 31 + ord(char)) & 0xFFFFFFFF
        return value

    def bucket_index(self, key):
        """동작 확인용: 현재 버킷 수에 대한 인덱스를 반환한다."""
        return self._hash_key(key) % self.capacity

    def _find_node(self, key):
        """해당 버킷의 노드를 직접 비교하며 탐색한다."""
        bucket = self._buckets[self.bucket_index(key)]
        node = None if bucket is None else bucket.head
        while node is not None:
            if node.data[0] == key:
                return node
            node = node.next
        return None

    def put(self, key, value):
        """문자열 쌍을 저장한다. 새 키 저장 직후에만 확장 여부를 판단한다."""
        if not isinstance(key, str) or not isinstance(value, str):
            raise TypeError("keys and values must be strings")
        node = self._find_node(key)
        if node is not None:
            node.data = (key, value)
            return
        slot = self.bucket_index(key)
        if self._buckets[slot] is None:
            self._buckets[slot] = LinkedList()
        self._buckets[slot].append_right((key, value))
        self._size += 1
        # 부동소수점 반올림 없이 size / capacity > 0.75를 검사한다.
        if self._size * 4 > self.capacity * 3:
            self._resize()

    def get(self, key):
        """키가 없으면 None, 있으면 저장된 문자열(빈 문자열 포함)을 반환한다."""
        node = self._find_node(key)
        return None if node is None else node.data[1]

    def contains(self, key):
        """내장 멤버십 연산 없이 키 존재 여부를 확인한다."""
        return self._find_node(key) is not None

    def delete(self, key):
        """키가 있으면 제거하고 True, 없으면 False를 반환한다."""
        node = self._find_node(key)
        if node is None:
            return False
        slot = self.bucket_index(key)
        bucket = self._buckets[slot]
        bucket.remove(node)
        if len(bucket) == 0:
            self._buckets[slot] = None
        self._size -= 1
        return True

    def keys(self):
        """모든 버킷과 체인을 직접 순회한다. 키 순서는 보장하지 않는다."""
        slot = 0
        while slot < self.capacity:
            bucket = self._buckets[slot]
            node = None if bucket is None else bucket.head
            while node is not None:
                yield node.data[0]
                node = node.next
            slot += 1

    def _resize(self):
        """2배 크기의 새 배열에 모든 쌍을 재배치하고 마지막에 교체한다."""
        new_capacity = self.capacity * 2
        new_buckets = [None] * new_capacity
        slot = 0
        while slot < self.capacity:
            bucket = self._buckets[slot]
            node = None if bucket is None else bucket.head
            while node is not None:
                key, value = node.data
                new_slot = self._hash_key(key) % new_capacity
                if new_buckets[new_slot] is None:
                    new_buckets[new_slot] = LinkedList()
                new_buckets[new_slot].append_right((key, value))
                node = node.next
            slot += 1
        self._buckets = new_buckets
