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


class AdaptablePriorityQueue:
    def __init__(self):
        self._binaryHeap = []

    def __str__(self):
        allTheItemsFitToPrint = ""
        for item in self._binaryHeap:
            allTheItemsFitToPrint += ("Key: %i, \t Value: %s, \t Index: %i" % (item.key, item.value, item.index)) + "\n"
        return allTheItemsFitToPrint

    __repr__ = __str__

    def length(self):
        return self._binaryHeap.__len__()

    def isEmpty(self):
        if self.length() == 0:
            return True
        return False

    def min(self):
        minItem = self._binaryHeap[0]
        return minItem.value

    def getKey(self, item):
        rightItem = self._binaryHeap[item.index]
        return rightItem.key

    def updateKey(self, item, updatedKey):
        oldKey = item.key
        item.key = updatedKey
        if oldKey < updatedKey:
            self.bubbleDown(item)
        self.bubbleUp(item)

    def add(self, key, item):
        index = self.length()
        itemIn = Element(key, item, index)
        if self.isEmpty():
            self._binaryHeap += [itemIn]
        else:
            self._binaryHeap += [itemIn]
            self.bubbleUp(itemIn)
        return itemIn


    def swap(self, item1, item2):
        index1, index2 = item1.index, item2.index
        self._binaryHeap[index1], self._binaryHeap[index2] = item2, item1
        item1.index, item2.index = index2, index1

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
        parentIndex = self.parentIndex(itemUp)
        if 0 <= parentIndex < self.length() - 1:
            parent = self.parent(itemUp)
            if parent.key > itemUp.key:
                self.swap(itemUp, parent)
                self.bubbleUp(itemUp)
        return self._binaryHeap

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

    def removeMin(self):
        if not self.isEmpty():
            itemOut = self._binaryHeap[0]
            if self.length() == 1:
                self._binaryHeap.pop(0)
            else:
                self.swap(self._binaryHeap[0], self._binaryHeap[-1])
                self._binaryHeap.pop(-1)
                self.bubbleDown(self._binaryHeap[0])
            return itemOut
        return None

    def remove(self, itemOut):
        if not self.isEmpty():
            currentIndex = itemOut.index
            self.swap(itemOut, self._binaryHeap[-1])
            self._binaryHeap.pop(-1)
            self.bubbleDown(self._binaryHeap[currentIndex])
            return itemOut
        return None


class Vertex:
    def __init__(self, element):
        self._element = element

    def __str__(self):
        return str(self._element)

    __repr__ = __str__

    def __lt__(self, v):
        return self._element < v.element()

    def getElement(self):
        return self._element

    def setElement(self, newElement):
        self._element = newElement

    element = property(getElement, setElement)


class Edge:
    def __init__(self, v, w, element):
        self._vertices = (v, w)
        self._element = element

    def __str__(self):
        return ('(' + str(self._vertices[0]) + '--'
                + str(self._vertices[1]) + ' : '
                + str(self._element) + ')')

    __repr__ = __str__

    def vertices(self):
        return self._vertices

    def start(self):
        return self._vertices[0]

    def end(self):
        return self._vertices[1]

    def opposite(self, v):
        if self._vertices[0] == v:
            return self._vertices[1]
        elif self._vertices[1] == v:
            return self._vertices[0]
        else:
            return None

    def getElement(self):
        return self._element

    def setElement(self, newElement):
        self._element = newElement

    element = property(getElement, setElement)


