


class MapKey:

    def __init__(self, key_value, link: DequeueNode):
        self.key_value = key_value
        self.link = link



class DequeueNode:

    def __init__(self, value):
        self.value = value
        self.prev = None
        self.next = None



class DequeueMap:

    # ======== Magic methods ========

    def __init__(self):
        self._map: dict[MapKey, DequeueNode] = {}
        self._head: DequeueNode = None
        self._tail: DequeueNode = None
        self._length: int = 0

    def __len__(self):
        return self._length

    def __getitem__(self, key):
        return self._map[key].value

    def __setitem__(self, key, value):
        node = self._map[key]
        node.value = value

    def __delitem__(self, key):
        node = self._map[key]
        node.prev.next = node.next
        node.next.prev = node.prev
        del self._map[key]
        self._length -= 1
    
    def __contains__(self, value):
        for item in self:
            if item == value:
                return True
        return False
    
    def __iter__(self):
        self.__iter_node = self._head
        return self
    
    def __next__(self):
        if self.__iter_node is None:
            raise StopIteration
        node = self.__iter_node
        self.__iter_node = node.next
        return node.value

    # ======== Queue methods ========
    
    def push(self, key, value):
        node = self._map.get(key)
        if node is None:
            node = DequeueNode(value)
            if self._head is None:
                # empty dequeue
                self._head = node
                self._tail = node
            else:
                # insert at tail
                self._tail.next = node
                node.prev = self._tail
                self._tail = node
            self._map[key] = node
            self._length += 1
        else:
            node.value = value
    
    def pushleft(self, key, value):
        node = self._map.get(key)
        if node is None:
            node = DequeueNode(value)
            if self._head is None:
                # empty dequeue
                self._head = node
                self._tail = node
            else:
                # insert at head
                self._head.prev = node
                node.next = self._head
                self._head = node
            self._map[key] = node
            self._length += 1
        else:
            node.value = value
    
    def pop(self):
        node = self._tail
        self._tail = node.prev
        self._tail.next = None
        del self._map[node.key_value]
        self._length -= 1

        return node.value
    
    def popleft(self):
        node = self._head
        self._head = node.next
        self._head.prev = None
        del self._map[node.key_value]
        self._length -= 1

        return node.value
    
    def peek(self):
        return self._head.value
    
    def peekright(self):
        return self._tail.value
    
    # ======== Map methods ========

    def keys(self):
        return self._map.keys()
    
    def values(self):
        return self._map.values()
    
    def items(self):
        return self._map.items()
    
    def get(self, key, default=None):
        return self._map.get(key, default)
    
    def setdefault(self, key, default=None):
        return self._map.setdefault(key, default)
    
    # ======== Specialist DequeueMap methods ========



    # ======== Utility methods ========

    def clear(self):
        self._map.clear()
        self._head = None
        self._tail = None
        self._length = 0
