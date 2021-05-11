class Element:
    def __init__(self, k, v, i):
        self._key = k
        self._value = v
        self._index = i

    def __str__(self):
        return "k: %i, v: %s, i: %i" % (self._key, self._value, self._index)

    __repr__ = __str__

    def getKey(self):
        return self._key

    def setKey(self, newKey):
        self._key = newKey

    key = property(getKey, setKey)

    def getValue(self):
        return self._value

    def setValue(self, newValue):
        self._value = newValue

    value = property(getValue, setValue)

    def getIndex(self):
        return self._index

    def setIndex(self, newIndex):
        self._index = newIndex

    index = property(getIndex, setIndex)

    def __eq__(self, other):
        return self._key == other.getKey()

    def __lt__(self, other):
        return self._key < other.getKey()

    def __gt__(self, other):
        return self._key > other.getKey()

class APQ:
    def __init__(self):
        self._binaryHeap = []  # create your heap

    def __str__(self):
        allTheItemsFitToPrint = ""  # yes, I'm making a NY Times reference
        for item in self._binaryHeap:
            allTheItemsFitToPrint += ("Key: %i, \t Value: %s, \t Index: %i" % (item.key, item.value, item.index)) + "\n"
        return allTheItemsFitToPrint

    __repr__ = __str__

    def length(self):
        return self._binaryHeap.__len__()  # predefined method

    def isEmpty(self):
        if self.length() == 0:
            return True  # if no stuff in heap
        return False  # if stuff in heap

    def min(self):
        minItem = self._binaryHeap[0]  # find the first item
        return minItem.value  # return its value

    def getKey(self, item):
        rightItem = self._binaryHeap[item.index]
        return rightItem.key

    def updateKey(self, item, updatedKey):
        oldKey = item.key  # keep track of info
        item.key = updatedKey  # reassignment
        if oldKey < updatedKey:
            self.bubbleDown(item)  # if it should be a child
        self.bubbleUp(item)  # if it should be a parent

    def add(self, key, item):
        index = self.length()  # values go from 0 to length - 1 so new index is same as the length
        itemIn = Element(key, item, index)  # we now have enough pieces
        if self.isEmpty():  # one lonely heap occupant
            self._binaryHeap += [itemIn]  # only item so no need to sort
        else:
            self._binaryHeap += [itemIn]  # adding item onto the end of the list
            self.bubbleUp(itemIn)  # need to make sure that it gets moved up when it has a low key
        return itemIn  # spits out an element at the end

    def swap(self, item1, item2):
        index1, index2 = item1.index, item2.index  # get the indexes of the two relevant items
        self._binaryHeap[index1], self._binaryHeap[index2] = item2, item1
        # move the key, value parts of the items into the right place
        item1.index, item2.index = index2, index1  # now we swap the indexes seeing as the parent/child have swapped

    @staticmethod
    def parentIndex(item):
        parentIndex = (item.index - 1) // 2
        return parentIndex

    def parent(self, item):
        parentIndex = self.parentIndex(item)
        parent = self._binaryHeap[parentIndex]
        return parent

    @staticmethod
    def leftIndex(index):
        leftIndex = (2 * index) + 1
        return leftIndex

    @staticmethod
    def rightIndex(index):
        rightIndex = (2 * index) + 2
        return rightIndex

    def bubbleUp(self, itemUp):
        parentIndex = self.parentIndex(itemUp)  # find what the parent's index is
        if 0 <= parentIndex < self.length() - 1:  # is the index within the list
            parent = self.parent(itemUp)  # get the parent of the current item
            if parent.key > itemUp.key:  # are the keys in the right place
                self.swap(itemUp, parent)  # if not the swap them into the correct place
                self.bubbleUp(itemUp)  # repeat recursively until the item is where it should be
        return self._binaryHeap  # spits the heap back out

    def bubbleDown(self, itemDown):
        index = itemDown.index
        leftIndex, rightIndex = self.leftIndex(index), self.rightIndex(index)
        if rightIndex < self.length():
            leftChild, rightChild = self._binaryHeap[leftIndex], self._binaryHeap[rightIndex]
            if leftChild and rightChild:
                if leftChild.key < rightChild.key:
                    if itemDown > self._binaryHeap[leftIndex]:
                        self.swap(itemDown, leftChild)
                        self.bubbleDown(itemDown)
                elif rightChild.key < leftChild.key:
                    if itemDown.key > rightChild.key:
                        self.swap(itemDown, rightChild)
                        self.bubbleDown(itemDown)
        elif leftIndex < self.length():
            leftChild = self._binaryHeap[leftIndex]
            if itemDown.key > leftChild.key:
                self.swap(itemDown, leftChild)
                self.bubbleDown(itemDown)
        return self._binaryHeap

    # Write the code to remove the items from the list and realign the indexes

    def removeMin(self):
        if not self.isEmpty():  # do we have something to remove
            itemOut = self._binaryHeap[0]
            if self.length() == 1:
                self._binaryHeap.pop(0)
            else:
                self.swap(self._binaryHeap[0], self._binaryHeap[-1])  # swap the min item to the back of the list
                self._binaryHeap.pop(-1)  # more efficient to pop off the end
                self.bubbleDown(self._binaryHeap[0])  # put the current minimum item to where it belongs
            return itemOut
        return None  # can't remove anything if nothing's left there

    def remove(self, itemOut):
        if not self.isEmpty():  # do we have stuff to remove
            currentIndex = itemOut.index  # save the index for later
            self.swap(itemOut, self._binaryHeap[-1])  # move item on the chopping block to the end of the heap
            self._binaryHeap.pop(-1)  # kick it off the heap
            self.bubbleDown(self._binaryHeap[currentIndex])
            # push this item back down the heap seeing as it was at the end anyway
            return itemOut  # return removed item
        return None  # return None if empty
