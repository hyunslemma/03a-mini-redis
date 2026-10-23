"""배열 인덱스와 직접 구현한 상향/하향 조정으로 동작하는 최소 힙."""


class MinHeap:
    """(우선순위, 값) 쌍을 저장한다. 동순위 값의 반환 순서는 보장하지 않는다."""

    def __init__(self):
        self._items = []

    def __len__(self):
        return len(self._items)

    def push(self, priority, value):
        """끝에 쌍을 추가하고 부모보다 우선순위가 작은 동안 위로 올린다."""
        self._items.append((priority, value))
        child = len(self._items) - 1
        while child > 0:
            parent = (child - 1) // 2
            if self._items[parent][0] <= self._items[child][0]:
                break
            self._items[parent], self._items[child] = (
                self._items[child], self._items[parent]
            )
            child = parent

    def peek(self):
        """최솟값 쌍을 제거 없이 반환한다. 비어 있으면 None을 반환한다."""
        return None if len(self._items) == 0 else self._items[0]

    def pop(self):
        """루트를 꺼내고 마지막 쌍을 내려 보내 힙 순서를 회복한다."""
        if len(self._items) == 0:
            return None
        result = self._items[0]
        last = self._items.pop()
        if len(self._items) == 0:
            return result
        self._items[0] = last
        parent = 0
        size = len(self._items)
        while parent * 2 + 1 < size:
            child = parent * 2 + 1
            right = child + 1
            if right < size and self._items[right][0] < self._items[child][0]:
                child = right
            if self._items[parent][0] <= self._items[child][0]:
                break
            self._items[parent], self._items[child] = (
                self._items[child], self._items[parent]
            )
            parent = child
        return result
