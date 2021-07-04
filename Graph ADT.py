class Vertex:
    def __init__(self, element):
        self._element = element

    def __str__(self):
        return str(self._element)

    def __lt__(self, v):
        return self.element < v.element

    def getElement(self):
        return self._element

    def setElement(self, element):
        self._element = element

    element = property(getElement, setElement)


class Edge:
    def __init__(self, v, w, element):
        self._vertices = (v, w)
        self._element = element

    def __str__(self):
        return '(' + str(self._vertices[0]) + '--' + str(self._vertices[1]) + ' : ' + str(self._element) + ')'

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

    def setElement(self, element):
        self._element = element

    element = property(getElement, setElement)


class Graph:
    def __init__(self):
        self._structure = dict()

    def __str__(self):
        heightString = ('|V| = ' + str(self.num_vertices()) + '; |E| = ' + str(self.num_edges()))
        vertexString = '\nVertices: '
        for v in self._structure:
            vertexString += str(v) + '-'
        edges = self.edges()
        edgeString = '\nEdges: '
        for e in edges:
            edgeString += str(e) + ' '
        return heightString + vertexString + edgeString

    def num_vertices(self):
        return len(self._structure)

    def num_edges(self):
        num = 0
        for v in self._structure:
            num += len(self._structure[v])
        return num // 2

    def vertices(self):
        return [key for key in self._structure]

    def get_vertex_by_label(self, element):
        for v in self._structure:
            if v.element == element:
                return v
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
        if (self._structure is not None
                and v in self._structure
                and w in self._structure[v]):
            return self._structure[v][w]
        return None

    def degree(self, v):
        return len(self._structure[v])

    def add_vertex(self, element):
        v = Vertex(element)
        self._structure[v] = dict()
        return v

    def add_vertex_if_new(self, element):
        for v in self._structure:
            if v.element == element:
                return v
        return self.add_vertex(element)

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


def readEuropeGraph():
    """ Read and return the graph of contiguous European countries. """
    # Ignores Iceland and Malta, includes Cyprus
    # https://www.sporcle.com/games/mslomovits/european-borders
    # Data source ^
    graph = Graph()
    file = open('Europe Borders.dat', 'r')
    count = 0
    for line in file:
        pair = line.strip('\n').split('-')
        country1 = pair[0]
        country2 = pair[1]
        v1 = graph.add_vertex_if_new(country1)
        v2 = graph.add_vertex_if_new(country2)
        graph.add_edge(v1, v2, 1)
        count += 1
    file.close()
    return graph


def processEurope():
    """ Process the Europe graph. """
    # Gibraltar included

    print('----------- Test on Europe graph ----------')

    graph = readEuropeGraph()
    print('Graph has', graph.num_vertices(), 'vertices.')
    print('Graph has', graph.num_edges(), 'edges.')
    hdv = graph.highestdegreevertex()
    print(hdv.element,
          'has the highest degree =',
          graph.degree(hdv))
    print(graph)
    for v in sorted(graph.vertices()):
        print(v, '; deg =', graph.degree(v))
    print('----------- End of test ----------')


def readNAGraph():
    """ Read and return the graph of contiguous North American countries. """
    # Ignores Cuba, etc.
    # https://www.sporcle.com/games/mslomovits/north-american-borders?playlist=national-borders&creator=mslomovits&pid=2r2e735btD
    # Data source ^
    graph = Graph()
    file = open('North America Borders.dat', 'r')
    count = 0
    for line in file:
        pair = line.strip('\n').split('-')
        country1 = pair[0]
        country2 = pair[1]
        v1 = graph.add_vertex_if_new(country1)
        v2 = graph.add_vertex_if_new(country2)
        graph.add_edge(v1, v2, 1)
        count += 1
    file.close()
    return graph


def processNA():
    """ Process the North America graph. """

    print('----------- Test on North America graph ----------')

    graph = readNAGraph()
    print('Graph has', graph.num_vertices(), 'vertices.')
    print('Graph has', graph.num_edges(), 'edges.')
    hdv = graph.highestdegreevertex()
    print(hdv.element, 'has the highest degree =', graph.degree(hdv))
    print(graph)
    for v in sorted(graph.vertices()):
        print(v, '; deg =', graph.degree(v))
    print('----------- End of test ----------')