class RouteMap:
    def __init__(self):
        self._structure = dict()  # {vertex:vertex}
        self._vertexCoordinates = dict()  # {vertex:coordinates}
        self._elementVertex = dict()  # {element:vertex}

    def __graphStr(self):
        heightString = ('|V| = ' + str(self.num_vertices())
                        + '; |E| = ' + str(self.num_edges()))
        vertexString = '\nVertices: '
        for v in self._structure:
            vertexString += str(v) + '-'
        edges = self.edges()
        edgeString = '\nEdges: '
        for e in edges:
            edgeString += str(e) + ' '
        return heightString + vertexString + edgeString

    def num_vertices(self):
        return self._structure.__len__()

    def num_edges(self):
        num = 0
        for v in self._structure:
            num += len(self._structure[v])
        return num // 2

    def vertices(self):
        return [key for key in self._structure]

    def get_vertex_by_label(self, element):
        if element in self._elementVertex.keys():
            return self._elementVertex[element]
        return None

    def edges(self):
        edgeList = []
        for v in self._structure:
            for w in self._structure[v]:
                if self._structure[v][w].start() == v:
                    edgeList += [self._structure[v][w]]
        return edgeList

    def get_edges(self, v):
        if v in self._structure:
            edgeList = []
            for w in self._structure[v]:
                edgeList += [self._structure[v][w]]
            return edgeList
        return None

    def get_edge(self, v, w):
        if self._structure is not None and v in self._structure and w in self._structure[v]:
            return self._structure[v][w]
        return None

    def degree(self, v):
        return len(self._structure[v])

    def add_edge(self, v, w, element):
        if v not in self._structure or w not in self._structure:
            return None
        e = Edge(v, w, element)
        self._structure[v][w] = e
        self._structure[w][v] = e
        return e

    def add_edge_pairs(self, eList):
        for (v, w) in eList:
            self.add_edge(v, w, None)

    def highestdegreevertex(self):
        highestDegree = -1
        highestDegreeVertex = None
        for v in self._structure:
            if self.degree(v) > highestDegree:
                highestDegree = self.degree(v)
                highestDegreeVertex = v
        return highestDegreeVertex

    def __str__(self):
        if (self.num_vertices() + self.num_edges()) <= 100:
            return self.__graphStr()

    def add_vertex(self, element, coords):
        v = Vertex(element)
        self._structure[v] = dict()
        self._elementVertex[element] = v
        self._vertexCoordinates[v] = coords
        return v

    def add_vertex_if_new(self, element, coords):
        for v in self._structure:
            if v.element() == element:
                return v
        return self.add_vertex(element, coords)

    def djikstra(self, s):
        opened = AdaptablePriorityQueue()
        locsDict, closedDict, predsDict = dict(), dict(), {s: None}
        itemIn = opened.add(0, s)
        locsDict[s] = itemIn
        while not opened.isEmpty():
            costOut = opened.removeMin()
            cost, vertex = costOut.key, costOut.value
            predecessor = predsDict.pop(vertex)
            locsDict.pop(vertex)
            closedDict[vertex] = (cost, predecessor)
            for edge in self.get_edges(vertex):
                oppositeVertex = edge.opposite(vertex)
                if oppositeVertex not in closedDict:
                    newCost = cost + edge.element
                    if oppositeVertex not in locsDict:
                        predsDict[oppositeVertex] = vertex
                        item = opened.add(newCost, oppositeVertex)
                        locsDict[oppositeVertex] = item
                    elif newCost < opened.getKey(locsDict[oppositeVertex]):
                        predsDict[oppositeVertex] = vertex
                        opened.updateKey(locsDict[oppositeVertex], newCost)
        return closedDict

    def sp(self, v, w):
        djikstra = self.djikstra(v)
        vertexCurrent = None
        out = []
        djikstraValue = djikstra[w]
        cost, vertexPredecessor = djikstraValue[0], djikstraValue[1]
        out += [(w, cost)]
        while vertexCurrent is not v:
            vertexCurrent = vertexPredecessor
            djikstraValue = djikstra[vertexPredecessor]
            cost, vertexPredecessor = djikstraValue[0], djikstraValue[1]
            out += [(vertexCurrent, cost)]
        result = out[::-1]
        return result

    def printvlist(self, path):
        pathway = "type, latitude, longitude, element, cost"
        for item in path:
            vertexElement, cost = item[0], item[1]
            latitude, longitude = self._vertexCoordinates[vertexElement][0], self._vertexCoordinates[vertexElement][1]
            pathway += '\n'
            pathway += (
                    "W, %f, %f, %i, %f" %
                    (
                        latitude,
                        longitude,
                        vertexElement.element,
                        cost)
            )
        return pathway


def graphreader(filename):
    """ Read and return the route map in filename. """
    route = RouteMap()
    file = open(filename, 'r')
    entry = file.readline()  # either 'Node' or 'Edge'
    num = 0
    while entry == 'Node\n':
        num += 1
        nodeid = int(file.readline().split()[1])
        line = file.readline().split()  # line with GPS details
        coords = (float(line[1]), float(line[2]))  # latitude, longitude
        route.add_vertex(nodeid, coords)
        entry = file.readline()  # either 'Node' or 'Edge'
    print('Read', num, 'vertices and added into the graph')
    num = 0
    while entry == 'Edge\n':
        num += 1
        source = int(file.readline().split()[1])
        sv = route.get_vertex_by_label(source)
        target = int(file.readline().split()[1])
        tv = route.get_vertex_by_label(target)
        float(file.readline().split()[1])
        time = float(file.readline().split()[1])
        # oneway = (file.readline().split()[1])
        route.add_edge(sv, tv, time)
        file.readline()  # read the one-way data
        entry = file.readline()  # either 'Node' or 'Edge'
    return route


def test():
    routemap = graphreader('corkCityData.txt')
    ids = dict()
    ids['wgb'] = 1669466540
    ids['turnerscross'] = 348809726
    ids['neptune'] = 1147697924
    ids['cuh'] = 860206013
    ids['oldoak'] = 358357
    ids['gaol'] = 3777201945
    ids['mahonpoint'] = 330068634
    sourcestr = 'wgb'
    deststr = 'neptune'
    source = routemap.get_vertex_by_label(ids[sourcestr])
    dest = routemap.get_vertex_by_label(ids[deststr])
    tree = routemap.sp(source, dest)
    print(routemap.printvlist(tree))


test()