def readSAGraph():
    """ Read and return the graph of South American countries. """
    # Includes France
    # https://www.sporcle.com/games/mslomovits/south-american-land-borders?playlist=national-borders&creator=mslomovits&pid=2r2e735btD
    # Data source ^
    graph = Graph()
    file = open('South America Borders.dat', 'r')
    count = 0
    for line in file:
        pair = line.strip('\n').split('-')
        country1 = pair[0]
        country2 = pair[1]
        v1 = graph.add_vertex_if_new(country1)
        v2 = graph.add_vertex_if_new(country2)
        graph.add_edge(v1, v2, 1)
        count += 1
    file.close()
    return graph


def processSA():
    """ Process the South America graph. """

    print('----------- Test on South America graph ----------')

    graph = readSAGraph()
    print('Graph has', graph.num_vertices(), 'vertices.')
    print('Graph has', graph.num_edges(), 'edges.')
    hdv = graph.highestdegreevertex()
    print(hdv.element, 'has the highest degree =', graph.degree(hdv))
    print(graph)
    for v in sorted(graph.vertices()):
        print(v, '; deg =', graph.degree(v))
    print('----------- End of test ----------')


def readAfricaGraph():
    """ Read and return the graph of contiguous European countries. """
    # Ignores Madagascar, etc.
    # https://www.sporcle.com/games/mslomovits/african-borders?playlist=national-borders&creator=mslomovits&pid=2r2e735btD
    # Data source ^
    graph = Graph()
    file = open('Africa Borders.dat', 'r')
    count = 0
    for line in file:
        pair = line.strip('\n').split('-')
        country1 = pair[0]
        country2 = pair[1]
        v1 = graph.add_vertex_if_new(country1)
        v2 = graph.add_vertex_if_new(country2)
        graph.add_edge(v1, v2, 1)
        count += 1
    file.close()
    return graph


def processAfrica():
    """ Process the Africa graph. """

    print('----------- Test on Africa graph ----------')

    graph = readAfricaGraph()
    print('Graph has', graph.num_vertices(), 'vertices.')
    print('Graph has', graph.num_edges(), 'edges.')
    hdv = graph.highestdegreevertex()
    print(hdv.element, 'has the highest degree =', graph.degree(hdv))
    print(graph)
    for v in sorted(graph.vertices()):
        print(v, '; deg =', graph.degree(v))
    print('----------- End of test ----------')


def readAsiaGraph():
    """ Read and return the graph of contiguous Asian countries. """
    # Ignores Japan, etc.
    # Europe-Asia borders, ie. Norway-Russia, are taken out.
    # https://www.sporcle.com/games/mslomovits/asian-borders?playlist=national-borders&creator=mslomovits&pid=2r2e735btD
    # Data source ^
    graph = Graph()
    file = open('Asia Borders.dat', 'r')
    count = 0
    for line in file:
        pair = line.strip('\n').split('-')
        country1 = pair[0]
        country2 = pair[1]
        v1 = graph.add_vertex_if_new(country1)
        v2 = graph.add_vertex_if_new(country2)
        graph.add_edge(v1, v2, 1)
        count += 1
    file.close()
    return graph


def processAsia():
    """ Process the Asia graph. """

    print('----------- Test on Asia graph ----------')

    graph = readAsiaGraph()
    print('Graph has', graph.num_vertices(), 'vertices.')
    print('Graph has', graph.num_edges(), 'edges.')
    hdv = graph.highestdegreevertex()
    print(hdv.element, 'has the highest degree =', graph.degree(hdv))
    print(graph)
    for v in sorted(graph.vertices()):
        print(v, '; deg =', graph.degree(v))
    print('----------- End of test ----------')


# processEurope()
# processNA()
# processSA()
# processAfrica()
# processAsia()
